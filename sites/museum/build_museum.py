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
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Inter:wght@300;400;500;600&family=Lora:ital,wght@0,400;0,700;1,400&family=Space+Mono&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="museum.css">
    <style>
        /* ── Search Bar Specific Styles ── */
        .search-bar {{
            background: var(--bg-color);
            padding: 1.5rem;
            border-bottom: 2px solid var(--gray-200);
        }}
        .search-bar-inner {{
            max-width: var(--max-width);
            margin: 0 auto;
            display: flex;
            align-items: center;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        .search-bar label {{
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--museum-blue);
        }}
        .search-input {{
            flex: 1;
            min-width: 200px;
            border: 2px solid var(--gray-300);
            padding: 0.75rem 1rem;
            font-size: 1rem;
            font-family: var(--sans);
            background: var(--white);
            outline: none;
            transition: all 0.2s;
            border-radius: 4px;
        }}
        .search-input:focus {{
            border-color: var(--museum-blue);
            box-shadow: 0 0 0 3px rgba(49, 91, 124, 0.1);
        }}
        
        /* ── Hero / Intro ── */
        .hero-section {{
            text-align: center;
            padding: 4rem 1.5rem;
            background: var(--white);
            border-bottom: 1px solid var(--gray-200);
            border-top: 4px solid var(--museum-gold);
        }}
        .hero-section h1 {{
            font-family: var(--serif);
            font-size: clamp(2.5rem, 5vw, 4rem);
            color: var(--black);
            margin-bottom: 1rem;
            line-height: 1.1;
        }}
        .hero-section p {{
            font-size: 1.25rem;
            color: var(--gray-500);
            max-width: 600px;
            margin: 0 auto;
        }}

        /* ── Search results overlay ── */
        #search-results {{
            display: none;
            margin-top: 1rem;
        }}
        #search-results.visible {{ display: block; }}
        .search-result-item {{
            border-bottom: 1px solid var(--gray-200);
            padding: 1.5rem 0;
        }}
        .search-result-item a {{ text-decoration: none; color: inherit; display: block; }}
        .search-result-headline {{
            font-family: var(--serif);
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--museum-blue);
            margin-bottom: 0.5rem;
            transition: color 0.15s;
        }}
        .search-result-item a:hover .search-result-headline {{ color: var(--museum-red); }}
        .search-result-meta {{ font-size: 0.85rem; color: var(--gray-500); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }}
        .search-no-results {{ font-size: 1.1rem; color: var(--gray-500); padding: 2rem 0; font-style: italic; text-align: center; }}
    </style>
</head>
<body class="site-wrapper">

<header class="site-header">
    <a href="index.html" class="site-title">{site_name}</a>
    <nav style="display: flex; gap: 1.5rem;">
        <a href="#" style="color: white; text-decoration: none; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">Exhibits</a>
        <a href="#" style="color: white; text-decoration: none; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">Collections</a>
        <a href="#" style="color: white; text-decoration: none; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">About</a>
    </nav>
</header>

<div class="search-bar">
    <div class="search-bar-inner">
        <label for="search-input">Explore Archives:</label>
        <input type="text" id="search-input" class="search-input" placeholder="Search for artifacts, people, or formats..." autocomplete="off">
        <label for="category-filter" style="margin-left:auto; display:none;">Filter:</label>
        <select id="category-filter" class="search-input" style="flex:0 0 200px;">
             <option value="">All Formats</option>
            <option value="narrative">Deep Dives</option>
            <option value="placard">Placards</option>
            <option value="biography">Biographies</option>
            <option value="spotlight">Spotlights</option>
            <option value="path">Thematic Paths</option>
            <option value="audio">Audio Scripts</option>
            <option value="lesson">Lesson Plans</option>
            <option value="scavenger">Scavenger Hunts</option>
            <option value="discussion">Discussion Guides</option>
        </select>
    </div>
</div>

<main class="museum-container">
    <div class="museum-body">
        <div id="search-results" role="region" aria-label="Search results"></div>

        <div id="article-listing">
{article_listing_html}
        </div>
    </div>
</main>

<footer style="border-top: 3px solid var(--museum-blue); padding: 2rem 1.5rem; text-align: center; margin-top: auto; background: var(--bg-color);">
    <span style="font-family: var(--serif); font-weight: 700; font-size: 1.1rem; display: block; margin-bottom: 0.5rem; color: var(--museum-blue);">{site_name}</span>
    <p style="font-size: 0.8rem; color: var(--gray-500); letter-spacing: 0.08em;">{site_tagline} &nbsp;·&nbsp; {today}</p>
    <p style="font-size: 0.8rem; color: var(--gray-500); letter-spacing: 0.08em; margin-top: 0.5rem;">A digital repository preserving the objects, software, and stories that defined the computing era.</p>
</footer>

<script>
const searchIndex = {search_index_json};

