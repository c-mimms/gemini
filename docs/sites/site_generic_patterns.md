# Extractable Patterns Across Existing Sites

Analysis of shared patterns, code duplication, and opportunities for abstraction across the 5 sites:
**Museum, News (The Dispatch), Prayer, Georgia Mining, Research Archive**

---

## 1. Build Script Duplication

All 5 build scripts share a near-identical core. The common logic ~500 lines long is copy-pasted across each:

| Pattern | All Scripts | Inconsistencies |
|---------|-------------|-----------------|
| `argparse` setup | ✅ All 5 | Museum was missing `--cloudfront-id` (fixed) |
| `aws s3 sync --delete` | ✅ All 5 | Identical 3-line block |
| CloudFront invalidation | ✅ 4 of 5 | Research Archive has none |
| Metadata extraction from `<meta>` tags | ✅ All 5 | Slightly different regex flavors |
| Date parsing from filename `YYYY-MM-DD_slug` | ✅ All 5 | Identical |
| `output/` build dir creation + wipe | ✅ All 5 | Identical |
| CSS file copy to `output/` | ✅ All 5 | Identical pattern |
| `images/` dir copy to `output/` | ✅ 3 of 5  | Museum, Georgia Mining, News |

### Proposed: `shared_build_lib.py`

Extract a shared library at `sites/_shared/build_lib.py` containing:

```python
def standard_argparse(description):
    """Returns a pre-configured ArgumentParser with the standard 5 flags."""

def extract_article_meta(filepath, filename):
    """Standard metadata extraction from HTML meta tags + filename date."""

def sync_to_s3(build_dir, s3_bucket):
    """Run aws s3 sync and handle errors."""

def invalidate_cloudfront(distribution_id):
    """Run aws cloudfront create-invalidation."""

def prepare_build_dir(script_dir, css_filename, source_dir):
    """Wipe/create output/, copy CSS, copy images/."""
```

Each site's `build_X.py` would `import build_lib` and only implement its own site-specific `build_index_html()` and `post_process_article()` functions.

---

## 2. Metadata Convention is Inconsistent

The metadata block written by the AI is slightly different across sites:

| Site | Tag used for category | Tag used for topic |
|------|-----------------------|--------------------|
| Museum | `<meta name="tag">` | Format \| Theme |
| Prayer | `<meta name="category">` | `general` or `happy` |
| Georgia Mining | `<meta name="tag">` | Format \| Topic |
| News | `<meta name="category">` | single word |
| Research Archive | *(none — markdown files)* | — |

### Proposed: Unified metadata block

Standardize all sites to use both tags:
```html
<div class="metadata" style="display:none;">
    <meta name="title" content="...">
    <meta name="description" content="...">
    <meta name="category" content="economy">        <!-- broad category for filtering -->
    <meta name="tag" content="Deep Dive | Hardware"> <!-- display tag -->
</div>
```

---

## 3. Task Definition Structure

All 5 task definitions follow an implicit 6-step pattern but the ordering and naming varies:

| Step | Pattern | Inconsistency |
|------|---------|---------------|
| 1. Check for duplicates | All 5 | Research archive forgets to say "skip already covered topics" explicitly |
| 2. Brainstorm / pick topic | All 5 | Museum picks a *format* first, then topic. Others pick topic first. |
| 3. Research | All 5 | None significant |
| 4. Write & save HTML | All 5 | Filename date format: Research archive had `YYY-MM-DD` typo (fixed) |
| 5. Publish | All 5 | All now have CloudFront ✅ |
| 6. Log completion | All 5 | Good — all specify what to print |

### Proposed: Task Definition Template

Create a boilerplate `sites/_shared/new_site_task_template.md` that all future tasks inherit from, with clearly marked `<!-- CUSTOMIZE THIS -->` sections.

---

## 4. Image Download Pattern  

All sites that support images use the same Wikimedia Commons pattern but it appears copy-pasted literally:

```bash
# Identical in museum_task.md, georgia_mining_task.md:
curl -s -L -A "BotName/1.0" "https://commons.wikimedia.org/wiki/Special:FilePath/[FILENAME]?width=1000" -o [OUTPUT_PATH]
file [OUTPUT_PATH]
# Delete if HTML/text
```

### Proposed: `download_image.sh` helper

```bash
#!/usr/bin/env bash
# Usage: download_image.sh "Wikipedia_Filename.jpg" "/output/path.jpg" "BotName"
# Returns 0 on success, 1 on failure (and deletes the bad file)
```

This removes the if/delete logic from the task prompt, reducing cognitive load on the agent.

---

## 5. Deployment Command

The S3 prefix + CloudFront ID are currently only documented inside each task definition file. This creates a maintenance risk — there is no single source of truth.

### Proposed: `sites/sites.json`

```json
{
  "museum": {
    "s3_prefix": "s3://gemini-designs-portfolio-2026-v2/museum/",
    "cloudfront_id": "E1LL4Q1IQLN3FU",
    "build_script": "sites/museum/build_museum.py",
    "task_file": "sites/museum/museum_task.md",
    "url": "https://museum.cbmo.net"
  },
  "news": { ... },
  "prayer": { ... },
  "georgia_mining": { ... },
  "research_archive": { ... }
}
```

The build scripts would read this config, and a single `deploy_site.sh [site_name]` wrapper could handle any site without needing to remember the right arguments.

---

## 6. Missing: Health / Status Checks

None of the sites currently have any monitoring. If a build fails silently (no `is_good_fit` emails, or S3 sync fails), there's no alert.

### Proposed additions

- Build scripts should exit with a non-zero code on **any** failure (currently some just `print` errors and continue)
- Task scheduler retries: Museum and Prayer currently have `Retries: 0/0`; raising this to `0/2` would auto-retry transient failures
- A weekly "site audit" task that checks S3 for last-modified timestamps and emails if no new content was published in N days

---

## 7. Research Archive: Missing CloudFront

The Research Archive is the only site without a CloudFront invalidation. It also uses `build.py` as its script name (inconsistent — all others use `build_[sitename].py`).

**Fix needed:**
1. Add `--cloudfront-id` to `sites/research_archive/build.py`
2. Look up the correct distribution ID (see `aws cloudfront list-distributions`)
3. Update the task definition

---

## Priority Fix Summary

| # | Fix | Effort | Impact |
|---|-----|--------|--------|
| 1 | Research Archive: add CloudFront ID | Low | Medium — cache stays stale |
| 2 | Standardize metadata tags across all sites | Low | Medium — enables cross-site search |
| 3 | Extract `download_image.sh` helper | Low | Low — reduces prompt size |
| 4 | Create `shared_build_lib.py` | High | High — removes ~400 lines of duplication |
| 5 | Create `sites/sites.json` registry | Medium | Medium — central source of truth |
| 6 | Add retry counts to Prayers + Museum tasks | Low | Medium — auto-recovery from transient errors |
