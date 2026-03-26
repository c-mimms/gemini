#!/usr/bin/env python3
"""
build_birthday.py — Editorial Site Builder for Birthday Planning.

Generates separate tabbed pages (activities.html, gifts.html) using a JS-powered tab layout.
"""

import os
import glob
import subprocess
import re
import shutil
import argparse
from datetime import datetime
from collections import defaultdict

SITE_DIR   = os.path.dirname(os.path.abspath(__file__))
SRC_DIR    = os.path.join(SITE_DIR, "src")
OUTPUT_DIR = os.path.join(SITE_DIR, "output")
CSS_FILE   = os.path.join(SITE_DIR, "birthday.css")
PROFILE    = "default"

os.makedirs(OUTPUT_DIR, exist_ok=True)

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title} | Birthday Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="birthday.css">
    <style>
        .nav-link.active {{ font-weight: 600; border-bottom: 1px solid var(--color-accent); }}
    </style>
</head>
<body>
    <header class="section-wrapped">
        <div class="header-flex">
            <div>
                <span class="uppercase-label">April 12 Planning</span>
                <h3 style="font-family: var(--font-serif);"><a href="index.html" style="text-decoration: none; color: inherit;">Dashboard</a></h3>
            </div>
            <nav>
                <a href="activities.html" class="nav-link {nav_act}">Activities</a>
                <a href="gifts.html" class="nav-link {nav_gift}">Gifts</a>
            </nav>
        </div>
    </header>

    <main class="section-wrapped">
        {content}
    </main>

    <footer class="section-wrapped" style="padding: var(--spacing-lg) 0; border-top: 1px solid var(--color-border); margin-top: var(--spacing-xl);">
        <p class="text-muted" style="font-size: 0.8rem;">Curated for Chris’s Wife · Last update {build_date}</p>
    </footer>

    <script>
        // Simple Vanilla JS Tab Viewer
        function openTab(evt, tabName) {{
            var i, tabContent, tabButtons;
            tabContent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabContent.length; i++) {{
                tabContent[i].style.display = "none";
                tabContent[i].className = tabContent[i].className.replace(" active", "");
            }}
            tabButtons = document.getElementsByClassName("tab-button");
            for (i = 0; i < tabButtons.length; i++) {{
                tabButtons[i].className = tabButtons[i].className.replace(" active", "");
            }}
            document.getElementById(tabName).style.display = "block";
            document.getElementById(tabName).className += " active";
            evt.currentTarget.className += " active";
        }}
    </script>
