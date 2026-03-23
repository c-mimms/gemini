---
title: "GHCN Daily Climate Data (NOAA)"
date: 2026-03-08
category: "Earth & Environment"
tags: ["climate", "weather", "temperature", "noaa", "historical-data"]
---

# Knowledge Graph Research: Global Historical Climate Data (GHCN-Daily)

## Date: 2026-03-08

## Brainstormed Ideas
For this research cycle, the following novel dataset types were identified as high-value candidates for a local knowledge graph:

1.  **Global Historical Climate Data (GHCN-Daily)** (Selected): Comprehensive daily climate summaries from land surface stations worldwide.
2.  **WHO Global Health Observatory (GHO)**: Factual health statistics and indicators across all countries, covering diseases, nutrition, and health systems.
3.  **UN FAOSTAT**: Detailed data on global agricultural production, land use, trade, and food security from the Food and Agriculture Organization.
4.  **Internet Archive WayBack Machine Metadata**: Metadata indexing the history of the web, including URLs, crawl timestamps, and content types (CDX files).
5.  **UNHCR Refugee and Migration Flows**: Data on populations of concern, refugee movements, and asylum applications globally.

---

## Selected Idea: Global Historical Climate Data (GHCN-Daily)

### 1. Description
The Global Historical Climatology Network Daily (GHCN-Daily) is an integrated database of daily climate summaries from land surface stations across the globe. It is maintained by the NOAA National Centers for Environmental Information (NCEI) and contains records from over 100,000 stations in 180 countries and territories.

### 2. Where to obtain the data
- **Primary Source (HTTPS/FTP):** [NCEI GHCN-Daily Archive](https://www.ncei.noaa.gov/pub/data/ghcn/daily/)
- **Documentation:** [GHCN-Daily Readme](https://www.ncei.noaa.gov/pub/data/ghcn/daily/readme.txt)
- **Cloud Mirrors (CSV/Parquet):** Available on AWS S3 via the [NOAA Open Data Dissemination (NODD) Program](https://registry.opendata.aws/noaa-ghcn).
- **Google Cloud:** Available as a public dataset in BigQuery.

### 3. Data Format
- **ASCII (.dly / .txt):** The official archive uses a fixed-width format. One file per station (`.dly`) or bulk files grouped by year.
- **CSV:** Available via the AWS S3 mirrors and through the NOAA Climate Data Online (CDO) search tool.
- **Metadata:** Station list (`ghcnd-stations.txt`), country codes (`ghcnd-countries.txt`), and inventory (`ghcnd-inventory.txt`) are provided as text files.

### 4. Licensing and Costs
- **Licensing:** Public Domain (CC0-1.0). NOAA requests attribution but does not impose usage restrictions.
- **Costs:** Free to download from NCEI. Egress costs may apply if downloading massive volumes from AWS outside of the US-East-1 region, but the dataset itself is part of the "Free Tier" of open data.
- **Rate Limits:** No strict rate limits on the NCEI HTTPS server, but polite scraping (one connection at a time) is recommended for bulk downloads.

### 5. Dataset Size
- **Compressed (GZIP):** Approximately 12 GB to 20 GB.
- **Uncompressed:** Over 100 GB (ASCII/Fixed-width). CSV versions can be significantly larger (200GB+).
- **Record Count:** Over 1.4 billion data points.

### 6. Implementation Effort
- **Scraper/Downloader:** Low effort. A simple `wget` or `python` script can mirror the HTTPS directory or pull from S3.
- **Parser:** Moderate effort. The fixed-width format requires a specific parser (documented in the `readme.txt`). However, choosing the CSV format from AWS would reduce this to a simple `pandas` or `csv` module task.
- **Storage Strategy:** Due to the 1.4B records, a simple SQLite database might struggle without heavy optimization. A columnar storage format (Parquet) or a high-performance time-series database (like InfluxDB or QuestDB) would be ideal for local hosting.

---
## Conclusion
GHCN-Daily is an excellent candidate for the knowledge graph. It provides foundational factual data about the physical world that can be cross-referenced with historical events, agricultural data, and geographic information.
