#!/usr/bin/env python3
"""
build_news.py — News-article-style static site generator.

Reads a directory of pre-written HTML articles (or markdown, auto-converted)
and generates a news homepage (NYT/Atlantic-style) with search, then syncs
to S3.

Usage:
    python3 build_news.py \\
        --source /path/to/articles/ \\
        --s3-bucket s3://my-bucket/path/ \\
        --site-name "The Dispatch" \\
        --site-tagline "Evidence-based analysis of political claims"
"""

import os
import sys
import shutil
import argparse
import subprocess
import json
import re
from datetime import datetime

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

# ---------------------------------------------------------------------------
# HTML Templates
# ---------------------------------------------------------------------------

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_name}</title>
    <meta name="description" content="{site_tagline}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

        :root {{
            --black: #111111;
            --white: #FFFFFF;
            --gray-50: #F9FAFB;
            --gray-100: #F3F4F6;
            --gray-200: #E5E7EB;
            --gray-400: #9CA3AF;
            --gray-600: #4B5563;
            --gray-800: #1F2937;
            --accent: #B91C1C;
            --font-serif: "Playfair Display", Georgia, "Times New Roman", serif;
            --font-sans: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        body {{
            font-family: var(--font-sans);
            background: var(--white);
            color: var(--black);
            line-height: 1.6;
        }}

        /* ── Masthead ── */
        .masthead {{
            border-bottom: 3px solid var(--black);
            padding: 0 1.5rem;
        }}
        .masthead-inner {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2rem 0 1.5rem;
            gap: 0.5rem;
        }}
        .masthead-date {{
            font-family: var(--font-sans);
            font-size: 0.8rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--gray-600);
        }}
        .masthead-title {{
            font-family: var(--font-serif);
            font-size: clamp(2.5rem, 6vw, 5rem);
            font-weight: 900;
            letter-spacing: -0.02em;
            line-height: 1;
            text-align: center;
        }}
        .masthead-tagline {{
            font-size: 0.9rem;
            color: var(--gray-600);
            font-style: italic;
            text-align: center;
        }}
        .masthead-rule {{
            width: 100%;
            border: none;
            border-top: 1px solid var(--gray-200);
            margin-top: 1rem;
        }}
        .masthead-nav {{
            display: flex;
            gap: 1.5rem;
            padding: 0.6rem 0;
            font-size: 0.78rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            font-weight: 500;
        }}
        .masthead-nav a {{
            color: var(--black);
            text-decoration: none;
            transition: color 0.15s;
        }}
        .masthead-nav a:hover {{ color: var(--accent); }}

        /* ── Search ── */
        .search-bar {{
            border-bottom: 1px solid var(--gray-200);
            padding: 0.75rem 1.5rem;
            background: var(--gray-50);
        }}
        .search-bar-inner {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        .search-bar label {{
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--gray-600);
            white-space: nowrap;
        }}
        .search-input {{
            flex: 1;
            border: 1px solid var(--gray-200);
            border-bottom: 2px solid var(--black);
            padding: 0.5rem 0.75rem;
            font-size: 0.95rem;
            font-family: var(--font-serif);
            background: var(--white);
            outline: none;
            transition: border-color 0.15s;
        }}
        .search-input:focus {{ border-color: var(--black); border-bottom-width: 3px; }}
        .search-input::placeholder {{ color: var(--gray-400); font-style: italic; }}

        /* ── Section label ── */
        .section-label {{
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 0.75rem;
        }}

        /* ── Main layout ── */
        .main-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2.5rem 1.5rem;
        }}

        /* ── Featured article (top of grid) ── */
        .featured {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 3rem;
            border-bottom: 1px solid var(--gray-200);
            padding-bottom: 2.5rem;
            margin-bottom: 2.5rem;
        }}
        @media (max-width: 768px) {{
            .featured {{ grid-template-columns: 1fr; }}
        }}
        .featured.no-secondary {{
            display: block;
        }}
        .featured.no-secondary .featured-main {{
            max-width: 800px;
            margin: 0 auto;
        }}
        .featured-main a {{ text-decoration: none; color: inherit; }}
        .featured-tag {{
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--accent);
            display: block;
            margin-bottom: 0.6rem;
        }}
        .featured-headline {{
            font-family: var(--font-serif);
            font-size: clamp(1.6rem, 3vw, 2.4rem);
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 0.75rem;
            transition: color 0.15s;
        }}
        .featured-main a:hover .featured-headline {{ color: var(--accent); }}
        .featured-dek {{
            font-size: 1rem;
            color: var(--gray-600);
            line-height: 1.55;
            margin-bottom: 0.75rem;
        }}
        .featured-meta {{
            font-size: 0.78rem;
            color: var(--gray-400);
            letter-spacing: 0.05em;
        }}
        .featured-secondary {{ display: flex; flex-direction: column; gap: 1.5rem; }}
        .secondary-item a {{ text-decoration: none; color: inherit; }}
        .secondary-headline {{
            font-family: var(--font-serif);
            font-size: 1.1rem;
            font-weight: 700;
            line-height: 1.3;
            margin-bottom: 0.3rem;
            transition: color 0.15s;
        }}
        .secondary-item a:hover .secondary-headline {{ color: var(--accent); }}
        .secondary-dek {{ font-size: 0.88rem; color: var(--gray-600); margin-bottom: 0.3rem; }}
        .secondary-meta {{ font-size: 0.75rem; color: var(--gray-400); }}
        .secondary-divider {{ border: none; border-top: 1px solid var(--gray-200); }}

        /* ── Article grid ── */
        .articles-section h2 {{
            font-family: var(--font-serif);
            font-size: 1.2rem;
            font-weight: 700;
            border-bottom: 3px solid var(--black);
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
        }}
        .article-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }}
        .article-card a {{ text-decoration: none; color: inherit; display: block; }}
        .article-card-tag {{
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--accent);
            display: block;
            margin-bottom: 0.4rem;
        }}
        .article-card-headline {{
            font-family: var(--font-serif);
            font-size: 1.2rem;
            font-weight: 700;
            line-height: 1.3;
            margin-bottom: 0.4rem;
            transition: color 0.15s;
        }}
        .article-card a:hover .article-card-headline {{ color: var(--accent); }}
        .article-card-dek {{ font-size: 0.875rem; color: var(--gray-600); line-height: 1.5; margin-bottom: 0.4rem; }}
        .article-card-meta {{ font-size: 0.75rem; color: var(--gray-400); }}
        .article-card {{ border-top: 1px solid var(--gray-200); padding-top: 1.25rem; }}

        /* ── Search results overlay ── */
        #search-results {{
            display: none;
            margin-top: 1rem;
        }}
        #search-results.visible {{ display: block; }}
        .search-result-item {{
            border-bottom: 1px solid var(--gray-200);
            padding: 1rem 0;
        }}
        .search-result-item a {{ text-decoration: none; color: inherit; }}
        .search-result-headline {{
            font-family: var(--font-serif);
            font-size: 1.15rem;
            font-weight: 700;
            transition: color 0.15s;
        }}
        .search-result-item a:hover .search-result-headline {{ color: var(--accent); }}
        .search-result-meta {{ font-size: 0.78rem; color: var(--gray-400); margin-top: 0.25rem; }}
        .search-no-results {{ font-size: 0.9rem; color: var(--gray-600); padding: 1.5rem 0; font-style: italic; }}

        /* ── Footer ── */
        footer {{
            border-top: 3px solid var(--black);
            padding: 2rem 1.5rem;
            text-align: center;
        }}
        footer p {{
            font-size: 0.8rem;
            color: var(--gray-600);
            letter-spacing: 0.08em;
        }}
        footer .footer-name {{
            font-family: var(--font-serif);
            font-weight: 700;
            font-size: 1.1rem;
            display: block;
            margin-bottom: 0.5rem;
        }}
    </style>
