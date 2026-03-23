import os
import sys
import shutil
import argparse
import subprocess
import json
import re
import markdown
import yaml
from datetime import datetime

# ---------------------------------------------------------------------------
# YAML frontmatter parsing
# ---------------------------------------------------------------------------

def parse_frontmatter(content):
    """Extract YAML frontmatter dict and remaining markdown body."""
    if not content.lstrip().startswith('---'):
        return {}, content
    # Strip leading whitespace before ---
    content = content.lstrip()
    end = content.find('\n---', 3)
    if end == -1:
        return {}, content
    yaml_str = content[3:end].strip()
    body = content[end + 4:].lstrip('\n')
    try:
        meta = yaml.safe_load(yaml_str) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, body

# ---------------------------------------------------------------------------
# Title helpers
# ---------------------------------------------------------------------------

TITLE_STRIP_PREFIXES = [
    "Research Report: ",
    "Research Report:",
    "Research Report — ",
    "Research Report—",
]

def clean_title(raw_title):
    """Remove 'Research Report:' and similar boilerplate from the H1 title."""
    for prefix in TITLE_STRIP_PREFIXES:
        if raw_title.startswith(prefix):
            return raw_title[len(prefix):].strip()
    return raw_title

def extract_h1_title(markdown_content):
    match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "Untitled Document"

# ---------------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------------

DATE_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})_')

def parse_date_from_filename(filename):
    m = DATE_RE.match(filename)
    return m.group(1) if m else None

def format_date(date_str):
    """Format YYYY-MM-DD as 'March 5, 2026'."""
    if not date_str:
        return ""
    try:
        return datetime.strptime(str(date_str), "%Y-%m-%d").strftime("%B %-d, %Y")
    except (ValueError, TypeError):
        return str(date_str)

# ---------------------------------------------------------------------------
# HTML Templates
# ---------------------------------------------------------------------------

