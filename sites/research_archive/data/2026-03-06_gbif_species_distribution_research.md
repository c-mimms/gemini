---
title: "Global Biodiversity Information Facility (GBIF)"
date: 2026-03-06
category: "Life Sciences"
tags: ["biodiversity", "species", "ecology", "gbif", "open-data"]
---

# Research Report: Global Biodiversity Information Facility (GBIF)

**Date**: 2026-03-06
**Topic**: Global Biological Species Distribution (GBIF)

## 1. Brainstormed Ideas
- **Global Biological Species Distribution (GBIF)**: Over 3.65 billion records of species occurrences worldwide, providing deep GIS-based factual knowledge about the natural world.
- **Historical Maritime Trade Routes (CLIWOC)**: Digitized ship logbooks from 1750-1850, offering a unique look at historical trade, weather, and global movements.
- **Museum Metadata (National Gallery of Art / Smithsonian)**: Structured data on art history, including artists, styles, periods, and high-resolution image links.
- **Global Power Plant Database (WRI)**: A comprehensive, open-source database of power plants around the world, including type, capacity, and generation data.
- **Historical Newspaper Metadata (Chronicling America)**: API for metadata and OCR text from millions of pages of American newspapers (1770–1963).

## 2. Selected Idea
**Global Biological Species Distribution (GBIF)** was selected for its massive scale, high level of structure, and value in providing "ground truth" for the biological and geographical components of a local knowledge graph.

## 3. Research Findings: GBIF

### Where can this data be obtained?
- **API**: The [GBIF Occurrence API](https://www.gbif.org/developer/occurrence) is the primary method for filtered downloads. The base endpoint is `https://api.gbif.org/v1/occurrence/download/request`.
- **Bulk Download**: Full snapshots are available on cloud platforms like **Microsoft Azure (Planetary Computer)** and **Amazon S3** (as part of the AWS Open Data program).
- **Web Portal**: [gbif.org/occurrence/search](https://www.gbif.org/occurrence/search) allows for manual filtering and download requests.

### Data Format
- **Darwin Core Archive (DWCA)**: A zipped package containing interpreted data, original publisher data, and metadata.
- **Simple CSV (TSV)**: A tab-separated file containing the most commonly used fields.
- **Simple Parquet**: Optimized for big data; available in cloud snapshots.
- **Species List**: A summarized list of species names based on filters.

### Licensing and Costs
- **Cost**: Completely free. Registration for a free account is required for downloads.
- **Licenses**: Data is published under **CC0** (Public Domain), **CC-BY** (Attribution required), or **CC-BY-NC** (Non-commercial).
- **Requirements**: Users must cite the data using a **Digital Object Identifier (DOI)** provided with each download for reproducibility.
- **Rate Limits**:
  - Concurrent downloads: 1–3 active requests per user.
  - API Predicates: Maximum of 101,000 items (e.g., taxon keys) per request.
  - Geometry: Spatial filters (within) limited to 10,000 points.

### Dataset Size
- **Total Records**: ~3.65 billion occurrences (as of March 2026).
- **Total Size**: The full compressed Parquet snapshot is estimated at **3.5+ TB**.
- **Subset Size**: A download for a specific country or species group (e.g., "Birds of North America") typically ranges from **100 MB to 10 GB**.

### Estimated Effort to Scrape/Download
- **Difficulty**: Moderate.
- **Scraper Architecture**: 
  1. Submit a JSON-based "predicate" request to the API.
  2. Receive a `downloadKey`.
  3. Poll the API status endpoint until the state changes from `PREPARING` to `SUCCEEDED`.
  4. Download the resulting ZIP or Parquet file.
- **Effort**: 1–2 days to build a robust script that handles authentication, asynchronous polling, and large file decompression.

## 4. Conclusion
GBIF is an essential dataset for a knowledge graph aimed at "answering any question" about biology or geography. While the full 3.5 TB dataset may be too large for some local storage, targeted downloads of specific regions or high-level species summaries are highly feasible and provide immense value.
