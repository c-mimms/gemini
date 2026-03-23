---
title: "InterRidge Hydrothermal Vent Database"
date: 2026-03-14
category: "Earth & Environment"
tags: ["ocean", "hydrothermal-vents", "geology", "deep-sea", "marine"]
---

# Research Report: InterRidge Global Database of Active Submarine Hydrothermal Vent Fields

## Date
2026-03-14

## Goal
The goal of this research is to evaluate the **InterRidge Global Database of Active Submarine Hydrothermal Vent Fields** as a factual dataset for a local knowledge graph.

## Brainstormed Ideas
1.  **InterRidge Global Database of Active Submarine Hydrothermal Vent Fields**: Locations, geology, and geochemistry of hydrothermal vents.
2.  **Global Seamount and Knoll Distribution (Yesson et al.)**: Comprehensive GIS data on the physical distribution of seamounts.
3.  **Cold Seep Microbiomic Database (CSMD)**: Genomic and functional diversity of cold seep ecosystems.
4.  **International Nuclear Reactors Database (PRIS)**: Operational and historical data on nuclear power plants worldwide.
5.  **Global Lighthouse Database**: Historical and current data on lighthouses (characteristics, location, history).

## Selected Idea
**InterRidge Global Database of Active Submarine Hydrothermal Vent Fields**

## Research Findings

### 1. Where can this data be obtained?
The database is available through several official repositories:
-   **PANGAEA (Authoritative Repository)**: [https://doi.pangaea.de/10.1594/PANGAEA.917894](https://doi.pangaea.de/10.1594/PANGAEA.917894) (Version 3.4).
-   **InterRidge Online Database**: [https://vents-data.interridge.org/](https://vents-data.interridge.org/) - Allows for searching and direct export.
-   **Pacific Data Hub**: [https://pacificdata.org/](https://pacificdata.org/) - Provides metadata and alternate formats.
-   **Marine Geoscience Data System (MGDS)**: [http://www.marine-geo.org/](http://www.marine-geo.org/) - Integrated via web services.

### 2. What is the format of the data?
The database is highly structured and available in multiple formats:
-   **CSV / Tab-delimited**: Standard tabular format for all vent attributes.
-   **JSON / GeoJSON**: Available via Pacific Data Hub and MGDS web services.
-   **Shapefile (GIS)**: For spatial analysis in ArcGIS/QGIS.
-   **KML**: For visualization in Google Earth.
-   **RDF/XML**: For linked data applications.

### 3. Rate limits, licensing, or costs?
-   **Licensing**: **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC-BY-NC-SA-4.0)**.
    -   Requires attribution (Cite: Beaulieu, S.E., and Szafrański, K.M., 2020).
    -   Restricted to non-commercial use.
    -   ShareAlike requires derived works to use the same license.
-   **Costs**: Free for research and educational use.
-   **Rate Limits**: No explicit rate limits for bulk downloads from PANGAEA or InterRidge.

### 4. How large is the dataset approximately?
-   **Number of Records**: Approximately **700-1000** active or suspected vent fields (Version 3.4 has ~700).
-   **Size**: Extremely small for local storage. The CSV/JSON files are typically **< 2 MB**.

### 5. Estimated effort to write a scraper or download script?
-   **Effort**: **Very Low**.
-   Since bulk CSV and JSON downloads are provided directly by PANGAEA and Pacific Data Hub, no complex scraper is needed. A simple `curl` or `requests` call can fetch the latest version.
-   **GitHub Resource**: A Drupal export script is available at [sbeaulieu/vents-Drupal](https://github.com/sbeaulieu/vents-Drupal) if deeper integration is required.

## Conclusion
The InterRidge Vents Database is a high-value, factual, and compact dataset perfectly suited for a local knowledge graph. It provides precise coordinates, tectonic settings, and geological context for some of the most remote features on Earth.

---
**Bonus Finding: Seamounts and Cold Seeps**
Related datasets like **Yesson et al. (2011) Seamounts** (CC BY 3.0) and **ChEssBase/CSMD** (Cold Seeps) provide complementary GIS and biological data for a comprehensive deep-sea knowledge layer.