const searchInput = document.getElementById('search-input');
const categoryFilter = document.getElementById('category-filter');
const searchResults = document.getElementById('search-results');
const articleListing = document.getElementById('article-listing');

function escapeHtml(str) {{
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}}

function executeSearch() {{
    const q = searchInput.value.toLowerCase().trim();
    const cat = categoryFilter.value.toLowerCase();
    
    if (!q && !cat) {{
        searchResults.classList.remove('visible');
        searchResults.innerHTML = '';
        articleListing.style.display = '';
        return;
    }}
    
    articleListing.style.display = 'none';
    searchResults.classList.add('visible');

    const matches = searchIndex.filter(a => {{
        const textMatch = !q || a.title.toLowerCase().includes(q) || (a.dek && a.dek.toLowerCase().includes(q));
        const catMatch = !cat || (a.tag && a.tag.toLowerCase().includes(cat));
        return textMatch && catMatch;
    }});

    if (matches.length === 0) {{
        searchResults.innerHTML = '<p class="search-no-results">No artifacts found matching criteria.</p>';
        return;
    }}
    
    searchResults.innerHTML = matches.map(m => `
        <div class="search-result-item">
            <a href="${{m.path}}">
                <div class="search-result-meta">${{escapeHtml(m.tag)}} &nbsp;·&nbsp; ${{escapeHtml(m.date)}}</div>
                <div class="search-result-headline">${{escapeHtml(m.title)}}</div>
                <div style="color: var(--gray-800); font-size: 1rem;">${{escapeHtml(m.dek)}}</div>
            </a>
        </div>
    `).join('');
}}

