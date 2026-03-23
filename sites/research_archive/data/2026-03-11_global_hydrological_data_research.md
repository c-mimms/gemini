---
title: "Global Hydrological Data (GRDC / HydroSHEDS)"
date: 2026-03-11
category: "Earth & Environment"
tags: ["hydrology", "rivers", "watersheds", "water", "grdc"]
---

# Research Report: Global Hydrological Data (Rivers, Lakes, Dams, and Runoff)

**Date**: 2026-03-11  
**Topic**: Global Hydrological Data Research for Knowledge Graph Construction  
**Researcher**: Gemini CLI  

---

## 1. Brainstorming: Novel Dataset Ideas
The following dataset types were brainstormed as potential candidates for local knowledge graph integration:
1.  **Global Hydrological Data**: Comprehensive mapping of rivers, lakes, dams, catchments, and historical runoff. (Selected for Research)
2.  **Human Genomics and Proteomics**: Structural and functional data on human genes and proteins (e.g., UniProt, PDB, ClinVar).
3.  **Cryptographic Standards and Vulnerabilities**: Factual data on encryption algorithms, security protocols, and historical CVE data.
4.  **International Postal and Address Standards**: Geographic data on postal codes, administrative divisions, and addressing formats (Universal Postal Union).
5.  **Historical Sports Statistics**: Complete records of major international competitions like the Olympics, FIFA World Cup, and professional leagues.

---

## 2. Selected Idea: Global Hydrological Data
This research focuses on identifying high-resolution, factual datasets that describe the Earth's freshwater systems. This data is critical for spatial reasoning and answering complex questions about geography, environment, and infrastructure.

---

## 3. Research Findings

### A. Primary Data Sources
1.  **HydroSHEDS (Hydrological data and maps based on SHuttle Elevation Derivatives at multiple Scales)**
    *   **Description**: Provides global hydrographic information including river networks, watershed boundaries, and drainage directions.
    *   **Sub-products**:
        *   **HydroRIVERS**: A global vectorized line network of river reaches.
        *   **HydroLAKES**: A global database of 1.4 million lakes (area > 10 ha).
        *   **HydroBASINS**: Hierarchical sub-basin boundaries.
        *   **HydroATLAS**: Links hydrographic data with 50+ socio-environmental attributes (climate, land cover, population).
    *   **URL**: [https://www.hydrosheds.org/](https://www.hydrosheds.org/)

2.  **Global Reservoir and Dam Database (GRanD)**
    *   **Description**: Detailed information on 7,320 large dams and their associated reservoirs, including name, location, capacity, and purpose.
    *   **URL**: [https://www.globaldamwatch.org/directory](https://www.globaldamwatch.org/directory)

3.  **Global Runoff Data Centre (GRDC)**
    *   **Description**: Historical river discharge (runoff) data from over 10,000 gauging stations globally.
    *   **URL**: [https://portal.grdc.bafg.de/](https://portal.grdc.bafg.de/)

### B. Data Format
*   **Vector Data**: Most datasets (HydroRIVERS, HydroLAKES, GRanD) are available as **ESRI Shapefiles (.shp)** or **File Geodatabases (.gdb)**.
*   **Raster Data**: Drainage directions and flow accumulation (HydroSHEDS) are provided in **GeoTIFF** or **ESRI GRID** formats.
*   **Tabular Data**: Runoff data (GRDC) and attributes (HydroATLAS) are often in **CSV**, **XLSX**, or **TXT** formats.

### C. Licensing, Rate Limits, and Costs
*   **HydroSHEDS/RIVERS/LAKES**: Free for both non-commercial and commercial use. Requires attribution. No specific rate limits as files are downloaded in bulk.
*   **GRanD**: Free for research and educational purposes. Attribution is mandatory.
*   **GRDC**: **Strictly non-commercial**. Redistribution is prohibited. Access requires a manual request via a portal; data is delivered within ~24 hours via email. Bulk "database-wide" downloads are generally restricted without special WMO consent.

### D. Dataset Size
*   **HydroRIVERS (Global)**: ~800 MB - 1 GB (compressed).
*   **HydroLAKES (Global)**: ~800 MB (compressed).
*   **HydroSHEDS v1 (90m resolution)**: Several GBs when decompressed.
*   **HydroSHEDS v2 (30m resolution)**: Expected to be ~9x larger than v1 (staged release started in 2024/2025).
*   **GRanD**: Very small (tens of MBs).
*   **HydroATLAS**: Several GBs for full global attributes.

### E. Estimated Effort to Scrape/Download
*   **Effort: Low to Moderate.**
*   Most HydroSHEDS products are available as direct HTTP downloads. A simple `wget` or `python` script using `requests` can automate the retrieval of continental or global tiles.
*   GRDC requires a semi-automated approach (filling out a web form) which may be difficult to fully automate without browser-based automation (e.g., Selenium/Playwright) and manual oversight for the approval process.

---

## 4. Conclusion & Value for Knowledge Graph
Integrating global hydrological data would allow the local knowledge graph to perform advanced spatial and relational queries, such as:
*   "Trace the path of the Blue Nile from its source to the Mediterranean."
*   "Which dams are located on the Mekong River?"
*   "List all lakes in Canada with a surface area greater than 500 square kilometers."
*   "What is the average annual discharge of the Congo River at its mouth?"

This data is foundational for any AI agent tasked with understanding the physical world, resource management, or environmental science.