</body>
</html>
"""

def extract_meta(html: str, name: str, fallback: str = "") -> str:
    pattern = r'<meta\s+name=["\']' + re.escape(name) + r'["\'][^>]+content=["\']([^"\']+)["\']'
    m = re.search(pattern, html, re.IGNORECASE)
    if m: return m.group(1)
    pattern_rev = r'<meta\s+content=["\']([^"\']+)["\']\s+name=["\']' + re.escape(name) + r'["\']'
    m = re.search(pattern_rev, html, re.IGNORECASE)
    return m.group(1) if m else fallback

def get_component_html(filepath):
    with open(filepath) as f:
        html = f.read()
    clean_html = re.sub(r'<meta[^>]+>', '', html)
    clean_html = re.sub(r'<div class="premium-card">', '<div class="editorial-item">', clean_html)
    clean_html = re.sub(r'class="venue-card[^"]*"', 'class="editorial-item"', clean_html)
    
    title = extract_meta(html, "title", "Untitled")
    tag = extract_meta(html, "tag", "General")
    # try to hit concept-tag if tag missing in meta
    if tag == "General":
        ctm = re.search(r'<span class="concept-tag[^"]*">([^<]+)</span>', html)
        if ctm: tag = ctm.group(1)

    return {
        "content": clean_html.strip(),
        "title": title,
        "tag": tag.split("|")[0].strip(),
        "filename": os.path.basename(filepath)
    }

def build_tabbed_page(title, items, nav_act, nav_gift, build_date):
    # Group items by tag
    groups = defaultdict(list)
    for item in items:
        groups[item['tag']].append(item['content'])
    
    # Generate Tabs UI
    if not items:
        content_html = "<p class='text-muted'>No items processed yet.</p>"
    else:
        tags = sorted(list(groups.keys()))
        tabs_nav = "<div class='tabs-container'>"
        tabs_content = ""
        
        for i, tag in enumerate(tags):
            tag_id = "tab_" + re.sub(r'\W+', '', tag.lower())
            active_class = "active" if i == 0 else ""
            
            tabs_nav += f'<button class="tab-button {active_class}" onclick="openTab(event, \'{tag_id}\')">{tag}</button>\n'
            
            display_style = "block" if i == 0 else "none"
            tabs_content += f'<div id="{tag_id}" class="tab-content {active_class}" style="display:{display_style};">\n'
            tabs_content += '<div class="content-wrapped">\n'
            for html_str in groups[tag]:
                tabs_content += html_str + "\n"
            tabs_content += '</div></div>\n'
            
        tabs_nav += "</div>\n"
        content_html = f"<h1>{title}</h1>\n" + tabs_nav + tabs_content

    return TEMPLATE.format(page_title=title, content=content_html, build_date=build_date, nav_act=nav_act, nav_gift=nav_gift)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--s3-bucket", help="S3 bucket URI")
    parser.add_argument("--cloudfront-id", help="CloudFront ID")
    args = parser.parse_args()

    build_date = datetime.now().strftime("%B %d, %Y")
    
    # 1. Copy Assets
    if os.path.exists(CSS_FILE):
        shutil.copy2(CSS_FILE, os.path.join(OUTPUT_DIR, "birthday.css"))
    
    img_src = os.path.join(SITE_DIR, "data", "images")
    if os.path.exists(img_src):
        img_dest = os.path.join(OUTPUT_DIR, "data", "images")
        os.makedirs(img_dest, exist_ok=True)
        for img in glob.glob(os.path.join(img_src, "*")):
            shutil.copy2(img, img_dest)

    # 2. Gather Components
    activities_dir = os.path.join(SRC_DIR, "activities")
    gifts_dir = os.path.join(SRC_DIR, "gifts")
    
    activities = [get_component_html(f) for f in glob.glob(os.path.join(activities_dir, "*.html"))]
    gifts = [get_component_html(f) for f in glob.glob(os.path.join(gifts_dir, "*.html"))]

    # 3. Assemble Pages
    index_content = """
    <div class="content-wrapped" style="text-align: center; margin-top: var(--spacing-xl);">
        <span class="uppercase-label">April 12th</span>
        <h1 style="margin-top: var(--spacing-lg); font-size: 4rem;">The Collection.</h1>
        <p class="text-muted" style="font-size: 1.2rem; max-width: 600px; margin: var(--spacing-md) auto var(--spacing-xl);">A curated dashboard of distinct aesthetics, day-trips, and luxury sentiments for her birthday.</p>
        <div style="display: flex; justify-content: center; gap: var(--spacing-md);">
            <a href="activities.html" style="font-size: 1.1rem; border-bottom: 1px solid var(--color-accent); padding-bottom: 2px;">View Day-Of Plans</a>
            <span class="text-muted">·</span>
            <a href="gifts.html" style="font-size: 1.1rem; border-bottom: 1px solid var(--color-accent); padding-bottom: 2px;">View Gift Concepts</a>
        </div>
    </div>
    """
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
        f.write(TEMPLATE.format(page_title="Dashboard", content=index_content, build_date=build_date, nav_act="", nav_gift=""))

    act_page = build_tabbed_page("Activities", activities, nav_act="active", nav_gift="", build_date=build_date)
    with open(os.path.join(OUTPUT_DIR, "activities.html"), "w") as f:
        f.write(act_page)

    gift_page = build_tabbed_page("Gifts", gifts, nav_act="", nav_gift="active", build_date=build_date)
    with open(os.path.join(OUTPUT_DIR, "gifts.html"), "w") as f:
        f.write(gift_page)

    print("Success: Generated index.html, activities.html, gifts.html")

    # 4. Deployment & Git
    if args.s3_bucket:
        subprocess.run(["aws", "s3", "sync", OUTPUT_DIR, args.s3_bucket, "--profile", PROFILE, "--delete"], check=True)
        if args.cloudfront_id:
            subprocess.run(["aws", "cloudfront", "create-invalidation", "--distribution-id", args.cloudfront_id, "--paths", "/*"], check=True)

    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    subprocess.run(["git", "add", "sites/birthday/"], cwd=repo_root, check=True)
    status = subprocess.run(["git", "status", "--porcelain", "sites/birthday/"], cwd=repo_root, capture_output=True, text=True)
    if status.stdout.strip():
        subprocess.run(["git", "commit", "-m", "fix: separate activity/gift pages and robust image fetching"], cwd=repo_root, check=True)
        subprocess.run(["git", "push"], cwd=repo_root, check=True)

if __name__ == "__main__":
    main()
