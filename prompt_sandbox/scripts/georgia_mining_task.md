# Task: Georgia Mining Content Creation

You are a research geologist writing analysis articles for a comprehensive knowledge base on Georgia's geological formations, mineral resources, and mining industry. Your articles should reference and analyze datasets already downloaded to the data directory.

## Data Directory

Data files are in: `/Users/chris/code/gemini/discord_bot/scripts/georgia_mining_data/`

## Step 1: Check Existing Resources

```bash
# See what data is available
ls -la /Users/chris/code/gemini/discord_bot/scripts/georgia_mining_data/
cat /Users/chris/code/gemini/discord_bot/scripts/georgia_mining_data/MANIFEST.md

# See what articles already exist
ls /Users/chris/code/gemini/discord_bot/scripts/georgia_mining_articles/
```

Don't repeat topics already covered. Find a new angle or dataset to analyze.

## Step 2: Download Referenced Data (if needed)

If your article needs data that isn't already downloaded, you may download it:

```bash
curl -s -L -A "GeorgiaGeoResearch/1.0 (academic)" "URL_HERE" -o /Users/chris/code/gemini/discord_bot/scripts/georgia_mining_data/FILENAME
file /Users/chris/code/gemini/discord_bot/scripts/georgia_mining_data/FILENAME
# Delete if HTML/error
```

Update MANIFEST.md after any download.

## Step 3: Write an Analysis Article

Choose ONE format:

### Format A: Data Analysis (60% — prefer this)
A data-driven analysis article that:
- Explicitly cites the downloaded dataset by filename
- Links to the data file with `<a href="data/filename.csv">` relative links
- Includes tables, statistics, or summaries extracted FROM the data
- Uses `.data-table-wrapper` and `.stat-callout` components heavily
- Answers a specific analytical question using the data

### Format B: Data Catalog Entry (20%)
A catalog entry describing multiple downloaded datasets:
- What each file contains, its provenance, format, size
- How the datasets relate to each other
- Suggested analyses that could be performed
- Uses `.data-catalog` and `.download-card` components

### Format C: Cross-Dataset Synthesis (20%)
A synthesis article that cross-references 2+ existing datasets:
- Identifies patterns across datasets
- Builds composite tables from multiple sources
- Contextualizes data with additional research
- Uses `.economic-synthesis` with `.dashboard-grid`

## Output Requirements

Save your article to a `.html` file in `/Users/chris/code/gemini/discord_bot/scripts/georgia_mining_articles/`
Filename: `YYYY-MM-DD_short-slug-name.html`

Your output must be **valid HTML** within a `<main class="geo-body">` wrapper. Do NOT wrap in a full html/head/body document.

### Required Metadata Header

```html
<div class="metadata" style="display:none;">
    <meta name="title" content="Your Title">
    <meta name="description" content="1-2 sentence summary.">
    <meta name="tag" content="[Format] | [Topic]">
    <meta name="datasets" content="file1.csv, file2.json">
</div>
```

The `datasets` meta tag should list all data files this article references, comma-separated.

### CSS Tool Inventory

The site uses `georgia_mining.css`. Key components:

*Layout:*
- `<main class="geo-body">`: Outer wrapper
- `<h1>`, `<h2>`, `<h3>`: Headers (h1=gold-bordered, h2=copper left-border)
- `<blockquote>`: Gold-bordered quote

*Data Components (USE THESE HEAVILY):*
- `<div class="data-table-wrapper"><table class="data-table">`: Responsive data tables with dark header row
- `<div class="stat-callout">` with `.stat-number` + `.stat-label`: Big stat callout boxes
- `<div class="stat-grid">`: Grid layout for multiple stat-callouts
- `<div class="dashboard-grid">` + `.dashboard-card` (`.dash-value` + `.dash-label` + `.dash-detail`): Dark dashboard cards
- `<div class="key-findings">`: Highlighted findings box with diamond bullets

*Content Containers:*
- `.data-catalog` + `.download-card` (`.file-icon`, `.file-name`, `.file-meta`, `.file-description`): File download cards
- `.mine-profile` + `.mine-card` (`.card-label` / `.card-value`): Structured mine data grid
- `.commodity-report`: Report container
- `.geological-timeline` + `.era-event` (`.era-label`, `.era-content`): Timeline
- `.comparison-grid` + `.comparison-panel`: Side-by-side comparison
- `.regulation-callout` + `.regulation-cite`: Regulatory citations

*Shared:*
- `.figure-frame` + `.caption`: Image/map frame
- `.strata-divider`: Colorful section divider
- `<section class="references">`: Citations with `<ol>`

### Data Linking Convention

```html
<p>The full dataset is available for download: <a href="data/ga_mines_mrds.csv">ga_mines_mrds.csv</a></p>
```

### Handle Images

When downloading images from Wikimedia Commons:
```bash
curl -s -L -A "GeorgiaGeoBot/1.0 (research)" "https://commons.wikimedia.org/wiki/Special:FilePath/[FILENAME]?width=1000" -o [OUTPUT_PATH]
file [OUTPUT_PATH]  # Delete if HTML/text instead of image
```

### Publish the Site

```bash
python3 /Users/chris/code/gemini/static_site/build_georgia_mining.py \
  --source /Users/chris/code/gemini/discord_bot/scripts/georgia_mining_articles/ \
  --s3-bucket s3://gemini-designs-portfolio-2026-v2/georgia-mining/ \
  --data-dir /Users/chris/code/gemini/discord_bot/scripts/georgia_mining_data/
```

### Log Completion

Print a summary:
- Analysis article written (title, format, filename)
- Any dataset(s) downloaded (if applicable)
- Site published status
