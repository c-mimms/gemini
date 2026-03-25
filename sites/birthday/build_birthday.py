#!/usr/bin/env python3
"""
build_birthday.py — Editorial Site Builder for Birthday Planning.

Categorizes components from src/activities/ and src/gifts/ into a clean layout.
"""

import os
import glob
import subprocess
import re
import shutil
import argparse
from datetime import datetime

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
</head>
<body>
    <header class="section-wrapped">
        <div class="header-flex">
            <div>
                <span class="uppercase-label">April 12 Planning</span>
                <h3 style="font-family: var(--font-serif);"><a href="index.html" style="text-decoration: none; color: inherit;">Dashboard</a></h3>
            </div>
            <nav>
                <a href="index.html">The Collection</a>
                <a href="#activities">Activities</a>
                <a href="#gifts">Gifts</a>
            </nav>
        </div>
    </header>

    <main>
        {content}
    </main>

    <footer class="section-wrapped" style="padding: var(--spacing-lg) 0; border-top: 1px solid var(--color-border); margin-top: var(--spacing-xl);">
        <p class="text-muted" style="font-size: 0.8rem;">Curated for Chris’s Wife · Last update {build_date}</p>
    </footer>
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
    # Strip meta tags if any
    clean_html = re.sub(r'<meta[^>]+>', '', html)
    title = extract_meta(html, "title", "Untitled")
    desc = extract_meta(html, "description", "")
    return {
        "content": clean_html.strip(),
        "title": title,
        "description": desc,
        "filename": os.path.basename(filepath)
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--s3-bucket", help="S3 bucket URI")
    parser.add_argument("--cloudfront-id", help="CloudFront ID")
    args = parser.parse_args()

    build_date = datetime.now().strftime("%B %d, %Y")
    
    # 1. Copy Assets
    if os.path.exists(CSS_FILE):
        shutil.copy2(CSS_FILE, os.path.join(OUTPUT_DIR, "birthday.css"))
    
    # Copy images if they exist in data/images
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

    # 3. Assemble Index
    index_html = f"""
    <div class="section-wrapped">
        <section class="editorial-section" style="margin-top: var(--spacing-lg);">
            <div class="content-wrapped">
                <span class="uppercase-label">State of Search</span>
                <h1 style="margin-top: var(--spacing-sm);">A PNW Farewell.</h1>
                <p class="text-muted" style="font-size: 1.2rem; margin-top: var(--spacing-md);">A curated collection of experiences and tokens to celebrate her final Seattle birthday.</p>
            </div>
        </section>

        <section id="activities" class="editorial-section">
            <div class="content-wrapped">
                <h2 style="margin-bottom: var(--spacing-lg);">Day-Of Experiences</h2>
            </div>
            <div class="editorial-grid">
                {''.join([f'<div class="grid-item">{item["content"]}</div>' for item in activities])}
            </div>
        </section>

        <section id="gifts" class="editorial-section">
            <div class="content-wrapped">
                <h2 style="margin-bottom: var(--spacing-lg);">The Gift Options</h2>
            </div>
            <div class="editorial-grid">
                {''.join([f'<div class="grid-item">{item["content"]}</div>' for item in gifts])}
            </div>
        </section>
    </div>
    """

    final_page = TEMPLATE.format(page_title="Dashboard", content=index_html, build_date=build_date)
    
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
        f.write(final_page)

    print("Success: Generated index.html")

    # 4. Deployment & Git
    if args.s3_bucket:
        subprocess.run(["aws", "s3", "sync", OUTPUT_DIR, args.s3_bucket, "--profile", PROFILE, "--delete"], check=True)
        if args.cloudfront_id:
            subprocess.run(["aws", "cloudfront", "create-invalidation", "--distribution-id", args.cloudfront_id, "--paths", "/*"], check=True)

    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    subprocess.run(["git", "add", "sites/birthday/"], cwd=repo_root, check=True)
    status = subprocess.run(["git", "status", "--porcelain", "sites/birthday/"], cwd=repo_root, capture_output=True, text=True)
    if status.stdout.strip():
        subprocess.run(["git", "commit", "-m", "feat: redesign birthday dashboard to editorial aesthetic"], cwd=repo_root, check=True)
        subprocess.run(["git", "push"], cwd=repo_root, check=True)

if __name__ == "__main__":
    main()
