---
title: "Global Soil Data (SoilGrids / FAO)"
date: 2026-03-15
category: "Earth & Environment"
tags: ["soil", "agriculture", "geospatial", "fao", "land-use"]
---

# Research Report: Global Soil Data & Properties

**Date:** 2026-03-15
**Topic:** Global Soil Data (HWSD, SoilGrids, GSOC)
**Researcher:** Gemini CLI

---

## 1. Brainstorming: Novel Dataset Types
The following dataset types were brainstormed as potential high-value, factual, and locally storable data sources for the knowledge graph:

1.  **Global Soil Data (Harmonized World Soil Database / SoilGrids)**: Detailed spatial data on soil composition (clay, sand, silt), pH, organic carbon, and texture. *Selected for this research task.*
2.  **Historical Census Data (IPUMS International)**: Integrated census microdata from over 100 countries, covering decades of demographic, social, and economic shifts.
3.  **Global Urban Expansion (Global Human Settlement Layer - GHSL)**: Satellite-derived data on human settlements, built-up areas, and population density from 1975 to the present.
4.  **Global Port and Maritime Infrastructure**: Detailed data on port capacities, berths, and historical shipping traffic (UNCTAD/World Bank).
5.  **Global Mountain Peaks and Topographic Prominence**: A comprehensive database of world peaks, including prominence, isolation, and climbing history beyond the Himalayas.

---

## 2. Selected Idea: Global Soil Data
Soil data is fundamental for understanding agricultural productivity, ecosystem health, carbon sequestration, and climate change impacts. It provides a "physical foundation" for the knowledge graph.

### Research Findings

#### A. Data Sources & Providers
There are three primary global datasets, each with different strengths:

1.  **Harmonized World Soil Database (HWSD) v2.0**:
    *   **Provider**: FAO and IIASA.
    *   **Description**: A global soil inventory combining national and regional soil maps.
    *   **URL**: [FAO Soils Portal](https://www.fao.org/soils-portal/data-hub/soil-maps-and-databases/harmonized-world-soil-database-v20/en/)

2.  **SoilGrids 2.0**:
    *   **Provider**: ISRIC — World Soil Information.
    *   **Description**: Machine-learning predicted soil properties at high resolution.
    *   **URL**: [SoilGrids.org](https://soilgrids.org)

3.  **Global Soil Organic Carbon (GSOCmap)**:
    *   **Provider**: Global Soil Partnership (GSP/FAO).
    *   **Description**: Country-driven maps specifically focusing on soil carbon stocks.
    *   **URL**: [GSOCmap Viewer](http://54.229.242.119/GSOCmap/)

#### B. Data Format
*   **HWSD**: Provided as a GIS raster (30 arc-second) linked to a soil attribute database in **SQLite** or **Microsoft Access (.mdb)**.
*   **SoilGrids**: **Cloud Optimized GeoTIFF (COG)** and Virtual Raster (VRT).
*   **GSOCmap**: **GeoTIFF** and COG.

#### C. APIs & Access
*   **SoilGrids REST API**: `https://rest.isric.org/soilgrids/v2.0/properties/query` allows for point-based queries (latitude/longitude).
*   **WebDAV/WCS**: SoilGrids supports Web Coverage Service (WCS) for extracting subsets and WebDAV for bulk downloads of VRT files.
*   **HWSD**: No REST API; requires local querying of the SQLite database.

#### D. Licensing & Costs
*   **SoilGrids**: **CC-BY-4.0** (Permissive, allows commercial use with attribution).
*   **HWSD v2.0**: **CC BY-NC-SA** (Non-commercial, share-alike).
*   **GSOCmap**: Usually **CC BY-4.0** or **CC BY-NC-SA 3.0 IGO**.
*   **Cost**: All are free for research/academic use.

#### E. Dataset Size
*   **HWSD v2.0**: Small (~50 MB for the full global database).
*   **GSOCmap**: Moderate (~1-5 GB for global layers).
*   **SoilGrids 2.0**: Massive (>500 GB for the full global high-res dataset across all properties and depths). Individual layers are ~1-2 GB.

---

## 3. Scraper/Downloader Effort Estimate

### Estimated Effort: Moderate
*   **HWSD**: Very low effort. A single download of the SQLite database provides all metadata. A simple Python script using `sqlite3` and `rasterio` can link spatial points to soil properties.
*   **SoilGrids**: High effort for full local storage, but low effort for a "on-demand" scraper using their REST API. 
*   **GSOCmap**: Low effort. Bulk downloads of GeoTIFFs are available via the FAO portal.

### Implementation Strategy
1.  **Local Knowledge Graph**: Download the HWSD v2.0 SQLite database and raster. This provides a lightweight (~50MB) factual base for global soil types.
2.  **Extended Details**: Use the SoilGrids REST API to fetch high-resolution (250m) details for specific coordinates of interest (e.g., when querying about a specific farm or city).

---

## 4. Complementary Data
*   **NOAA GSOM (Global Summary of the Month)**: Monthly climate summaries (temperature/precip) available in **CSV** (Public Domain) can be joined with soil data to model land suitability.
