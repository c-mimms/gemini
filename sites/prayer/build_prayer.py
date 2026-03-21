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
PROFILE = "AdministratorAccess-302205098862"

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
            <nav class="nav-links">
                <a href="index.html">Daily Meditations</a>
                <a href="about.html">About</a>
                <a href="donate.html">Support</a>
            </nav>
            <h1>Daily Christian Meditation</h1>
            <div class="subtitle">Scripture, Context, and Empathetic Reflection</div>
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

ABOUT_HTML = """
<article class="static-page">
    <h2 class="article-title">About Our Mission</h2>
    <div class="static-page-content">
        <p>In a world increasingly driven by outrage, rapid news cycles, and partisan division, this daily meditation is offered as a quiet sanctuary. We seek to spread good news daily, and help heal the world through empathetic reflection.</p>
        <p>Every morning, these readings draw upon the ancient, enduring wisdom of Scripture and place it in dialogue with the very real, often painful events unfolding around the globe today.</p>
        <p>We do not take political sides. We simply sit with the text, sit with the news, and invite God's peace and restorative justice into our shared human experience. Our daily reflections act as "mini-sermons" guiding you towards peace before a busy day.</p>
    </div>
</article>
"""

DONATE_HTML = """
<article class="static-page">
    <h2 class="article-title">Support This Ministry</h2>
    <div class="static-page-content">
        <p>If these daily meditations have brought you a sense of grounding, peace, or clarity, please consider supporting the infrastructure that keeps this site running.</p>
        <p>Your contributions go directly toward covering global server distributions, domain upkeep, and the scheduled generation engines that ensure a new prayer is waiting for you every sunrise.</p>
        <div style="text-align: center; margin-top: 3rem;">
            <a href="#" class="donate-btn">Donate via PayPal</a>
        </div>
    </div>
</article>
"""

def main():
    print("Building Prayer Site...")
    # Copy CSS
    shutil.copy2(os.path.join(SRC_DIR, "prayer.css"), os.path.join(OUTPUT_DIR, "prayer.css"))
    
    # Process dynamic meditations
    files = glob.glob(os.path.join(SRC_DIR, "*.html"))
    files.sort(reverse=True)

    content_html = ""
    meditation_count = 0
    for filepath in files:
        filename = os.path.basename(filepath)
        # Skip static ones if they sneak in
        if not re.match(r"\d{4}-\d{2}-\d{2}", filename):
            continue
            
        meditation_count += 1
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", filename)
        date_str = date_match.group(1)
        
        with open(filepath, "r") as f:
            html_body = f.read()

        title_match = re.search(r'<meta name="title" content="(.*?)">', html_body)
        title = title_match.group(1) if title_match else "Daily Meditation"
        
        # Remove metadata tag block to clean the output
        html_body = re.sub(r'<div class="metadata".*?</div>', '', html_body, flags=re.DOTALL)

        article_block = f"""
        <article>
            <div class="date-badge">{date_str}</div>
            <h2 class="article-title">{title}</h2>
            {html_body}
        </article>
        """
        content_html += article_block

    if meditation_count == 0:
        content_html = "<article><p>No meditations yet. Check back soon.</p></article>"

    # Write index.html
    index_page = TEMPLATE.replace("{page_title}", "Home").replace("{content}", content_html)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
        f.write(index_page)
        
    # Write about.html
    about_page = TEMPLATE.replace("{page_title}", "About").replace("{content}", ABOUT_HTML)
    with open(os.path.join(OUTPUT_DIR, "about.html"), "w") as f:
        f.write(about_page)

    # Write donate.html
    donate_page = TEMPLATE.replace("{page_title}", "Support").replace("{content}", DONATE_HTML)
    with open(os.path.join(OUTPUT_DIR, "donate.html"), "w") as f:
        f.write(donate_page)

    print(f"Generated index.html, about.html, donate.html. Found {meditation_count} meditations.")
    
    # Sync to S3
    print("Syncing to S3...")
    cmd = ["aws", "s3", "sync", OUTPUT_DIR, S3_BUCKET, "--profile", PROFILE, "--delete"]
    subprocess.run(cmd, check=True)
    print("Site Published Successfully!")

if __name__ == "__main__":
    main()