</head>
<body>

<header class="masthead">
    <div class="masthead-inner">
        <span class="masthead-date">{today}</span>
        <h1 class="masthead-title">{site_name}</h1>
        <p class="masthead-tagline">{site_tagline}</p>
        <hr class="masthead-rule">
        <nav class="masthead-nav">
            <a href="#">Analysis</a>
            <a href="#">Fact Check</a>
            <a href="#">Data</a>
            <a href="#">About</a>
        </nav>
    </div>
</header>

<div class="search-bar">
    <div class="search-bar-inner">
        <label for="search-input">Search:</label>
        <input type="text" id="search-input" class="search-input" placeholder="Search articles…" autocomplete="off">
    </div>
</div>

<main class="main-content">
    <div id="search-results" role="region" aria-label="Search results"></div>

    <div id="article-listing">
{article_listing_html}
    </div>
</main>

<footer>
    <span class="footer-name">{site_name}</span>
    <p>{site_tagline} &nbsp;·&nbsp; {today}</p>
    <p style="margin-top:0.5rem">All analyses are independent and non-partisan. Data sourced from government agencies, peer-reviewed research, and established news organizations.</p>
</footer>

<script>
const searchIndex = {search_index_json};

const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');
const articleListing = document.getElementById('article-listing');

function escapeHtml(str) {{
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}}

