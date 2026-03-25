#!/usr/bin/env python3
"""
build_birthday.py — Static site builder for the April 12 Birthday Planning Dashboard.

Reads HTML fragments from src/, wraps them in the dashboard shell, builds index.html,
and optionally syncs to S3 + invalidates CloudFront.
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

os.makedirs(SRC_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Tag → badge colour mapping ────────────────────────────────────────────────
TAG_CLASSES = {
    "proposal":  "tag-proposal",
    "research":  "tag-research",
    "logistics": "tag-logistics",
    "question":  "tag-question",
}

TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title} | April 12 Planning Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="birthday.css">
</head>
<body>
    <div class="wrapper">
        <header>
            <div class="header-inner">
                <div class="header-icon">🎂</div>
                <div>
                    <h1>April 12 Planning Dashboard</h1>
                    <div class="subtitle">A Perfect Day · Baby-Friendly · Introvert-Safe</div>
                </div>
            </div>
            <nav class="header-nav">
                <a href="index.html">All Updates</a>
                <a href="proposals.html">Proposals</a>
                <a href="questions.html">Open Questions</a>
            </nav>
        </header>

        <main>
            {content}
        </main>

        <footer>
            <p>Birthday Architect · Last built {build_date}</p>
        </footer>
    </div>
</body>
</html>
"""


def extract_meta(html: str, name: str, fallback: str = "") -> str:
    """Extract <meta name="..." content="..."> from an HTML fragment."""
    # name-first: <meta name="title" content="...">
    pattern_name_first = (
        r'<meta\s+name=["\']' + re.escape(name) + r'["\'][^>]+content=["\']([^"\']+)["\']'
    )
    m = re.search(pattern_name_first, html, re.IGNORECASE)
    if m:
        return m.group(1)
    # content-first: <meta content="..." name="title">
    pattern_content_first = (
        r'<meta\s+content=["\']([^"\']+)["\']\s+name=["\']' + re.escape(name) + r'["\']'
    )
    m = re.search(pattern_content_first, html, re.IGNORECASE)
    return m.group(1) if m else fallback


def strip_metadata_block(html: str) -> str:
    return re.sub(r'<div class="metadata".*?</div>', '', html, flags=re.DOTALL)


def build_fragment_card(filename: str, title: str, description: str, tag: str, date_str: str) -> str:
    tag_lower = tag.lower().split("|")[0].strip()
    tag_class = TAG_CLASSES.get(tag_lower, "tag-proposal")
    fragment_url = filename
    return f"""
    <article class="fragment-card">
        <div class="fragment-card-header">
            <span class="tag {tag_class}">{tag}</span>
            <span class="fragment-date">{date_str}</span>
        </div>
        <h2 class="fragment-title"><a href="{fragment_url}">{title}</a></h2>
        <p class="fragment-desc">{description}</p>
    </article>
    """


