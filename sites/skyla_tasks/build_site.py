#!/usr/bin/env python3
import os
import glob
import subprocess
import shutil
import argparse
from datetime import datetime
from dotenv import load_dotenv

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(SITE_DIR, "src")
OUTPUT_DIR = os.path.join(SITE_DIR, "output")
CSS_FILE = os.path.join(SITE_DIR, "style.css")

os.makedirs(SRC_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skyla's AI Secretary Dashboard!</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>✨ Skyla's AI Secretary ✨</h1>
        <p class="text-muted" style="font-family: monospace;">Last synced: {build_date}</p>
        
        <main>
            {content}
        </main>
        
        <div style="text-align: center; margin-top: 50px;">
            <a href="#" class="btn-fun">Send me an email to add tasks!</a>
        </div>
    </div>
</body>
</html>
"""

def main():
    load_dotenv()
    # It attempts to use ENV vars first, or you can override with args
    s3_bucket = os.getenv("S3_BUCKET", "s3://skyla.cbmo.net")
    cf_id = os.getenv("CLOUDFRONT_ID", "")
    aws_profile = os.getenv("AWS_PROFILE", "default")
    
    build_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    # 1. Copy Assets
    if os.path.exists(CSS_FILE):
        shutil.copy2(CSS_FILE, os.path.join(OUTPUT_DIR, "style.css"))
        
    # 2. Gather Component Content
    content_html = ""
    snippets = sorted(glob.glob(os.path.join(SRC_DIR, "*.html")))
    
    if not snippets:
        content_html = "<div class='silly-box'><h2>Hi Skyla!</h2><p>I am your new magical AI secretary. I haven't done any tasks yet, but I'm super excited to start!</p></div>"
    else:
        for f in snippets:
            with open(f, "r") as html_file:
                content_html += f"<div class='content-block'>\n{html_file.read()}\n</div>\n"

    # 3. Assemble Index
    index_html = TEMPLATE.format(content=content_html, build_date=build_date)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
        f.write(index_html)
        
    print("Success: Generated index.html in output/")

    # 4. Deployment & Git
    # Deploy to S3 if configured
    if s3_bucket and "://" in s3_bucket:
        try:
            print(f"Deploying to {s3_bucket}...")
            subprocess.run(["aws", "s3", "sync", OUTPUT_DIR, s3_bucket, "--profile", aws_profile, "--delete"], check=True)
            if cf_id:
                print(f"Invalidating CloudFront {cf_id}...")
                subprocess.run(["aws", "cloudfront", "create-invalidation", "--distribution-id", cf_id, "--paths", "/*", "--profile", aws_profile], check=True)
        except subprocess.CalledProcessError as e:
            print(f"AWS deployment skipped/failed: {e}")

    # Commit to repo
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        subprocess.run(["git", "add", "sites/skyla_tasks/"], cwd=repo_root, check=True)
        status = subprocess.run(["git", "status", "--porcelain", "sites/skyla_tasks/"], cwd=repo_root, capture_output=True, text=True)
        if status.stdout.strip():
            subprocess.run(["git", "commit", "-m", "update: agent published new skyla tasks site"], cwd=repo_root, check=True)
            subprocess.run(["git", "push"], cwd=repo_root, check=True)
    except Exception as e:
        print(f"Git sync failed: {e}")

if __name__ == "__main__":
    main()