searchInput.addEventListener('input', function() {{
    const q = this.value.toLowerCase().trim();
    if (!q) {{
        searchResults.classList.remove('visible');
        searchResults.innerHTML = '';
        articleListing.style.display = '';
        return;
    }}
    articleListing.style.display = 'none';
    searchResults.classList.add('visible');

    const matches = searchIndex.filter(a =>
        a.title.toLowerCase().includes(q) ||
        (a.dek && a.dek.toLowerCase().includes(q)) ||
        (a.tag && a.tag.toLowerCase().includes(q))
    );

    if (matches.length === 0) {{
        searchResults.innerHTML = '<p class="search-no-results">No articles found for that query.</p>';
        return;
    }}
    searchResults.innerHTML = matches.map(m => `
        <div class="search-result-item">
            <a href="${{m.path}}">
                <div class="search-result-headline">${{escapeHtml(m.title)}}</div>
                <div class="search-result-meta">${{escapeHtml(m.tag)}} &nbsp;·&nbsp; ${{escapeHtml(m.date)}}</div>
            </a>
        </div>
    `).join('');
}});
</script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

DATE_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})_(.+)\.(html?|md)$')

def parse_filename(filename):
    """Extract date and slug from filename like 2026-03-09_immigrant-crime.html"""
    m = DATE_RE.match(filename)
    if m:
        return m.group(1), m.group(2).replace('-', ' ').title()
    return None, os.path.splitext(filename)[0]

def extract_article_meta(filepath, filename):
    """Pull title, description, date from HTML or markdown."""
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()

    title = ""
    dek = ""
    tag = "Analysis"
    date_str = ""
    slug_str = ""

    # Try extracting from meta tags
    def get_meta_content(name_attr):
        match = re.search(rf'<meta\b[^>]*name=["\'](?:{name_attr})["\'][^>]*>', raw, re.IGNORECASE)
        if match:
            # Match greedily up to the last quote
            c_match = re.search(r'content=["\'](.*)["\']', match.group(0), re.IGNORECASE)
            if c_match: return c_match.group(1).strip()
        return ""

    date_str = get_meta_content("date")
    slug_str = get_meta_content("slug")
    title = get_meta_content("title")
    tag = get_meta_content("tag") or get_meta_content("category") or "Analysis"
    dek = get_meta_content("description")

    parsed_date, parsed_slug = parse_filename(filename)
    if not date_str: date_str = parsed_date
    if not slug_str: slug_str = parsed_slug
    if not title:
        m_t = re.search(r'<title>([^<]+)</title>', raw, re.IGNORECASE)
        title = m_t.group(1).strip() if m_t else parsed_slug

    if not dek:
        m = re.search(r'<h1[^>]*>.*?</h1>\s*(?:<[^>]+>\s*)*<p[^>]*>(.*?)</p>', raw, re.IGNORECASE | re.DOTALL)
        if m:
            inner = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            dek = inner[:220] + ('…' if len(inner) > 220 else '')

    # Safe format date
    if date_str:
        try:
            formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %-d, %Y")
        except ValueError:
            formatted_date = date_str
    else:
        formatted_date = "2026"

    return {
        "title": title,
        "dek": dek,
        "raw_date": date_str or "2026-01-01",
        "date": formatted_date,
        "tag": tag,
        "tags_set": set(t.strip().lower() for t in tag.replace('|', ',').split(',') if t.strip()),
        "slug": slug_str
    }


def related_articles(current, all_articles, n=4):
    """Return up to n related articles sorted by tag overlap then recency."""
    others = [a for a in all_articles if a['filename'] != current['filename']]
    cur_tags = current.get('tags_set', set())

    def score(a):
        overlap = len(cur_tags & a.get('tags_set', set()))
        # secondary sort: recency (date string, lexicographic works for YYYY-MM-DD)
        return (overlap, a['date'])

    return sorted(others, key=score, reverse=True)[:n]