def main():
    parser = argparse.ArgumentParser(description="Birthday Planning Dashboard Builder")
    parser.add_argument("--source",         default=SRC_DIR,  help="Source directory of HTML fragments")
    parser.add_argument("--output",         default=OUTPUT_DIR, help="Output directory")
    parser.add_argument("--s3-bucket",      help="S3 bucket URI, e.g. s3://bucket/birthday/")
    parser.add_argument("--cloudfront-id",  help="CloudFront Distribution ID for cache invalidation")
    parser.add_argument("--site-name",      default="April 12 Planning Dashboard")
    args = parser.parse_args()

    src_dir    = args.source
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)

    build_date = datetime.now().strftime("%B %d, %Y at %H:%M")
    print(f"Building {args.site_name}...")

    # Copy CSS
    if os.path.exists(CSS_FILE):
        shutil.copy2(CSS_FILE, os.path.join(output_dir, "birthday.css"))

    # Gather and sort fragments (newest first)
    files = sorted(
        glob.glob(os.path.join(src_dir, "*.html")),
        key=lambda f: os.path.basename(f),
        reverse=True
    )

    index_cards       = ""
    proposal_cards    = ""
    question_cards    = ""
    fragment_count    = 0

    for filepath in files:
        filename  = os.path.basename(filepath)
        date_match = re.match(r'^(\d{4}-\d{2}-\d{2})_(.+)\.html?$', filename)
        date_str  = date_match.group(1) if date_match else "Unknown date"

        with open(filepath) as f:
            html = f.read()

        title       = extract_meta(html, "title",       fallback=filename)
        description = extract_meta(html, "description", fallback="")
        tag         = extract_meta(html, "tag",         fallback="Research")

        # Build individual article page
        body         = strip_metadata_block(html)
        article_html = f"""
        <div class="fragment-header">
            <div class="fragment-breadcrumb"><a href="index.html">← All Updates</a></div>
            <span class="tag {TAG_CLASSES.get(tag.lower().split('|')[0].strip(), 'tag-proposal')}">{tag}</span>
            <span class="fragment-date">{date_str}</span>
        </div>
        <h1 class="article-title">{title}</h1>
        {body}
        """
        page = (TEMPLATE
                .replace("{page_title}", title)
                .replace("{content}", article_html)
                .replace("{build_date}", build_date))
        with open(os.path.join(output_dir, filename), "w") as f:
            f.write(page)

        # Build card for indexes
        card = build_fragment_card(filename, title, description, tag, date_str)
        index_cards += card
        fragment_count += 1

        tag_lower = tag.lower()
        if "proposal" in tag_lower:
            proposal_cards += card
        if "question" in tag_lower:
            question_cards += card

    # Empty-state fallbacks
    def empty(msg):
        return f'<p class="empty-state">{msg}</p>'

    if not index_cards:
        index_cards = empty("No planning updates yet. The Birthday Architect is warming up. ☕")
    if not proposal_cards:
        proposal_cards = empty("No proposals yet.")
    if not question_cards:
        question_cards = empty("No open questions yet.")

    def write_page(page_title, heading, content, out_filename):
        body = f"<h1 class='page-heading'>{heading}</h1>\n{content}"
        page = (TEMPLATE
                .replace("{page_title}", page_title)
                .replace("{content}", body)
                .replace("{build_date}", build_date))
        with open(os.path.join(output_dir, out_filename), "w") as f:
            f.write(page)

    write_page("All Updates",    "All Planning Updates",   index_cards,    "index.html")
    write_page("Proposals",      "Proposals",              proposal_cards, "proposals.html")
    write_page("Open Questions", "Open Questions",         question_cards, "questions.html")

    print(f"Generated index.html, proposals.html, questions.html. Found {fragment_count} planning fragment(s).")

    # ── Sync to S3 ─────────────────────────────────────────────────────────────
    if args.s3_bucket:
        print(f"Syncing to S3: {args.s3_bucket}")
        subprocess.run(
            ["aws", "s3", "sync", output_dir, args.s3_bucket, "--profile", PROFILE, "--delete"],
            check=True
        )
        print("Site published successfully!")

        if args.cloudfront_id:
            print(f"Invalidating CloudFront cache for {args.cloudfront_id} ...")
            subprocess.run(
                ["aws", "cloudfront", "create-invalidation",
                 "--distribution-id", args.cloudfront_id,
                 "--paths", "/*"],
                check=True
            )
            print("CloudFront invalidation requested.")

    # ── Git commit ─────────────────────────────────────────────────────────────
    print("Committing and pushing changes to git...")
    # Script is at: <repo>/sites/birthday/build_birthday.py
    # dirname x1 → sites/birthday/  dirname x2 → sites/  dirname x3 → <repo>
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    site_dir  = "sites/birthday/"

    subprocess.run(["git", "add", site_dir], cwd=repo_root, check=True)
    status = subprocess.run(
        ["git", "status", "--porcelain", site_dir],
        cwd=repo_root, capture_output=True, text=True
    )
    if status.stdout.strip():
        today = datetime.now().strftime("%Y-%m-%d")
        subprocess.run(
            ["git", "commit", "-m", f"birthday: planning update {today}"],
            cwd=repo_root, check=True
        )
        subprocess.run(["git", "push"], cwd=repo_root, check=True)
        print("Git commit and push successful.")
    else:
        print("No new changes to commit.")


if __name__ == "__main__":
    main()
