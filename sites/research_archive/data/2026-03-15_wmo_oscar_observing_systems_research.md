---
title: "WMO OSCAR Observing Systems Database"
date: 2026-03-15
category: "Earth & Environment"
tags: ["meteorology", "wmo", "observing-systems", "climate", "sensors"]
---

# Research Report: WMO OSCAR (Observing Systems Capability Analysis and Review Tool)

**Date**: 2026-03-15
**Topic**: Meteorological Observing Systems Metadata (WMO OSCAR)
**Researcher**: Gemini CLI

---

## 1. Brainstormed Ideas
Before selecting the primary research topic, the following novel dataset types were brainstormed:
1.  **WMO OSCAR (Observing Systems Capability Analysis and Review Tool)**: Technical registry of all global meteorological observing systems (selected).
2.  **Cuneiform Digital Library Initiative (CDLI)**: Digital database of ancient Near Eastern cuneiform texts.
3.  **Global Cave and Karst Database**: Registry of major cave systems and karst features worldwide.
4.  **UNESCO Intangible Cultural Heritage Database**: Factual records of cultural traditions and practices.
5.  **International Seismological Centre (ISC) Event Catalogue**: Definitive global registry of seismic events and station metadata.

---

## 2. Selected Idea: WMO OSCAR
The **WMO OSCAR** database is the official technical registry for the **WMO Integrated Global Observing System (WIGOS)**. it provides a comprehensive, structured metadata repository for all earth-observing platforms (surface, space, and upper-air) used for weather, climate, and water monitoring.

### Why it is High-Value
-   **Deep Technical Factual Knowledge**: Contains precise coordinates, sensor types, measurement frequencies, and historical metadata for every official weather station and satellite.
-   **Foundational Context**: Provides the "how" and "where" behind global climate data (GHCN, ERA5), allowing a knowledge graph to understand the reliability and source of observations.
-   **Highly Structured**: Data follows strict international standards (WMO-No. 1192 / WMDR XML), making it ideal for ingestion into a knowledge graph.

---

## 3. Research Findings

### Where can this data be obtained?
The data is managed by the World Meteorological Organization (WMO) and is accessible through two primary modules:
-   **OSCAR/Surface**: metadata for surface-based platforms (land stations, ships, buoys, radars).
    -   **API Base**: `https://oscar.wmo.int/surface/rest/api`
    -   **Search Endpoint**: `https://oscar.wmo.int/surface/rest/api/search/station`
    -   **Download Endpoint**: `https://oscar.wmo.int/surface/rest/api/wmdr/download/station/<WIGOS_Station_ID>`
-   **OSCAR/Space**: Metadata for satellite missions and instruments.
    -   **API Base**: `https://space.oscar.wmo.int/api`
    -   **Export**: The web interface provides "Full Tables" for satellites and instruments that can be exported directly.

### What is the format of the data?
-   **OSCAR/Surface**: Primarily **WMDR XML** (WIGOS Metadata Representation). Also supports **JSON**, **CSV**, and **KML** for search results and certain station metadata.
-   **OSCAR/Space**: Primarily **JSON** via a RESTful API.

### Licensing, Rate Limits, and Costs
-   **Cost**: Free. The WMO maintains this as a public resource for international cooperation.
-   **Licensing**: Generally open for use in meteorological and climate research, though specific attribution to the WMO is required.
-   **Rate Limits**: There are no strictly published rate limits for public read access, but bulk downloads should be staggered. For large-scale system integration, the WMO provides a "Web Client Tool" for batch processing.

### Approximate Dataset Size
-   **Station Count**: ~11,000 primary land stations, ~1,300 radiosonde sites, and tens of thousands of marine/mobile platforms (ships, buoys, aircraft). Total platforms likely exceed 50,000.
-   **Storage Estimate**: 1GB to 5GB for a full local mirror of all detailed XML/JSON station reports. Search result metadata (CSV/JSON) is much smaller (under 100MB).

### Estimated Effort for Scraper/Download Script
-   **Effort**: **Medium**.
-   **Complexity**: The OSCAR/Space JSON API is very simple to scrape. The OSCAR/Surface API requires a two-step process: 
    1.  Querying search results to obtain a list of WIGOS Station IDs (WSIs).
    2.  Iterating through the IDs to download individual station reports in WMDR XML format.
-   **Parsing**: Parsing the WMO-No. 1192 XML schema is non-trivial due to its depth, but provides extremely rich metadata (e.g., sensor height, uncertainty, calibration history).

---

## 4. Conclusion
WMO OSCAR is a "Tier 1" dataset for a local knowledge graph. It connects abstract climate statistics to physical sensors and locations on the planet. A scraper would ideally target the JSON summaries for rapid search indexing and selectively pull the full XML reports for high-priority stations.
