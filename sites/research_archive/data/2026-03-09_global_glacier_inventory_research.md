---
title: "Global Glacier Inventory (RGI)"
date: 2026-03-09
category: "Earth & Environment"
tags: ["glaciers", "climate-change", "cryosphere", "gis", "hydrology"]
---

# Research Report: Global Glacier Inventory (RGI 7.0)

**Date**: 2026-03-09
**Topic**: Global Glacier Inventory (Randolph Glacier Inventory - RGI 7.0)
**Researcher**: Gemini CLI

---

## 1. Brainstorming: Novel Dataset Types
The following dataset types were brainstormed for potential inclusion in the local knowledge graph:

1.  **Global Glacier Inventory (RGI 7.0)**: Comprehensive geospatial data on the world's glaciers (excluding ice sheets), including outlines, area, and elevation.
2.  **Global Dam Inventory (GRanD)**: Detailed data on over 7,000 large dams worldwide, including location, height, purpose, and reservoir capacity.
3.  **Global River Basins and Hydrography (HydroSHEDS/HydroBASINS)**: High-resolution data on watersheds, river networks, and drainage basins.
4.  **Global Soil Properties (SoilGrids)**: Deeply researched maps of soil composition, pH, organic matter, and characteristics at multiple depths.
5.  **International Seismological Centre (ISC) Event Catalogue**: A definitive record of global seismic events (earthquakes) with detailed parametric data.

**Selected Idea for this Task**: **Global Glacier Inventory (RGI 7.0)**

---

## 2. Research Findings: Global Glacier Inventory (RGI 7.0)

### Where can this data be obtained?
The primary source for the Randolph Glacier Inventory (RGI) is the **National Snow and Ice Data Center (NSIDC)**.
*   **Direct Link**: [NSIDC RGI 7.0 Data Portal](https://nsidc.org/data/f6jmovy5navz/versions/7)
*   **Alternative Source**: [GLIMS.org](https://www.glims.org/RGI) (Global Land Ice Measurements from Space).

### What is the format of the data?
The dataset is provided in several formats to accommodate GIS and analytical needs:
*   **Geospatial Outlines**: ESRI **Shapefiles** (`.shp`) for glacier boundaries.
*   **Attributes**: **CSV** files containing metadata for each glacier (name, area, elevation range, etc.).
*   **Metadata**: **JSON** and XML (ISO 19115) formats.
*   **Ancillary Data**: Gridded products available in **GeoTIFF**.

### Rate limits, Licensing, and Costs
*   **Licensing**: Distributed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.
*   **Cost**: Free of charge for research and public use.
*   **Rate Limits**: No significant rate limits for bulk downloads, though registration with Earthdata (NASA) may be required for some NSIDC portals.

### Estimated Size
*   **Compressed**: Approximately **1.5 GB to 2.0 GB** for the full global dataset.
*   **Decompressed**: May expand to several gigabytes depending on the inclusion of high-resolution shapefiles.
*   **Regional Granularity**: The data is partitioned into 19 first-order regions, allowing for partial downloads (e.g., Central Asia, Southern Andes).

### Estimated Effort for Scraping/Downloading
*   **Effort**: **Low**. 
*   **Mechanism**: The data can be downloaded via direct HTTPS or FTP links provided by NSIDC. A simple `wget` or `curl` script can automate the retrieval of regional or global ZIP files. No complex scraping is required as the data is served as static archives.

---

## 3. Potential for Knowledge Graph Integration
Integrating RGI 7.0 into the knowledge graph allows for:
- Spatial queries identifying glaciers by proximity to mountains or river basins.
- Temporal analysis of glacier extent when combined with older RGI versions (RGI 6.0).
- Hydrological modeling linking glacier melt-water to regional water resources.
