# Task: Georgia Mining Data Acquisition

You are a data acquisition agent tasked with finding and downloading real, publicly available geological and mining datasets for Georgia. Your ONLY job is to find new data and download it. Do NOT write articles.

## Data Directory

All data files go in: `/Users/chris/code/gemini/prompt_sandbox/scripts/georgia_mining_data/`

## Step 1: Check Existing Data

```bash
ls -la /Users/chris/code/gemini/prompt_sandbox/scripts/georgia_mining_data/
cat /Users/chris/code/gemini/prompt_sandbox/scripts/georgia_mining_data/MANIFEST.md
```

Read the manifest to see what has already been downloaded. Do NOT re-download existing files.

## Step 2: Find New Data

Search for and download data from these sources. **Prioritize datasets with geographic coordinates (lat/lon) and GIS formats.**

### Priority 1: GIS & Geospatial Data (MOST IMPORTANT)
- **USGS MRDS with coordinates**: `https://mrdata.usgs.gov/mrds/search.php?state=GA&format=csv` — try to get versions with latitude/longitude columns
- **GeoJSON/Shapefiles**: Search for Georgia geology shapefiles, mineral deposit GeoJSON
- **USGS Geochemistry**: `https://mrdata.usgs.gov/nure/sediment/` — NURE stream sediment geochemistry
- **National Geologic Map Database**: `https://ngmdb.usgs.gov/` — state geologic map data
- **USGS Gravity/Magnetics**: `https://mrdata.usgs.gov/gravity/`, `https://mrdata.usgs.gov/magnetic/`
- **KML/KMZ files** from Georgia geological survey publications

### Priority 2: Tabular Data with Analysis Potential
- **USGS Mineral Commodity Summaries**: `https://pubs.usgs.gov/periodicals/mcs2025/mcs2025.pdf` — look for individual commodity CSV/XLS tables
- **State mineral data**: `https://www.usgs.gov/centers/national-minerals-information-center/mineral-industry-georgia`
- **Georgia EPD mining permits**: `https://epd.georgia.gov/` — permit databases, compliance data
- **USGS Water quality**: `https://waterdata.usgs.gov/ga/nwis/` — water quality near mining districts

### Priority 3: General Data Portals
- `https://catalog.data.gov/dataset?q=georgia+mining`
- `https://catalog.data.gov/dataset?q=georgia+geology`
- `https://catalog.data.gov/dataset?q=georgia+mineral`
- State open data portals

## Step 3: Download Protocol

```bash
# Always use curl with proper headers
curl -s -L -A "GeorgiaGeoResearch/1.0 (academic)" "URL_HERE" -o /Users/chris/code/gemini/prompt_sandbox/scripts/georgia_mining_data/FILENAME

# Verify the download is real data, not an error page
file /Users/chris/code/gemini/prompt_sandbox/scripts/georgia_mining_data/FILENAME
head -5 /Users/chris/code/gemini/prompt_sandbox/scripts/georgia_mining_data/FILENAME

# If the file is HTML/error instead of data, DELETE IT IMMEDIATELY
rm /Users/chris/code/gemini/prompt_sandbox/scripts/georgia_mining_data/FILENAME
```

**Acceptable formats:** CSV, TSV, JSON, GeoJSON, XLS/XLSX, XML, Shapefiles (zipped), PDF (geological reports/bulletins only), SQLite, KML/KMZ

## Step 4: Update Manifest

After EVERY successful download, append to the manifest:

```bash
echo "| filename.csv | https://source-url... | $(date +%Y-%m-%d) | CSV | $(du -h filename.csv | cut -f1) | Brief description |" >> /Users/chris/code/gemini/prompt_sandbox/scripts/georgia_mining_data/MANIFEST.md
```

## Step 5: Publish

After downloading at least one new file, rebuild and publish:

```bash
python3 /Users/chris/code/gemini/static_site/build_georgia_mining.py \
  --source /Users/chris/code/gemini/prompt_sandbox/scripts/georgia_mining_articles/ \
  --s3-bucket s3://gemini-designs-portfolio-2026-v2/georgia-mining/ \
  --data-dir /Users/chris/code/gemini/prompt_sandbox/scripts/georgia_mining_data/
```

## Step 6: Log Completion

Print a summary:
- Dataset(s) downloaded (filenames, sizes, sources)
- MANIFEST.md entries added
- Site published status
- If no new data found, print "No new datasets found this run."