def build_sidebar_html(related, depth_prefix=""):
    """Build the aside sidebar HTML for a list of related article metas."""
    if not related:
        return ''
    items = ''
    for art in related:
        # Resolve the nested path
        parts = art['raw_date'].split("-")
        cat_slug = art['tag'].split('|')[0].strip().lower().replace(" ", "-").replace(":", "")
        slug = art.get('slug', art['filename'].split("_", 1)[-1].replace(".md", ".html") if "_" in art['filename'] else art['filename'])
        if not slug.endswith('.html'): slug += '.html'
        
        if len(parts) == 3:
            url = f"{depth_prefix}{cat_slug}/{parts[0]}/{parts[1]}/{parts[2]}/{slug}"
        else:
            url = f"{depth_prefix}{slug}"
            
        tag_display = art['tag'].split('|')[0].strip()
        items += f'''
        <div class="sidebar-article">
            <a href="{url}">
                <span class="sidebar-article-tag">{tag_display}</span>
                <div class="sidebar-article-title">{art['title']}</div>
                <div class="sidebar-article-date">{art['date']}</div>
            </a>
        </div>'''
    return f'''
    <aside class="article-sidebar">
        <div class="sidebar-section">
            <div class="sidebar-heading">Related Articles</div>
            {items}
        </div>
    </aside>'''


def post_process_article(html, sidebar_html):
    """
    Ensure the article has a proper two-column layout by wrapping
    .article-header + .article-body (or .article-main) in .article-container
    with an appended sidebar.

    Strategy: find the outermost <main>, <article>, or <div> that contains
    the article-header/article-body, then rewrap it.
    """
    # Find the closing </footer> so we know where body content ends
    # The injection point: we find the block between </header> and <footer>
    # and wrap its contents in the two-column layout.

    # Locate the site-header close and footer open
    header_end = re.search(r'</header>', html, re.IGNORECASE)
    footer_start = re.search(r'<footer\b', html, re.IGNORECASE)

    if not header_end or not footer_start:
        # Can't parse, return as-is
        return html

    before = html[:header_end.end()]          # everything up to and incl </header>
    content = html[header_end.end():footer_start.start()]  # inner content
    after = html[footer_start.start():]       # <footer>...</footer> and beyond

    # Check if the agent already wrapped things in .article-container.
    # If so, just inject the sidebar inside it.
    if 'article-container' in content:
        if sidebar_html:
            # Try to inject sidebar before the closing tag of article-container
            content = re.sub(
                r'(</div>\s*)(</main>|</section>|</div>)',
                lambda m: sidebar_html + m.group(0),
                content, count=1
            )
        return before + content + after

    # Otherwise, wrap everything in the two-column layout
    wrapped = f'''
<div class="article-container">
    <div class="article-main">
{content}
    </div>
{sidebar_html}
</div>
'''
    return before + wrapped + after

def markdown_to_html_standalone(md_content, title):
    """Convert markdown to a minimal standalone HTML article page."""
    if not HAS_MARKDOWN:
        body = "<pre>" + md_content.replace("&","&amp;").replace("<","&lt;") + "</pre>"
    else:
        md = markdown.Markdown(extensions=['fenced_code', 'tables', 'sane_lists'])
        body = md.convert(md_content)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--accent:#B91C1C;--serif:"Playfair Display",Georgia,serif;--sans:"Inter",sans-serif}}
