---
title: "Global Fishing Activity (Global Fishing Watch)"
date: 2026-03-21
category: "Earth & Environment"
tags: ["fishing", "ocean", "ais", "maritime", "global-fishing-watch"]
---

# Research Report: Global Fishing Activity (Global Fishing Watch)

## Brainstormed Ideas
1.  **Global Fishing Activity (Global Fishing Watch)**: Vessel movements and fishing patterns.
2.  **Global Fire History (MODIS/VIIRS)**: Historical satellite-detected fire data.
3.  **Global Genealogy and Surname Distribution**: Surname frequency and origin maps.
4.  **Global Real-time / Historical Air Quality (OpenAQ)**: Air quality sensors worldwide.
5.  **Global Toponyms and Etymology**: Origins and history of place names across the world.

## Selected Idea: Global Fishing Activity (Global Fishing Watch)
Global Fishing Watch (GFW) provides high-resolution data on maritime activities, primarily focusing on commercial fishing. This dataset is a powerful source of behavioral and spatial knowledge for a local knowledge graph, offering insights into vessel identities, fishing effort, and maritime infrastructure.

## Research Findings

### 1. Where can this data be obtained?
The data can be accessed through multiple channels provided by Global Fishing Watch:
- **Data Download Portal**: [globalfishingwatch.org/data-download](https://globalfishingwatch.org/data-download) — Offers static versioned CSV files for vessel identity, fishing effort, and port visits.
- **Bulk Download API (v3)**: An asynchronous API designed for retrieving large datasets that exceed the limits of standard REST endpoints.
- **Google BigQuery Public Dataset**: The full raw AIS database (terabyte-scale) is hosted on BigQuery under the dataset `global-fishing-watch.fishing_effort_v3`.
- **Specialized APIs**: Vessels API, Events API (encounters, loitering, port visits), and Datasets API.

### 2. What is the format of the data?
- **Tabular**: Primarily **CSV** and **JSON** for vessel records and event logs.
- **Spatial/Gridded**: **GeoTIFF** or **PNG** for gridded effort layers.
- **Vector**: **MVT** (Mapbox Vector Tiles) for map-based visualizations.
- **Bulk Packages**: Downloads often come as a package containing the data file (CSV/JSON), geometry files, and metadata documentation.

### 3. Rate limits, licensing, and costs
- **Licensing**: Operating under **CC BY-NC 4.0** (Creative Commons Attribution-NonCommercial). The data is free for academic, NGO, and government use.
- **Attribution**: Mandatory; Global Fishing Watch must be credited in any resulting work.
- **Commercial Use**: Requires a custom license and direct contact with GFW (`apis@globalfishingwatch.org`).
- **Rate Limits**: API keys are required (free registration). Standard rate limits apply to REST endpoints, but the Bulk Download API is designed for high-volume retrieval.

### 4. Approximate size of the dataset
- **Processed CSVs**: Typically range from **several hundred MB to 10+ GB** depending on resolution and time span.
- **Raw AIS Data**: Bills of messages from 2012 to the present, totaling in the **multi-terabyte (TB)** range.
- **Recent Effort Data**: The March 2025 release contains ~695 million fishing hours across ~192,000 vessels.

### 5. Estimated effort to write a scraper or download script
- **Effort Level**: **Moderate**.
- **Implementation**:
    - For static downloads, a simple `requests` or `wget` script can fetch the versioned CSVs from the portal.
    - For the Bulk API, a polling script is required: 1) POST a request for a report, 2) Poll the status endpoint until complete, 3) Download the result.
    - For BigQuery, a Python script using the `google-cloud-bigquery` library can execute SQL queries to extract specific subsets directly into local storage.
