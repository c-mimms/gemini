---
title: "Global Dam & Reservoir Database (GRanD)"
date: 2026-03-14
category: "Technology & Infrastructure"
tags: ["dams", "reservoirs", "hydrology", "infrastructure", "water"]
---

# Research Report: Global Dam and Reservoir Database (GRanD & GDW)

**Date**: 2026-03-14  
**Topic**: Global Dam and Reservoir Data  
**Researcher**: Gemini CLI  

---

## 1. Brainstorming: Novel Dataset Ideas
The following dataset types were brainstormed as potential candidates for the local knowledge graph:

1.  **Global Lighthouse Database**: Historical and functional data about lighthouses worldwide (location, height, light characteristic, year built).
2.  **Global Underground Infrastructure (Non-Mining)**: Data on subways, bunkers, catacombs, and underground cities.
3.  **Global Forest Fire History**: Detailed records of wildfire events, including start date, cause, area burned, and vegetation type.
4.  **World Traditional Musical Instruments Database**: Technical specifications, cultural history, and acoustic properties of traditional instruments.
5.  **Global Dam and Reservoir Database (Selected)**: Comprehensive data on the world's dams and reservoirs, including engineering specs and environmental impact.

---

## 2. Selected Idea: Global Dam and Reservoir Database
Dams and reservoirs are critical components of global infrastructure, affecting water security, energy production, and ecosystem health. A local knowledge graph including this data can answer complex questions about river systems, hydroelectric potential, and regional water management.

---

## 3. Research Findings

### Where can this data be obtained?
There are several key sources for dam and reservoir data:
*   **Global Dam Watch (GDW)**: The successor to the GRanD database, providing a unified directory of several global datasets. 
    *   URL: [https://www.globaldamwatch.org/directory](https://www.globaldamwatch.org/directory)
*   **NASA SEDAC (Socioeconomic Data and Applications Center)**: Hosts the original Global Reservoir and Dam Database (GRanD).
    *   URL: [https://sedac.ciesin.columbia.edu/data/set/grand-v1-dams-rev01](https://sedac.ciesin.columbia.edu/data/set/grand-v1-dams-rev01)
*   **US National Inventory of Dams (NID)**: A very high-resolution dataset for the United States.
    *   URL: [https://nid.sec.usace.army.mil/](https://nid.sec.usace.army.mil/)
*   **ICOLD World Register of Dams (WRD)**: The most comprehensive global list (62,000+ dams) but requires a paid membership.
    *   URL: [https://www.icold-cigb.org/](https://www.icold-cigb.org/)

### What is the format of the data?
*   **Spatial Formats**: ESRI Shapefiles (.shp), GeoPackage (.gpkg), and KML/KMZ for visualization.
*   **Tabular Formats**: CSV and XLSX are commonly provided for attribute data.
*   **Attributes Included**: Dam name, river name, coordinates, year of construction, dam height, reservoir capacity, surface area, primary use (irrigation, hydro, etc.), and owner.

### Licensing, Rate Limits, and Costs
*   **GRanD / GDW**: Freely available for non-commercial and scientific use. Requires citation.
*   **US NID**: Public domain, free for all uses. No rate limits on bulk downloads.
*   **ICOLD WRD**: Restricted to members or those who purchase "access rights." Individual membership is approximately $50-$100 USD/year.

### Dataset Size
*   **GRanD (v1.3)**: ~7,320 records; ~50-150 MB (compressed) depending on the inclusion of high-res reservoir polygons.
*   **US NID**: ~91,000 records; CSV export is approximately 80-100 MB.
*   **ICOLD**: ~62,000 records; tabular data is relatively small (<50 MB).

### Estimated Effort to Scrape/Download
*   **Effort**: **Low**.
*   **Process**: 
    1.  Bulk downloads for GRanD and US NID are available directly via their respective portals. 
    2.  The US NID provides a direct "Download All" feature for CSV/GeoPackage.
    3.  GRanD/GDW requires a simple registration on NASA SEDAC or a direct download from Global Dam Watch.
    4.  No complex scraper is needed; a simple Python script using `requests` or `urllib` could automate the retrieval of these files if they were updated frequently.

---

## 4. Conclusion & Recommendation
The **Global Dam Watch** and **US National Inventory of Dams** datasets are excellent candidates for the local knowledge graph. They provide high-value, structured factual data with minimal acquisition effort. The US NID is particularly detailed for North American analysis, while GDW provides the necessary global context for major international river systems.
