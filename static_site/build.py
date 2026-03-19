import os
import sys
import shutil
import argparse
import subprocess
import json
import re
import markdown

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
        /* tables */
        .md-content table {{ width: 100%; border-collapse: collapse; margin-bottom: 2rem; }}
        .md-content th, .md-content td {{ border: 1px solid #000; padding: 0.75rem; text-align: left; font-family: "Source Serif 4"; }}
        .md-content th {{ font-weight: 600; text-transform: uppercase; font-family: "JetBrains Mono"; font-size: 0.875rem; letter-spacing: 0.05em; border-bottom: 2px solid #000; }}

        .nav-link {{ display: inline-block; padding: 0.5rem 1rem; border: 2px solid #000; text-transform: uppercase; font-size: 0.875rem; letter-spacing: 0.1em; font-family: 'JetBrains Mono', monospace; font-weight: 600; text-decoration: none; color: #000; transition: all 100ms; }}
        .nav-link:hover {{ background-color: #000; color: #fff; }}
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
        .search-input {{ width: 100%; border: 2px solid #000; border-bottom: 2px solid #000; padding: 1rem 1.5rem; font-size: 1.25rem; font-family: "Source Serif 4", serif; outline: none; transition: all 100ms; background: #fff; }}
        .search-input:focus {{ border-bottom: 4px solid #000; }}
        .search-input::placeholder {{ color: #525252; font-style: italic; }}
        
        .item-card-link {{ display: block; text-decoration: none; color: #000; background-color: #fff; transition: all 100ms; }}
        .item-card {{ padding: 2rem; border: 1px solid #000; margin-bottom: -1px; display: flex; flex-direction: column; }}
        .item-card-link:hover .item-card {{ background-color: #000; color: #fff; }}
        .item-card-link:hover .item-title {{ color: #fff; }}
        
        .item-title {{ font-family: "Playfair Display", Georgia, serif; font-size: 1.75rem; font-weight: 600; margin-bottom: 0.5rem; color: inherit; transition: color 100ms; }}
        .item-meta {{ font-family: "JetBrains Mono", monospace; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.8; }}
        
        .dir-card {{ border-left: 4px solid #000; padding-left: 1.5rem; }}
        .dir-card-link:hover .dir-card {{ border-left-color: #fff; }}

        .nav-link {{ display: inline-block; padding: 0.5rem 1rem; border: 2px solid #000; text-transform: uppercase; font-size: 0.875rem; letter-spacing: 0.1em; font-family: 'JetBrains Mono', monospace; font-weight: 600; text-decoration: none; color: #000; transition: all 100ms; }}
        .nav-link:hover {{ background-color: #000; color: #fff; }}
        
        .hero-title {{
            font-size: clamp(3rem, 8vw, 6rem);
            line-height: 1;
            font-weight: 800;
        }}
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
        
        <div class="mb-20">
            <h1 class="hero-title font-serif tracking-tighter uppercase mb-6">{dir_name}</h1>
            <div class="h-1 w-full bg-black"></div>
        </div>

        {search_html}

        <div class="mt-16">
            <div class="flex items-center justify-between border-b-[4px] border-black pb-4 mb-8">
                <h2 class="text-2xl font-serif font-bold uppercase tracking-tighter">Directory Contents</h2>
                <span class="font-mono text-sm tracking-widest uppercase">{item_count} items</span>
            </div>
            
            <div class="flex flex-col" id="content-list">
                {items_html}
            </div>
        </div>
    </main>
    <footer class="border-t-[4px] border-black px-6 md:px-12 py-12 mt-24">
        <p class="text-sm font-mono tracking-widest uppercase">&copy; 2026 Archive. All rights reserved.</p>
    </footer>

    {search_script}
</body>
</html>
"""

def extract_title(markdown_content):
    match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "Untitled Document"

def generate_breadcrumbs(rel_path, root_path):
    if not rel_path or rel_path == '.':
        return ""
    parts = rel_path.split(os.sep)
    crumbs = []
    current_path = ""
    for i, part in enumerate(parts):
        if not part: continue
        current_path = os.path.join(current_path, part)
        back_steps = len(parts) - 1 - i
        link = ("../" * back_steps) + "index.html"
        crumbs.append(f'<a href="{link}" class="nav-link">{part}</a>')
    return "\n".join(crumbs)

def main():
    parser = argparse.ArgumentParser(description="Static Site Generator")
    parser.add_argument("--source", required=True, help="Source directory containing markdown files")
    parser.add_argument("--s3-bucket", required=False, help="S3 bucket path (e.g., s3://bucket/folder/)")
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
        rel_dir = os.path.relpath(root, source_dir)
        if rel_dir == '.':
            rel_dir = ''
        
        target_dir = os.path.join(build_dir, rel_dir)
        os.makedirs(target_dir, exist_ok=True)
        
        depth = len([p for p in rel_dir.split(os.sep) if p])
        root_path = "../" * depth if depth > 0 else "./"
        
        # We need an index.html at each level
        items_html = []
        
        # Directories first
        for d in sorted(dirs):
            items_html.append(f'''
            <a href="{d}/index.html" class="item-card-link dir-card-link">
                <div class="item-card dir-card">
                    <span class="item-meta mb-2">Directory</span>
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
            with open(src_file, 'r', encoding='utf-8') as file:
                content = file.read()
                
            title = extract_title(content)
            html_content = md.convert(content)
            
            # Write page html
            base_name = os.path.splitext(f)[0]
            page_rel_path = f"{base_name}.html"
            page_target = os.path.join(target_dir, page_rel_path)
            
            page_html = TEMPLATE_PAGE.format(
                title=title,
                content=html_content,
                root_path=root_path,
                breadcrumbs=generate_breadcrumbs(rel_dir, root_path)
            )
            
            with open(page_target, 'w', encoding='utf-8') as pf:
                pf.write(page_html)
                
            # Add to level index
            items_html.append(f'''
            <a href="{page_rel_path}" class="item-card-link">
                <div class="item-card">
                    <span class="item-meta mb-2">Document</span>
                    <h3 class="item-title">{title}</h3>
                </div>
            </a>
            ''')
            
            # Add to global search index
            search_index.append({
                "title": title,
                "path": os.path.join(rel_dir, page_rel_path).replace("\\\\", "/"),
                "content": content[:1000] # store some snippet for search (or just title for simplicity, doing simple match)
            })
            
        # Generate index.html for this dir
        dir_name = os.path.basename(root) if rel_dir else "Archive Root"
        
        search_html = f'''
        <div class="mb-12">
            <input type="text" id="search-input" class="search-input" placeholder="Search across all documents..." aria-label="Search">
            <div id="search-results" class="hidden flex flex-col mt-4 border-l-[4px] border-black pl-4 gap-2"></div>
        </div>
        '''
        
        search_script = f'''
        <script>
            let indexData = [];
            fetch('{root_path}search_index.json')
                .then(res => res.json())
                .then(data => indexData = data)
                .catch(err => console.error("Error loading search index", err));
            
            const searchInput = document.getElementById('search-input');
            const searchResults = document.getElementById('search-results');
            const contentList = document.getElementById('content-list');
            
            if (searchInput) {{
                searchInput.addEventListener('input', (e) => {{
                    const query = e.target.value.toLowerCase().trim();
                    if (!query) {{
                        searchResults.classList.add('hidden');
                        searchResults.innerHTML = '';
                        if (contentList) contentList.style.display = 'flex';
                        return;
                    }}
                    
                    if (contentList) contentList.style.display = 'none';
                    searchResults.classList.remove('hidden');
                    
                    const matches = indexData.filter(item => 
                        item.title.toLowerCase().includes(query) || 
                        item.content.toLowerCase().includes(query)
                    );
                    
                    if (matches.length === 0) {{
                        searchResults.innerHTML = '<p class="font-mono text-sm tracking-widest uppercase py-4">No results found.</p>';
                    }} else {{
                        searchResults.innerHTML = matches.map(match => `
                            <a href="{root_path}${{match.path}}" class="item-card-link border border-black p-4 block hover:bg-black hover:text-white transition-colors">
                                <h4 class="font-serif text-xl font-bold">${{match.title}}</h4>
                                <span class="font-mono text-xs uppercase tracking-widest opacity-80 mt-2 block">${{match.path}}</span>
                            </a>
                        `).join('');
                    }}
                }});
            }}
        </script>
        '''
        
        index_html = TEMPLATE_INDEX.format(
            title=f"Index of {dir_name}",
            dir_name=dir_name,
            root_path=root_path,
            breadcrumbs=generate_breadcrumbs(rel_dir, root_path),
            items_html="\n".join(items_html),
            item_count=len(dirs) + count_files,
            search_html=search_html,
            search_script=search_script
        )
        
        with open(os.path.join(target_dir, "index.html"), 'w', encoding='utf-8') as idxf:
            idxf.write(index_html)
            
    # Write search index
    with open(os.path.join(build_dir, "search_index.json"), "w", encoding="utf-8") as f:
        json.dump(search_index, f)
        
    print(f"Successfully built static site in {build_dir}")

    if args.s3_bucket:
        print(f"Deploying to S3: {args.s3_bucket}")
        # Run aws s3 sync
        cmd = ["aws", "s3", "sync", build_dir, args.s3_bucket, "--delete"]
        try:
            subprocess.run(cmd, check=True)
            print("Successfully deployed to S3.")
        except subprocess.CalledProcessError as e:
            print(f"Error deploying to S3: {e}")
            sys.exit(1)
            
if __name__ == "__main__":
    main()