TEMPLATE_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,800;1,400&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
    tailwind.config = {{
        theme: {{
            extend: {{
                fontFamily: {{
                    sans: ['"Source Serif 4"', 'Georgia', 'serif'],
                    serif: ['"Playfair Display"', 'Georgia', 'serif'],
                    mono: ['"JetBrains Mono"', 'monospace'],
                }},
                colors: {{
                    background: '#FFFFFF',
                    foreground: '#000000',
                    muted: '#F5F5F5',
                    mutedForeground: '#525252',
                    border: '#000000',
                    borderLight: '#E5E5E5',
                }}
            }}
        }}
    }}
    </script>
    <style>
        body {{ background-color: #FFFFFF; color: #000000; border-radius: 0 !important; }}
        * {{ border-radius: 0 !important; }}
        h1, h2, h3, h4, h5, h6 {{ font-family: "Playfair Display", Georgia, serif; letter-spacing: -0.025em; }}
        .texture-global {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
            opacity: 0.02;
        }}
        .md-content h1 {{ font-size: 3.5rem; margin-bottom: 2rem; font-weight: 800; line-height: 1; text-transform: uppercase; }}
        .md-content h2 {{ font-size: 2.5rem; margin-top: 3rem; margin-bottom: 1.5rem; font-weight: 600; border-top: 4px solid #000; padding-top: 1.5rem; }}
        .md-content h3 {{ font-size: 1.5rem; margin-top: 2rem; margin-bottom: 1rem; font-weight: 600; }}
        .md-content p {{ margin-bottom: 1.5rem; line-height: 1.625; font-size: 1.125rem; font-family: "Source Serif 4", Georgia, serif; }}
        .md-content a {{ text-decoration: underline; text-decoration-thickness: 1px; transition: all 100ms; }}
        .md-content a:hover {{ text-decoration-thickness: 3px; }}
        .md-content ul {{ list-style-type: square; padding-left: 2rem; margin-bottom: 1.5rem; font-family: "Source Serif 4"; font-size: 1.125rem; }}
        .md-content ol {{ list-style-type: decimal; padding-left: 2rem; margin-bottom: 1.5rem; font-family: "Source Serif 4"; font-size: 1.125rem; }}
        .md-content pre {{ background-color: #FFF; padding: 1.5rem; border: 1px solid #000; margin-bottom: 1.5rem; overflow-x: auto; font-family: "JetBrains Mono", monospace; font-size: 0.875rem; }}
        .md-content code {{ font-family: "JetBrains Mono", monospace; font-size: 0.875rem; background-color: #FFF; padding: 0.125rem 0.25rem; border: 1px solid #E5E5E5; }}
        .md-content pre code {{ border: none; padding: 0; background: transparent; }}
        .md-content blockquote {{ border-left: 4px solid #000; padding-left: 1.5rem; font-style: italic; font-size: 1.5rem; font-family: "Playfair Display", Georgia, serif; margin: 2rem 0; opacity: 0.9; }}
        .md-content hr {{ border: none; border-top: 4px solid #000; margin: 3rem 0; }}
        .md-content table {{ width: 100%; border-collapse: collapse; margin-bottom: 2rem; }}
        .md-content th, .md-content td {{ border: 1px solid #000; padding: 0.75rem; text-align: left; font-family: "Source Serif 4"; }}
        .md-content th {{ font-weight: 600; text-transform: uppercase; font-family: "JetBrains Mono"; font-size: 0.875rem; letter-spacing: 0.05em; border-bottom: 2px solid #000; }}

        .nav-link {{ display: inline-block; padding: 0.5rem 1rem; border: 2px solid #000; text-transform: uppercase; font-size: 0.875rem; letter-spacing: 0.1em; font-family: 'JetBrains Mono', monospace; font-weight: 600; text-decoration: none; color: #000; transition: all 100ms; }}
        .nav-link:hover {{ background-color: #000; color: #fff; }}
        .doc-meta {{ font-family: "JetBrains Mono", monospace; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: #525252; margin-bottom: 2rem; display: flex; gap: 1.5rem; flex-wrap: wrap; }}
        .doc-meta-tag {{ background: #000; color: #fff; padding: 0.2rem 0.6rem; }}
    </style>
</head>
<body class="min-h-screen relative">
    <div class="texture-global"></div>
    <header class="border-b-[4px] border-black px-6 md:px-12 py-8 flex items-center justify-between">
        <a href="{root_path}index.html" class="text-3xl font-serif font-bold tracking-tighter uppercase shrink-0 mr-4 whitespace-nowrap">Research Archive</a>
        <nav class="flex gap-4 sm:flex-row flex-col flex-wrap justify-end">
            <a href="{root_path}index.html" class="nav-link whitespace-nowrap">Home</a>
            {breadcrumbs}
        </nav>
    </header>
    <main class="max-w-4xl mx-auto px-6 md:px-12 py-16 md:py-24">
        {doc_meta_html}
        <div class="md-content">
            {content}
        </div>
    </main>
    <footer class="border-t-[4px] border-black px-6 md:px-12 py-12 mt-24">
        <p class="text-sm font-mono tracking-widest uppercase">&copy; 2026 Archive. All rights reserved.</p>
    </footer>
</body>
</html>
"""

TEMPLATE_INDEX = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,800;1,400&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
    tailwind.config = {{
        theme: {{
            extend: {{
                fontFamily: {{
                    sans: ['"Source Serif 4"', 'Georgia', 'serif'],
                    serif: ['"Playfair Display"', 'Georgia', 'serif'],
                    mono: ['"JetBrains Mono"', 'monospace'],
                }},
                colors: {{
                    background: '#FFFFFF',
                    foreground: '#000000',
                    muted: '#F5F5F5',
                    mutedForeground: '#525252',
                    border: '#000000',
                    borderLight: '#E5E5E5',
                }}
            }}
        }}
    }}
    </script>
    <style>
        body {{ background-color: #FFFFFF; color: #000000; border-radius: 0 !important; }}
        * {{ border-radius: 0 !important; }}
        h1, h2, h3, h4, h5, h6 {{ font-family: "Playfair Display", Georgia, serif; letter-spacing: -0.025em; }}
        .texture-global {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
            opacity: 0.02;
        }}
        .search-input {{ width: 100%; border: 2px solid #000; padding: 1rem 1.5rem; font-size: 1.125rem; font-family: "Source Serif 4", serif; outline: none; transition: all 100ms; background: #fff; }}
        .search-input:focus {{ border-bottom: 4px solid #000; }}
        .search-input::placeholder {{ color: #525252; font-style: italic; }}

        /* Category filter pills */
        .filter-pills {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem; }}
        .pill {{
            display: inline-block; padding: 0.35rem 0.85rem;
            border: 2px solid #000; font-family: "JetBrains Mono", monospace;
            font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em;
            cursor: pointer; transition: all 100ms; background: #fff; color: #000; user-select: none;
        }}
        .pill:hover {{ background: #000; color: #fff; }}
        .pill.active {{ background: #000; color: #fff; }}

        .item-card-link {{ display: block; text-decoration: none; color: #000; background-color: #fff; transition: all 100ms; }}
        .item-card {{ padding: 1.5rem 2rem; border: 1px solid #000; margin-bottom: -1px; display: flex; flex-direction: column; gap: 0.25rem; }}
        .item-card-link:hover .item-card {{ background-color: #000; color: #fff; }}
        .item-card-link:hover .item-title {{ color: #fff; }}
        .item-card-link:hover .item-meta {{ opacity: 0.7; }}

        .item-title {{ font-family: "Playfair Display", Georgia, serif; font-size: 1.5rem; font-weight: 600; color: inherit; transition: color 100ms; }}
        .item-meta {{ font-family: "JetBrains Mono", monospace; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; opacity: 0.7; display: flex; gap: 1rem; flex-wrap: wrap; align-items: center; }}
        .item-category-badge {{ background: #000; color: #fff; padding: 0.1rem 0.5rem; font-size: 0.7rem; }}
        .item-card-link:hover .item-category-badge {{ background: #fff; color: #000; }}

        .dir-card {{ border-left: 4px solid #000; padding-left: 1.5rem; }}
        .dir-card-link:hover .dir-card {{ border-left-color: #fff; }}

        .nav-link {{ display: inline-block; padding: 0.5rem 1rem; border: 2px solid #000; text-transform: uppercase; font-size: 0.875rem; letter-spacing: 0.1em; font-family: 'JetBrains Mono', monospace; font-weight: 600; text-decoration: none; color: #000; transition: all 100ms; }}
        .nav-link:hover {{ background-color: #000; color: #fff; }}

        .hero-title {{
            font-size: clamp(3rem, 8vw, 6rem);
            line-height: 1;
            font-weight: 800;
        }}

        #no-results {{ display: none; padding: 3rem 0; font-family: "JetBrains Mono"; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.5; }}
    </style>
</head>
<body class="min-h-screen relative">
    <div class="texture-global"></div>
    <header class="border-b-[4px] border-black px-6 md:px-12 py-8 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div class="flex items-center gap-4">
            <div class="w-8 h-8 border-4 border-black shrink-0 md:block hidden"></div>
            <a href="{root_path}index.html" class="text-3xl font-serif font-bold tracking-tighter uppercase whitespace-nowrap">Research Archive</a>
        </div>
        <nav class="flex gap-4 sm:flex-row flex-col flex-wrap">
            <a href="{root_path}index.html" class="nav-link whitespace-nowrap">Home</a>
            {breadcrumbs}
        </nav>
    </header>
    <main class="max-w-6xl mx-auto px-6 md:px-12 py-16 md:py-24">

        <div class="mb-16">
            <h1 class="hero-title font-serif tracking-tighter uppercase mb-6">{dir_name}</h1>
            <div class="h-1 w-full bg-black"></div>
        </div>

        <!-- Search -->
        <div class="mb-8">
            <input type="text" id="search-input" class="search-input" placeholder="Search documents..." aria-label="Search">
        </div>

        <!-- Category filter pills -->
        {filter_pills_html}

        <div class="mt-12">
            <div class="flex items-center justify-between border-b-[4px] border-black pb-4 mb-8">
                <h2 class="text-2xl font-serif font-bold uppercase tracking-tighter">Documents</h2>
                <span class="font-mono text-sm tracking-widest uppercase" id="count-label">{item_count} items</span>
            </div>

            <div id="no-results">No documents match your filter.</div>

            <div class="flex flex-col" id="content-list">
                {items_html}
            </div>
        </div>
    </main>
    <footer class="border-t-[4px] border-black px-6 md:px-12 py-12 mt-24">
        <p class="text-sm font-mono tracking-widest uppercase">&copy; 2026 Archive. All rights reserved.</p>
    </footer>

    {filter_script}
</body>
</html>
"""

FILTER_SCRIPT_TEMPLATE = """
<script>
    // ── Data ──────────────────────────────────────────────────────────────
    let searchIndexData = {search_index_json};

    // ── State ─────────────────────────────────────────────────────────────
    let activeCategory = null;
    let searchQuery = '';

    // ── Elements ──────────────────────────────────────────────────────────
    const searchInput = document.getElementById('search-input');
    const contentList = document.getElementById('content-list');
    const countLabel = document.getElementById('count-label');
    const noResults = document.getElementById('no-results');
    const pills = document.querySelectorAll('.pill[data-category]');
    const allCards = contentList ? Array.from(contentList.querySelectorAll('.item-card-link[data-category]')) : [];
    const totalCount = allCards.length;

    function applyFilters() {{
        let visible = 0;
        allCards.forEach(card => {{
            const cat = card.dataset.category || '';
            const title = (card.dataset.title || '').toLowerCase();
            const tags = (card.dataset.tags || '').toLowerCase();
            const date = (card.dataset.date || '').toLowerCase();

            const catMatch = !activeCategory || cat === activeCategory;
            const searchMatch = !searchQuery ||
                title.includes(searchQuery) ||
                tags.includes(searchQuery) ||
                cat.toLowerCase().includes(searchQuery) ||
                date.includes(searchQuery);

            if (catMatch && searchMatch) {{
                card.style.display = '';
                visible++;
            }} else {{
                card.style.display = 'none';
            }}
        }});

        countLabel.textContent = visible + ' item' + (visible !== 1 ? 's' : '');
        noResults.style.display = visible === 0 ? 'block' : 'none';
    }}

    // ── Category pills ────────────────────────────────────────────────────
    pills.forEach(pill => {{
        pill.addEventListener('click', () => {{
            const cat = pill.dataset.category;
            if (activeCategory === cat) {{
                // toggle off
                activeCategory = null;
                pills.forEach(p => p.classList.remove('active'));
            }} else {{
                activeCategory = cat;
                pills.forEach(p => p.classList.remove('active'));
                pill.classList.add('active');
            }}
            applyFilters();
        }});
    }});

    // ── Search ────────────────────────────────────────────────────────────
    searchInput && searchInput.addEventListener('input', e => {{
        searchQuery = e.target.value.toLowerCase().trim();
        applyFilters();
    }});
</script>
"""

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def generate_breadcrumbs(rel_path, root_path):
    if not rel_path or rel_path == '.':
        return ""
    parts = rel_path.split(os.sep)
    crumbs = []
    for i, part in enumerate(parts):
        if not part: continue
        back_steps = len(parts) - 1 - i
        link = ("../" * back_steps) + "index.html"
        crumbs.append(f'<a href="{link}" class="nav-link">{part}</a>')
    return "\n".join(crumbs)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Research Archive Static Site Generator")
    parser.add_argument("--source", required=True, help="Source directory containing markdown files")
    parser.add_argument("--s3-bucket", required=False, help="S3 bucket path (e.g., s3://bucket/folder/)")
    parser.add_argument("--cloudfront-id", required=False, help="CloudFront Distribution ID for cache invalidation")
    args = parser.parse_args()

    source_dir = os.path.abspath(args.source)
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory {source_dir} does not exist.")
        sys.exit(1)

    build_dir = os.path.abspath("build_out")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)

    md = markdown.Markdown(extensions=['fenced_code', 'tables', 'sane_lists'])

    search_index = []

    for root, dirs, files in os.walk(source_dir):
        # Skip hidden dirs
        dirs[:] = [d for d in sorted(dirs) if not d.startswith('.')]

        rel_dir = os.path.relpath(root, source_dir)
        if rel_dir == '.':
            rel_dir = ''

        target_dir = os.path.join(build_dir, rel_dir)
        os.makedirs(target_dir, exist_ok=True)

        depth = len([p for p in rel_dir.split(os.sep) if p])
        root_path = "../" * depth if depth > 0 else "./"

        items_html = []
        all_categories = []  # collect categories at this level for filter pills

        # Directories first
        for d in sorted(dirs):
            items_html.append(f'''
            <a href="{d}/index.html" class="item-card-link dir-card-link">
                <div class="item-card dir-card">
                    <span class="item-meta">Directory</span>
                    <h3 class="item-title">{d}/</h3>
                </div>
            </a>
            ''')

        # Files
        count_files = len([f for f in files if f.endswith('.md')])
        for f in sorted(files):
            if not f.endswith('.md'):
                continue

            src_file = os.path.join(root, f)
            with open(src_file, 'r', encoding='utf-8') as fh:
                raw_content = fh.read()

            # Parse frontmatter
            meta, body = parse_frontmatter(raw_content)

            # Resolve title: prefer frontmatter, fall back to H1 (stripped)
            fm_title = meta.get('title', '')
            h1_title = extract_h1_title(body)
            display_title = fm_title if fm_title else clean_title(h1_title)
            # Also strip from H1 for frontmatter-less docs
            if not fm_title:
                display_title = clean_title(h1_title)

            # Date: prefer frontmatter, fall back to filename
            fm_date = meta.get('date', '')
            filename_date = parse_date_from_filename(f)
            raw_date = str(fm_date) if fm_date else (filename_date or '')
            formatted_date = format_date(raw_date)

            # Category & tags
            category = meta.get('category', '')
            tags = meta.get('tags', [])
            if isinstance(tags, list):
                tags_str = ', '.join(str(t) for t in tags)
            else:
                tags_str = str(tags)

            if category:
                all_categories.append(category)

            # Render markdown body (without frontmatter)
            md.reset()
            html_content = md.convert(body)

            # Build document meta bar for article page
            meta_parts = []
            if formatted_date:
                meta_parts.append(f'<span>{formatted_date}</span>')
            if category:
                meta_parts.append(f'<span class="item-category-badge">{category}</span>')
            if tags_str:
                meta_parts.append(f'<span>{tags_str}</span>')
            doc_meta_html = f'<div class="doc-meta">{"".join(meta_parts)}</div>' if meta_parts else ''

            # Write page HTML
            base_name = os.path.splitext(f)[0]
            page_rel_path = f"{base_name}.html"
            page_target = os.path.join(target_dir, page_rel_path)

            page_html = TEMPLATE_PAGE.format(
                title=display_title,
                content=html_content,
                root_path=root_path,
                breadcrumbs=generate_breadcrumbs(rel_dir, root_path),
                doc_meta_html=doc_meta_html,
            )

            with open(page_target, 'w', encoding='utf-8') as pf:
                pf.write(page_html)

            # Add to index list (data attrs for JS filtering)
            cat_attr = category.replace('"', '&quot;')
            title_attr = display_title.replace('"', '&quot;')
            tags_attr = tags_str.replace('"', '&quot;')
            date_attr = (formatted_date or raw_date).replace('"', '&quot;')

            items_html.append(f'''
            <a href="{page_rel_path}" class="item-card-link"
               data-category="{cat_attr}"
               data-title="{title_attr}"
               data-tags="{tags_attr}"
               data-date="{date_attr}">
                <div class="item-card">
                    <div class="item-meta">
                        {f'<span class="item-category-badge">{category}</span>' if category else ''}
                        {f'<span>{formatted_date}</span>' if formatted_date else ''}
                    </div>
                    <h3 class="item-title">{display_title}</h3>
                </div>
            </a>
            ''')

            # Add to global search index
            search_index.append({
                "title": display_title,
                "path": os.path.join(rel_dir, page_rel_path).replace("\\", "/"),
                "category": category,
                "tags": tags_str,
                "date": formatted_date,
                "raw_date": raw_date,
                "content": body[:500],
            })

        # Build filter pills from unique sorted categories at this level
        unique_cats = sorted(set(all_categories))
        if unique_cats:
            pills_html = '<div class="filter-pills">\n'
            for cat in unique_cats:
                pills_html += f'  <button class="pill" data-category="{cat}">{cat}</button>\n'
            pills_html += '</div>\n'
        else:
            pills_html = ''

        # Build index.html
        dir_name = os.path.basename(root) if rel_dir else "Research Archive"

        filter_script = FILTER_SCRIPT_TEMPLATE.format(
            search_index_json=json.dumps(search_index)
        )

        index_html = TEMPLATE_INDEX.format(
            title=f"Research Archive — {dir_name}" if rel_dir else "Research Archive",
            dir_name=dir_name,
            root_path=root_path,
            breadcrumbs=generate_breadcrumbs(rel_dir, root_path),
            items_html="\n".join(items_html),
            item_count=len(dirs) + count_files,
            filter_pills_html=pills_html,
            filter_script=filter_script,
        )

        with open(os.path.join(target_dir, "index.html"), 'w', encoding='utf-8') as idxf:
            idxf.write(index_html)

    # Write global search index
    with open(os.path.join(build_dir, "search_index.json"), "w", encoding="utf-8") as f:
        json.dump(search_index, f)

    print(f"Successfully built static site in {build_dir}")

    if args.s3_bucket:
        bucket = args.s3_bucket.rstrip('/') + '/'
        print(f"\nDeploying to {bucket} ...")
        cmd = ["aws", "s3", "sync", build_dir, bucket, "--delete"]
        try:
            subprocess.run(cmd, check=True)
            print("Successfully deployed to S3.")

            if args.cloudfront_id:
                print(f"Invalidating CloudFront cache for {args.cloudfront_id} ...")
                cf_cmd = [
                    "aws", "cloudfront", "create-invalidation",
                    "--distribution-id", args.cloudfront_id,
                    "--paths", "/*"
                ]
                subprocess.run(cf_cmd, check=True)
                print("CloudFront invalidation requested.")

            # Git auto-commit
            print("Committing and pushing changes to git...")
            repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            site_dir = "sites/research_archive/"
            today = datetime.now().strftime("%B %-d, %Y")
            subprocess.run(["git", "add", site_dir], cwd=repo_root, check=True)
            status = subprocess.run(
                ["git", "status", "--porcelain", site_dir],
                cwd=repo_root, capture_output=True, text=True
            )
            if status.stdout.strip():
                subprocess.run(
                    ["git", "commit", "-m", f"Update research archive — {today}"],
                    cwd=repo_root, check=True
                )
                subprocess.run(["git", "push"], cwd=repo_root, check=True)
                print("Git commit and push successful.")
            else:
                print("No new changes to commit.")

        except subprocess.CalledProcessError as e:
            print(f"Error deploying: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
