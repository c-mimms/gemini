#!/usr/bin/env python3
"""
build_prayer.py — Static site generator for Daily Christian Meditations.

Usage:
    python3 build_prayer.py
"""

import os
import glob
import subprocess
import re
from datetime import datetime

SRC_DIR = "/Users/chris/code/gemini/sites/prayer/src"
OUTPUT_DIR = "/Users/chris/code/gemini/sites/prayer/output"
S3_BUCKET = "s3://gemini-designs-portfolio-2026-v2/prayer/"
PROFILE = "AdministratorAccess-302205098862"

os.makedirs(SRC_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Christian Meditation | CBMO Network</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Lora:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #faf9f6;
            --text-main: #2b2c28;
            --text-muted: #6b705c;
            --accent: #546a7b;
            --container-bg: #ffffff;
            --border-light: rgba(0,0,0,0.06);
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: 'Lora', serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.8;
            padding: 2rem 1rem;
            -webkit-font-smoothing: antialiased;
        }}

        .wrapper {{
            max-width: 720px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            margin-bottom: 4rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid var(--border-light);
        }}

        h1 {{
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text-main);
            letter-spacing: -0.02em;
        }}

        .subtitle {{
            font-size: 1rem;
            color: var(--text-muted);
            font-style: italic;
            letter-spacing: 0.05em;
        }}

        article {{
            background: var(--container-bg);
            padding: 3rem;
            border-radius: 4px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.03);
            margin-bottom: 3rem;
        }}

        .date-badge {{
            display: inline-block;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--accent);
            margin-bottom: 1.5rem;
            font-weight: 500;
            border-bottom: 1px solid var(--accent);
            padding-bottom: 0.25rem;
        }}

        .article-title {{
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            margin-bottom: 2rem;
            line-height: 1.3;
        }}

        .verse-block {{
            background: rgba(84, 106, 123, 0.04);
            border-left: 3px solid var(--accent);
            padding: 1.5rem 2rem;
            margin-bottom: 2rem;
            font-style: italic;
            font-size: 1.15rem;
            color: var(--text-main);
        }}

        .verse-ref {{
            display: block;
            margin-top: 0.75rem;
            font-size: 0.9rem;
            font-style: normal;
            font-weight: 600;
            text-align: right;
            color: var(--accent);
        }}

        .world-context {{
            font-size: 1.05rem;
            color: var(--text-muted);
            margin-bottom: 2rem;
        }}

        .world-context p {{ margin-bottom: 1rem; }}

        .meditation-core {{
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }}

        .meditation-core p {{ margin-bottom: 1.5rem; }}

        .prayer-close {{
            font-style: italic;
            color: var(--accent);
            margin-top: 2rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border-light);
            text-align: center;
        }}

        footer {{
            text-align: center;
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-top: 4rem;
            padding-top: 2rem;
        }}

        @media (max-width: 600px) {{
            article {{ padding: 2rem 1.5rem; }}
        }}
    </style>
</head>
<body>
    <div class="wrapper">
        <header>
            <h1>Daily Christian Meditation</h1>
            <div class="subtitle">Scripture, World Context, and Empathetic Reflection</div>
        </header>
        
        <main>
            {content}
        </main>
        
        <footer>
            <p>Generated for CBMO Network &middot; Peace be with you.</p>
        </footer>
    </div>
</body>
</html>
"""

def main():
    print("Building Prayer Site...")
    # Find all articles
    files = glob.glob(os.path.join(SRC_DIR, "*.html"))
    files.sort(reverse=True) # newest first

    content_html = ""
    if not files:
        content_html = "<article><p>No meditations yet. Check back soon.</p></article>"
    else:
        for filepath in files:
            filename = os.path.basename(filepath)
            # Try to grab date YYYY-MM-DD
            date_match = re.search(r"(\d{4}-\d{2}-\d{2})", filename)
            date_str = date_match.group(1) if date_match else "Unknown Date"
            
            with open(filepath, "r") as f:
                html_body = f.read()

            title_match = re.search(r'<meta name="title" content="(.*?)">', html_body)
            title = title_match.group(1) if title_match else "Daily Meditation"

            article_block = f"""
            <article>
                <div class="date-badge">{date_str}</div>
                <h2 class="article-title">{title}</h2>
                {html_body}
            </article>
            """
            content_html += article_block

    final_html = TEMPLATE.replace("{content}", content_html)
    
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
        f.write(final_html)

    print(f"Generated index.html with {len(files)} meditations.")
    
    # Sync to S3
    print("Syncing to S3...")
    cmd = ["aws", "s3", "sync", OUTPUT_DIR, S3_BUCKET, "--profile", PROFILE, "--delete"]
    subprocess.run(cmd, check=True)
    print("Site Published Successfully!")

if __name__ == "__main__":
    main()
