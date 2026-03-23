---
title: "Global Bridge Inventory"
date: 2026-03-16
category: "Technology & Infrastructure"
tags: ["bridges", "infrastructure", "civil-engineering", "transport", "gis"]
---

# Research Report: Global Bridge Inventory & Infrastructure Data

**Date:** 2026-03-16  
**Topic:** Global Bridge Inventory  
**Status:** Completed  

---

## 1. Brainstorming: Novel Dataset Types
The following dataset types were brainstormed as potential additions to the local knowledge graph. These focus on high-value, factual, and locally storable infrastructure and cultural data that have not been previously researched.

1.  **Global Bridge Inventory**: Detailed technical data on bridges worldwide (locations, materials, structural types, construction dates). (SELECTED)
2.  **Historical Scientific Instrument Catalogs**: Databases of historical astrolabes, telescopes, and clocks from major museums.
3.  **Global Postal Code Geometry and Metadata**: Geographic boundaries and administrative associations for postal codes globally.
4.  **International Sign Language Lexicons**: Structured data on the vocabulary and geographic variations of different sign languages.
5.  **Global Radio and TV Broadcast Infrastructure**: Locations, frequencies, power levels, and ownership of broadcast stations.

---

## 2. Selected Idea: Global Bridge Inventory
Bridges are critical nodes in global transportation networks. A comprehensive inventory of bridges—including their location, structural type, material, age, and capacity—provides a deep layer of engineering and logistical knowledge for the local knowledge graph.

---

## 3. Detailed Research Findings

### 3.1. Where can this data be obtained?
There is no single "official" global database, but several high-quality sources provide extensive coverage:

*   **World Food Programme (WFP) / Humanitarian Data Exchange (HDX):**
    -   **Source:** [HDX - Global Bridges (WFP SDI-T)](https://data.humdata.org/dataset/wfp-sdi-t-logistics-database-global-bridges)
    -   **Description:** A centralized global layer used for humanitarian logistics.
*   **OpenStreetMap (OSM):**
    -   **Source:** [Overpass API](https://overpass-turbo.eu/)
    -   **Description:** The most comprehensive and frequently updated global source. Bridges are tagged as `bridge=yes` or with specific types like `bridge:structure=suspension`.
*   **US National Bridge Inventory (NBI):**
    -   **Source:** [FHWA NBI](https://www.fhwa.dot.gov/bridge/nbi.cfm)
    -   **Description:** Provides extreme technical detail for ~700,000 US bridges (material, condition, deck area).
*   **World Bank Global Roads Inventory Project (GRIP):**
    -   **Source:** [World Bank Data Catalog](https://datacatalog.worldbank.org/search/dataset/0039541)
    -   **Description:** Includes bridge nodes as part of the global road network.

### 3.2. Data Format
*   **WFP/HDX:** GeoJSON, Zipped Shapefile.
*   **OSM:** JSON, XML, or CSV (via Overpass API or planet dumps).
*   **NBI:** CSV, Excel, and Shapefile.
*   **World Bank GRIP:** CSV and Shapefile.

### 3.3. Licensing, Costs, and Rate Limits
*   **WFP/HDX:** Creative Commons Attribution (CC-BY). Free.
*   **OSM:** Open Database License (ODbL). Free, but Overpass API has rate limits for large queries (better to use planet fragments/PBF files for bulk scraping).
*   **NBI:** Public Domain (US Government). Free, no limits.
*   **World Bank GRIP:** Creative Commons Attribution 4.0 (CC-BY 4.0). Free.

### 3.4. Dataset Size
*   **WFP Global Bridges:** ~200-500 MB (GeoJSON).
*   **OSM Global Bridges:** Extraction of all `bridge` tags from a full planet dump (~70 GB PBF) would likely result in several GBs of JSON/CSV data.
*   **US NBI:** ~500 MB for the full CSV dataset.

### 3.5. Estimated Effort to Scrape/Download
*   **WFP/HDX:** **Low**. Single API call to the WFS endpoint or direct download from HDX.
*   **OSM:** **Moderate/High**. Requires writing an Overpass query or using `osmium` to filter a planet.pbf file.
*   **US NBI:** **Low**. Direct bulk download of annual files.

---

## 4. Conclusion & Strategy
To build a robust bridge inventory, the recommended strategy is to:
1.  **Baseline:** Download the WFP Global Bridges dataset for immediate global coverage.
2.  **Enrichment:** Download the US NBI for high-resolution technical data in North America.
3.  **Refinement:** Use the OSM Overpass API to incrementally update and fill gaps in regions with sparse WFP coverage.

This multi-source approach ensures a balance between breadth (Global) and depth (Technical).