searchInput.addEventListener('input', executeSearch);
categoryFilter.addEventListener('change', executeSearch);
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
    date, slug_title = parse_filename(filename)
    title = slug_title
    dek = ""
    tag = "Analysis"

    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()

    if filepath.endswith('.html') or filepath.endswith('.htm'):
        # Try <title>
        m = re.search(r'<title>([^<]+)</title>', raw, re.IGNORECASE)
        if m:
            title = m.group(1).strip()
        # Try <meta name="title">
        m = re.search(r'<meta[^>]+name=["\']title["\'][^>]+content=["\']([^"\']+)["\']', raw, re.IGNORECASE)
        if not m:
            m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']title["\']', raw, re.IGNORECASE)
        if m:
            title = m.group(1).strip()
        # Try <meta name="description">
        m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', raw, re.IGNORECASE)
        if not m:
            m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']', raw, re.IGNORECASE)
        if m:
            dek = m.group(1).strip()
        # Try <meta name="tag"> or <meta name="category">
        m = re.search(r'<meta[^>]+name=["\'](?:tag|category)["\'][^>]+content=["\']([^"\']+)["\']', raw, re.IGNORECASE)
        if m:
            tag = m.group(1).strip()
        # Fallback dek: first <p> text after <h1>
        if not dek:
            m = re.search(r'<h1[^>]*>.*?</h1>\s*(?:<[^>]+>\s*)*<p[^>]*>(.*?)</p>', raw, re.IGNORECASE | re.DOTALL)
            if m:
                inner = re.sub(r'<[^>]+>', '', m.group(1)).strip()
                dek = inner[:220] + ('…' if len(inner) > 220 else '')
    else:
        # Markdown fallback
        lines = raw.splitlines()
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                dek = stripped[:220] + ('…' if len(stripped) > 220 else '')
                break

    if date:
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%B %-d, %Y")
        except ValueError:
            formatted_date = date
    else:
        formatted_date = "2026"

    return {
        "title": title,
        "dek": dek,
        "date": formatted_date,
        "tag": tag,
        "tags_set": set(t.strip().lower() for t in tag.replace('|', ',').split(',') if t.strip()),
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


def build_sidebar_html(related):
    """Build the aside sidebar HTML for a list of related article metas."""
    if not related:
        return ''
    items = ''
    for art in related:
        url = art['filename'].replace('.md', '.html')
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


def post_process_article(html, sidebar_html, meta):
    """
    Ensure the article has a proper layout. The museum bot outputs raw HTML
    snippets (usually starting with <main class="museum-body">). We must wrap
    them in a complete valid HTML document with the museum-container.
    """
    import html as html_lib
    title = html_lib.escape(meta.get('title', 'Museum Archive'))
    dek = html_lib.escape(meta.get('dek', ''))
    
    # Strip any stray html/head/body tags if the AI hallucinated them
    html = re.sub(r'<!DOCTYPE html>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'</?html[^>]*>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'</?head[^>]*>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'</?body[^>]*>', '', html, flags=re.IGNORECASE)
    
    # Remove the metadata block to prevent it from rendering at the top
    html = re.sub(r'<div class="metadata" style="display:none;">.*?</div>', '', html, flags=re.IGNORECASE | re.DOTALL)

    full_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Mimms Museum</title>
    <meta name="description" content="{dek}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="museum.css">
</head>
<body class="site-wrapper">
    <header class="site-header">
        <a href="index.html" class="site-title">Mimms Museum</a>
        <a href="index.html" class="back-link" style="color:white;text-decoration:none;font-size:0.9rem;">Return to Archives &rarr;</a>
    </header>

    <div class="museum-container">
{html}
    </div>

    <footer style="border-top: 3px solid #315B7C; padding: 2rem 1.5rem; text-align: center; margin-top: auto;">
        <span style="font-family: 'Playfair Display', Georgia, serif; font-weight: 700; font-size: 1.1rem; display: block; margin-bottom: 0.5rem; color: #315B7C;">Mimms Museum</span>
        <p style="font-size: 0.8rem; color: #4B5563; letter-spacing: 0.08em;">Preserving the artifacts of computing history</p>
    </footer>
</body>
</html>"""
    return full_page

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
    """Build the museum gallery grid HTML for index."""
    if not articles:
        return '<p style="color:var(--gray-500); font-style:italic; text-align:center; padding: 4rem 0;">No artifacts published in the digital archive yet.</p>'

    # Sort latest first
    sorted_arts = sorted(articles, key=lambda a: a['date'], reverse=True)

    def article_url(art):
        return art['filename'].replace('.md', '.html')

    html = """
    <div class="articles-section">
        <h2 style="font-family: var(--serif); font-size: 1.5rem; font-weight: 700; border-bottom: 3px solid var(--museum-blue); padding-bottom: 0.5rem; margin-bottom: 2rem; color: var(--museum-blue); text-transform: uppercase; letter-spacing: 0.05em;">Digital Archive Collections</h2>
        <div class="article-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 2.5rem;">
"""
    for art in sorted_arts:
        html += f"""
            <div class="article-card" style="border: 1px solid var(--gray-200); background: var(--white); padding: 2rem; transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s; height: 100%; display: flex; flex-direction: column; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
                <a href="{article_url(art)}" style="text-decoration: none; color: inherit; display: flex; flex-direction: column; height: 100%;">
                    <span class="article-card-tag" style="font-size: 0.75rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--museum-red); display: block; margin-bottom: 1rem; border-bottom: 1px solid var(--gray-100); padding-bottom: 0.5rem;">{art['tag']}</span>
                    <div class="article-card-headline" style="font-family: var(--serif); font-size: 1.5rem; font-weight: 700; line-height: 1.25; margin-bottom: 1rem; color: var(--black);">{art['title']}</div>
                    <div class="article-card-dek" style="font-size: 1.05rem; color: var(--gray-500); line-height: 1.6; margin-bottom: 2rem; flex: 1;">{art['dek']}</div>
                    <div class="article-card-meta" style="font-size: 0.8rem; color: var(--gray-400); font-family: var(--mono); text-transform: uppercase;">Aquired: {art['date']}</div>
                </a>
            </div>
"""
    html += "        </div>\n    </div>\n"

    # Minimal hover effect override
    html += """
    <style>
    .article-card:hover { transform: translateY(-4px); box-shadow: 0 12px 20px -5px rgba(0,0,0,0.1) !important; border-color: var(--museum-gold) !important; }
    .article-card:hover .article-card-headline { color: var(--museum-blue); }
    </style>
    """

    return html

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="News-style static site generator")
    parser.add_argument("--source", required=True, help="Directory of HTML/MD article files")
    parser.add_argument("--s3-bucket", required=False, help="S3 path, e.g. s3://bucket/path/")
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
    css_src = os.path.join(os.path.dirname(__file__), "museum.css")
    if os.path.exists(css_src):
        shutil.copy2(css_src, os.path.join(build_dir, "museum.css"))
        print(f"  → Copied museum.css to {build_dir}/")
    else:
        print(f"  ⚠  museum.css not found at {css_src} — articles may lack shared styles")

    # Copy image assets into build dir (if present)
    images_src = os.path.join(source_dir, "images")
    images_dst = os.path.join(build_dir, "images")
    if os.path.isdir(images_src):
        shutil.copytree(images_src, images_dst, dirs_exist_ok=True)
        print(f"  → Copied images/ to {images_dst}/")

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

        # Compute related articles and inject sidebar
        related = related_articles(meta, articles)
        sidebar_html = build_sidebar_html(related)
        html = post_process_article(html, sidebar_html, meta)

        with open(os.path.join(build_dir, out_name), 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"  + {fname}  →  \"{meta['title']}\"  (related: {len(related)})")

    # Build search index
    search_index = [
        {
            "title": a["title"],
            "dek": a["dek"],
            "tag": a["tag"],
            "date": a["date"],
            "path": a["filename"].replace('.md', '.html'),
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
        except subprocess.CalledProcessError as e:
            print(f"Error deploying to S3: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
