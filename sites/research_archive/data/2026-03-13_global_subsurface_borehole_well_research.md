---
title: "Global Subsurface Borehole & Well Data"
date: 2026-03-13
category: "Earth & Environment"
tags: ["geology", "borehole", "groundwater", "subsurface", "drilling"]
---

# Knowledge Graph Research: Global Subsurface Borehole and Well Data
**Date:** 2026-03-13
**Topic:** Subsurface Borehole and Well Data
**Status:** Completed

---

## 1. Brainstormed Ideas
For this research cycle, I brainstormed 5 novel dataset types for a local knowledge graph:
1.  **Global Dam and Reservoir Database (GRanD)**: High-resolution data on large dams, including storage, year built, and environmental impacts.
2.  **Linguistic Etymology and Word History**: Cross-linguistic data on the origins and evolution of core vocabularies.
3.  **Global Rare Earth Element (REE) Supply Chain**: Locations, refinery capacities, and corporate ownership of critical mineral sites.
4.  **Global Subsurface Borehole and Well Data**: High-fidelity geological and hydrological records from deep earth sampling. (SELECTED)
5.  **Historical Oceanographic Cruise Data**: Century-long records of deep-sea temperature, salinity, and biogeochemistry.

---

## 2. Selected Idea: Global Subsurface Borehole and Well Data
This dataset provides a 3D perspective of the Earth's crust, focusing on groundwater levels, geological stratigraphy (layers), and geophysical well logs (rock properties). This is a "foundational" dataset for understanding global resources, geological history, and hydrological health.

---

## 3. Research Findings

### Where can this data be obtained?
*   **Curated Global Dataset (Jasechko et al. 2024)**: 
    *   **Source:** [Zenodo Repository (10.5281/zenodo.10003697)](https://doi.org/10.5281/zenodo.10003697)
    *   **Description:** Covers 170,000+ monitoring wells in over 40 countries across 1,600+ aquifer systems.
*   **OSDU Open Test Data (Equinor Volve & TNO)**:
    *   **Source:** [OSDU GitLab (Open Test Data)](https://community.opengroup.org/osdu/data/data-definitions/open-test-data)
    *   **Description:** Professional-grade subsurface models including well logs, seismic data, and stratigraphic markers.
*   **Regional Open Data APIs**:
    *   **USGS (USA):** [Monitoring Locations API](https://api.waterdata.usgs.gov/ogcapi/v0/collections/monitoring-locations)
    *   **BGS (UK):** [Single Onshore Borehole Index (SOBI) OGC API](https://api.bgs.ac.uk/boreholes/v1/)
    *   **IGRAC (Global):** [GGIS Data Download portal](https://ggis.un-igrac.org/ggmn/data_download/)

### What is the format of the data?
*   **Point Data (Groundwater Levels):** Primarily **CSV** or **XLSX**.
*   **Well Logs (Geophysics):** **LAS (Log ASCII Standard)** versions 1.2 or 2.0. This is a structured text format for depth-indexed sensor data.
*   **Geospatial (Aquifer Boundaries):** **Shapefiles**, **GeoJSON**, or **KML**.
*   **API Output:** **REST (JSON)**, **WFS (XML/GML)**, or **OGC API** formats.

### Rate limits, licensing, and costs?
*   **Jasechko 2024 Dataset:** CC-BY 4.0 (Open Access). No cost.
*   **OSDU/Volve/TNO:** Open license for research and testing purposes.
*   **BGS/USGS APIs:** Free public access, though heavy bulk downloads may require API keys or staggered requests to avoid throttling.
*   **IGRAC GGIS:** Free, but requires account registration for full bulk access.

### Approximate Dataset Size?
*   **Jasechko 2024 (170k wells):** ~1GB for the core CSV/table files.
*   **OSDU Volve/TNO Test Data:** ~5-20GB for well logs, seismic files, and interpretations.
*   **Full Regional Repositories (USGS/BGS):** TBs of raw scanning/sensor data, but the metadata and markers are typically in the GB range.

### Estimated Scraping/Download Effort?
*   **Effort Level:** **Low to Medium**.
*   **Tools:**
    *   **`lasio` (Python library):** Can parse LAS files into Pandas DataFrames with 3-4 lines of code.
    *   **`requests` or `geopandas`:** For fetching API data and handling spatial boundaries.
    *   **`zenodo-get`:** For bulk downloading files from the Zenodo repository.
*   **Complexity:** The main challenge is standardizing different regional naming conventions for geological layers (stratigraphy).

---

## 4. Conclusion and Next Steps
The **Jasechko 2024 Zenodo dataset** is the most "plug-and-play" option for a knowledge graph, as it is already curated and globally distributed. The **OSDU Volve dataset** provides high-fidelity depth into how individual wells are structured, making it perfect for training models or building detailed 3D knowledge nodes.

**Next Step Recommendation:** Write a downloader script for the Zenodo Jasechko dataset to ingest the first 170,000 global well locations and their historical depth trends.