body{{font-family:var(--sans);background:#fff;color:#111;line-height:1.7;padding:2rem 1rem}}
.article-body{{max-width:680px;margin:0 auto}}
h1{{font-family:var(--serif);font-size:clamp(1.8rem,4vw,3rem);font-weight:900;line-height:1.15;margin-bottom:1rem}}
h2{{font-family:var(--serif);font-size:1.5rem;margin:2rem 0 0.75rem;border-top:1px solid #ddd;padding-top:1.5rem}}
h3{{font-family:var(--serif);font-size:1.15rem;margin:1.5rem 0 0.5rem}}
p{{margin-bottom:1.25rem;font-size:1.0625rem}}
a{{color:var(--accent)}}
blockquote{{border-left:3px solid #111;padding-left:1rem;font-style:italic;margin:1.5rem 0}}
sup a{{color:var(--accent);font-size:0.75rem}}
</style>
</head>
<body>
<div class="article-body">
<a href="index.html" style="font-size:0.85rem;color:#666;text-decoration:none;display:block;margin-bottom:2rem">&larr; Back to index</a>
{body}
</div>
</body>
</html>"""

def build_featured_html(articles):
    """Build the featured+grid section HTML for index."""
    if not articles:
        return '<p style="color:#666;font-style:italic">No articles published yet.</p>'

    # Sort latest first
    sorted_arts = sorted(articles, key=lambda a: a['date'], reverse=True)

    featured = sorted_arts[0]
    secondary = sorted_arts[1:4]
    rest = sorted_arts[4:]

    def article_url(art):
        parts = art['raw_date'].split("-")
        cat_slug = art['tag'].split('|')[0].strip().lower().replace(" ", "-").replace(":", "")
        slug = art.get('slug', art['filename'].split("_", 1)[-1].replace(".md", ".html") if "_" in art['filename'] else art['filename'])
        if not slug.endswith('.html'): slug += '.html'
        if len(parts) == 3:
            return f"{cat_slug}/{parts[0]}/{parts[1]}/{parts[2]}/{slug}"
        return f"{slug}"

    # Featured block
    featured_html = f"""
    <div class="featured{'' if secondary else ' no-secondary'}">
        <div class="featured-main">
            <a href="{article_url(featured)}">
                <span class="featured-tag">{featured['tag']}</span>
                <h2 class="featured-headline">{featured['title']}</h2>
                <p class="featured-dek">{featured['dek']}</p>
                <span class="featured-meta">{featured['date']}</span>
            </a>
        </div>
"""
    if secondary:
        featured_html += """
        <div class="featured-secondary" style="border-left: 1px solid var(--gray-200); padding-left: 2rem;">
"""
        for i, art in enumerate(secondary):
            featured_html += f"""
            {'<hr class="secondary-divider">' if i > 0 else ''}
            <div class="secondary-item">
                <a href="{article_url(art)}">
                    <span style="font-size:0.68rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#B91C1C;display:block;margin-bottom:0.3rem">{art['tag']}</span>
                    <div class="secondary-headline">{art['title']}</div>
                    <div class="secondary-dek">{art['dek']}</div>
                    <div class="secondary-meta">{art['date']}</div>
                </a>
            </div>
"""
        featured_html += "        </div>\n"

    featured_html += "    </div>\n"

    # Rest of articles grid
    if rest:
        featured_html += """
    <div class="articles-section">
        <h2>More Analysis</h2>
        <div class="article-grid">
"""
        for art in rest:
            featured_html += f"""
            <div class="article-card">
                <a href="{article_url(art)}">
                    <span class="article-card-tag">{art['tag']}</span>
                    <div class="article-card-headline">{art['title']}</div>
                    <div class="article-card-dek">{art['dek']}</div>
                    <div class="article-card-meta">{art['date']}</div>
                </a>
            </div>
"""
        featured_html += "        </div>\n    </div>\n"

    return featured_html

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="News-style static site generator")
    parser.add_argument("--source", required=True, help="Directory of HTML/MD article files")
    parser.add_argument("--s3-bucket", required=False, help="S3 path, e.g. s3://bucket/path/")
    parser.add_argument("--cloudfront-id", required=False, help="CloudFront Distribution ID for cache invalidation")
    parser.add_argument("--site-name", default="The Dispatch", help="Publication name")
    parser.add_argument("--site-tagline", default="Evidence-based political analysis", help="Tagline")
    args = parser.parse_args()

    source_dir = os.path.abspath(args.source)
    if not os.path.isdir(source_dir):
        print(f"Error: source directory '{source_dir}' does not exist.")
        sys.exit(1)

    build_dir = os.path.join(os.path.dirname(__file__), "output")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)

    articles = []

    # Copy shared stylesheet into build dir
    css_src = os.path.join(os.path.dirname(__file__), "article.css")
    if os.path.exists(css_src):
        shutil.copy2(css_src, os.path.join(build_dir, "article.css"))
        print(f"  → Copied article.css to {build_dir}/")
    else:
        print(f"  ⚠  article.css not found at {css_src} — articles may lack shared styles")

    # Process each article file
    for fname in sorted(os.listdir(source_dir)):
        if not (fname.endswith('.html') or fname.endswith('.htm') or fname.endswith('.md')):
            continue
        if fname.startswith('_') or fname.startswith('.'):
            continue

        src_path = os.path.join(source_dir, fname)
        meta = extract_article_meta(src_path, fname)
        meta['filename'] = fname
        meta['src_path'] = src_path

        articles.append(meta)

    # Second pass: write articles with sidebars
    for meta in articles:
        fname = meta['filename']
        src_path = meta['src_path']

        if fname.endswith('.md'):
            with open(src_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            html = markdown_to_html_standalone(md_content, meta['title'])
            out_name = fname.replace('.md', '.html')
            meta['filename'] = out_name
        else:
            with open(src_path, 'r', encoding='utf-8') as f:
                html = f.read()
            out_name = fname

        # Compute relative nested path structure: YYYY/MM/DD/category_slug/slug.html
        parts = meta['raw_date'].split("-")
        cat_slug = meta['tag'].split('|')[0].strip().lower().replace(" ", "-").replace(":", "")
        slug = meta.get('slug', out_name.split("_", 1)[-1] if "_" in out_name else out_name)
        if not slug.endswith('.html'): slug += '.html'
        
        if len(parts) == 3:
            out_rel_dir = os.path.join(cat_slug, parts[0], parts[1], parts[2])
            meta['nested_path'] = f"{cat_slug}/{parts[0]}/{parts[1]}/{parts[2]}/{slug}"
        else:
            out_rel_dir = ""
            meta['nested_path'] = f"{slug}"
            
        full_out_dir = os.path.join(build_dir, out_rel_dir)
        os.makedirs(full_out_dir, exist_ok=True)

        depth_prefix = "../" * 4 if len(parts) == 3 else ""

        # Compute related articles and inject sidebar
        related = related_articles(meta, articles)
        sidebar_html = build_sidebar_html(related, depth_prefix)
        html = post_process_article(html, sidebar_html)
        
        # Convert relative asset links into absolute root links inside the HTML
        html = re.sub(r'href="index\.html"', f'href="{depth_prefix}index.html"', html)
        html = re.sub(r'href="article\.css"', f'href="{depth_prefix}article.css"', html)
        # Fix backlink with ← All Articles
        html = re.sub(r'href="\.\./[^"]*index\.html"', f'href="{depth_prefix}index.html"', html)
        html = re.sub(r'href="/"', f'href="{depth_prefix}index.html"', html)

        with open(os.path.join(full_out_dir, slug), 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"  + {fname}  →  \"{meta['title']}\"")

    # Build search index
    search_index = [
        {
            "title": a["title"],
            "dek": a["dek"],
            "tag": a["tag"],
            "date": a["date"],
            "path": a.get("nested_path", "/" + a["filename"].replace('.md', '.html')),
        }
        for a in articles
    ]

    today = datetime.now().strftime("%B %-d, %Y")

    # Build index.html
    article_listing_html = build_featured_html(articles)
    index_html = INDEX_TEMPLATE.format(
        site_name=args.site_name,
        site_tagline=args.site_tagline,
        today=today,
        article_listing_html=article_listing_html,
        search_index_json=json.dumps(search_index),
    )
    with open(os.path.join(build_dir, "index.html"), 'w', encoding='utf-8') as f:
        f.write(index_html)

    # Write search index JSON
    with open(os.path.join(build_dir, "search_index.json"), 'w', encoding='utf-8') as f:
        json.dump(search_index, f)

    print(f"\nBuilt {len(articles)} article(s) → {build_dir}/index.html")

    if args.s3_bucket:
        bucket = args.s3_bucket.rstrip('/') + '/'
        print(f"\nDeploying to {bucket} ...")
        cmd = ["aws", "s3", "sync", build_dir, bucket, "--delete"]
        try:
            subprocess.run(cmd, check=True)
            print("Successfully published to S3.")

            if args.cloudfront_id:
                print(f"Invalidating CloudFront cache for {args.cloudfront_id} ...")
                cf_cmd = ["aws", "cloudfront", "create-invalidation", "--distribution-id", args.cloudfront_id, "--paths", "/*"]
                subprocess.run(cf_cmd, check=True)
                print("CloudFront invalidation requested.")

            # Git auto-commit
            print("Committing and pushing changes to git...")
            repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            site_dir = "sites/news/"
            
            subprocess.run(["git", "add", site_dir], cwd=repo_root, check=True)
            status = subprocess.run(["git", "status", "--porcelain", site_dir], cwd=repo_root, capture_output=True, text=True)
            if status.stdout.strip():
                subprocess.run(["git", "commit", "-m", f"Auto-publish news updates {today}"], cwd=repo_root, check=True)
                subprocess.run(["git", "push"], cwd=repo_root, check=True)
                print("Git commit and push successful.")
            else:
                print("No new changes to commit.")

        except subprocess.CalledProcessError as e:
            print(f"Error deploying: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
