#!/usr/bin/env python3
"""
build_prayer.py — Static site generator for Daily Christian Meditations.
"""

import os
import glob
import subprocess
import re
import shutil

SRC_DIR = "/Users/chris/code/gemini/sites/prayer/src"
OUTPUT_DIR = "/Users/chris/code/gemini/sites/prayer/output"
S3_BUCKET = "s3://gemini-designs-portfolio-2026-v2/prayer/"
PROFILE = "default"

os.makedirs(SRC_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title} | CBMO Network</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Lora:ital,wght@0,400;0,500;1,400&family=Playfair+Display:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="prayer.css">
</head>
<body>
    <div class="wrapper">
        <header>
            <h1>Daily Christian Meditation</h1>
            <div class="subtitle">Scripture, Context, and Empathetic Reflection</div>
        </header>
        
        <div class="content-layout">
            <aside class="sidebar">
                <nav class="side-nav">
                    <a href="index.html">Daily Meditations</a>
                    <a href="happy.html">✨ Happy Stuff ✨</a>
                    <a href="about.html">About</a>
                    <a href="donate.html">Support</a>
                    <a href="resources.html">Resources</a>
                    <a href="submit.html">Submit Prayer</a>
                </nav>
            </aside>
            <main>
                {content}
            </main>
        </div>
        
        <footer>
            <p>Generated for CBMO Network &middot; Peace be with you.</p>
        </footer>
    </div>
</body>
</html>
"""

def main():
    print("Building Prayer Site...")
    # Copy CSS
    shutil.copy2(os.path.join(SRC_DIR, "prayer.css"), os.path.join(OUTPUT_DIR, "prayer.css"))
    
    # Process files
    files = glob.glob(os.path.join(SRC_DIR, "*.html"))
    files.sort(reverse=True)

    content_html = ""
    happy_content_html = ""
    meditation_count = 0
    static_count = 0
    
    for filepath in files:
        filename = os.path.basename(filepath)
        
        with open(filepath, "r") as f:
            html_body = f.read()

        title_match = re.search(r'<meta name="title" content="(.*?)">', html_body)
        title = title_match.group(1) if title_match else "Daily Meditation"
        
        cat_match = re.search(r'<meta name="category" content="(.*?)">', html_body, re.IGNORECASE)
        category = cat_match.group(1).lower() if cat_match else ""

        # Remove metadata tag block to clean the output
        html_body = re.sub(r'<div class="metadata".*?</div>', '', html_body, flags=re.DOTALL)

        if not re.match(r"\d{4}-\d{2}-\d{2}", filename):
            # It's a static page
            static_count += 1
            page_content = TEMPLATE.replace("{page_title}", title).replace("{content}", html_body)
            with open(os.path.join(OUTPUT_DIR, filename), "w") as f:
                f.write(page_content)
            continue
            
        # It's a meditation
        meditation_count += 1
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", filename)
        date_str = date_match.group(1)

        article_block = f"""
        <article>
            <div class="date-badge">{date_str}</div>
            <h2 class="article-title">{title}</h2>
            {html_body}
        </article>
        """
        content_html += article_block
        
        if category in ["happy", "positive"]:
            happy_content_html += article_block

    if meditation_count == 0:
        content_html = "<article><p>No meditations yet. Check back soon.</p></article>"
    if not happy_content_html:
        happy_content_html = "<article><p>No specifically happy meditations found yet, but joy is everywhere. Check back soon.</p></article>"

    # Write index.html
    index_page = TEMPLATE.replace("{page_title}", "Home").replace("{content}", content_html)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
        f.write(index_page)
        
    # Write happy.html
    happy_page = TEMPLATE.replace("{page_title}", "Happy Stuff").replace("{content}", happy_content_html)
    with open(os.path.join(OUTPUT_DIR, "happy.html"), "w") as f:
        f.write(happy_page)

    print(f"Generated index.html, happy.html, and {static_count} static pages. Found {meditation_count} meditations.")
    
    # Sync to S3
    print("Syncing to S3...")
    cmd = ["aws", "s3", "sync", OUTPUT_DIR, S3_BUCKET, "--profile", PROFILE, "--delete"]
    subprocess.run(cmd, check=True)
    print("Site Published Successfully!")

if __name__ == "__main__":
    main()
