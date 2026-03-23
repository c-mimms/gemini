---
title: "Global Power Grid Transmission Network"
date: 2026-03-19
category: "Technology & Infrastructure"
tags: ["power-grid", "electricity", "transmission", "energy", "infrastructure"]
---

# Research Report: Global High-Voltage Power Grid Transmission Lines & Substations

**Date:** 2026-03-19
**Topic:** Global Infrastructure / Energy Connectivity
**Status:** Completed

---

## 1. Brainstorming: Novel Dataset Ideas

The following dataset types were brainstormed as high-value, factual, and locally storable knowledge sources for a comprehensive local knowledge graph.

1.  **Global High-Voltage Power Grid Transmission Lines & Substations (SELECTED)**: Mapping the "edges" of the world's energy system—connecting power plants to demand centers via transmission networks.
2.  **World Port Index (NGA Pub 150)**: A definitive catalog of over 3,700 major ports worldwide, including physical attributes (depths, harbor size), facilities, and available services.
3.  **Global Geothermal Resource & Heat Flow Database**: Mapping the Earth's internal heat flow and geothermal potential using datasets from the International Heat Flow Commission (IHFC).
4.  **Global Scientific Reference Materials & Physical Standards**: Deep factual data on standard reference materials (SRMs), isotopic abundances, and physical constants from bodies like NIST and ISO.
5.  **Global Historical Currency Exchange Rates & Inflation Events**: Long-term longitudinal data on currency valuations, precious metal parities, and documented hyperinflationary periods.

---

## 2. Selected Idea Research: Global High-Voltage Power Grid Transmission Lines & Substations

### 2.1 Overview
While previous research focused on the *nodes* (Power Plants), this dataset provides the *topology*—the transmission and distribution lines that form the global power grid. This is critical for understanding infrastructure resilience, energy flows, and geographic connectivity.

### 2.2 Data Sources & URLs
*   **Gridfinder (World Bank/ESMAP)**: A high-resolution global model that combines OpenStreetMap data with night-time satellite imagery (VIIRS) and road networks to predict the location of the world's power grid.
    *   **Zenodo:** [doi.org/10.5281/zenodo.3660300](https://doi.org/10.5281/zenodo.3660300)
    *   **EnergyData.info:** [energydata.info/dataset/predicted-global-electricity-transmission-distribution-networks](https://energydata.info/dataset/predicted-global-electricity-transmission-distribution-networks)
*   **Open Infrastructure Map (OpenInfraMap)**: A live visualization of infrastructure data from OpenStreetMap.
    *   **Website:** [openinframap.org](https://openinframap.org)
*   **GridKit (Network Model)**: A toolkit for extracting topological models from OpenStreetMap.
    *   **GitHub:** [github.com/bdw/GridKit](https://github.com/bdw/GridKit)
    *   **Zenodo (2016 Extracts):** [doi.org/10.5281/zenodo.47317](https://doi.org/10.5281/zenodo.47317)

### 2.3 Data Formats
*   **Gridfinder:**
    *   **GeoPackage (.gpkg):** Vector data for the predicted line network (transmission and distribution).
    *   **GeoTIFF (.tif):** Raster data representing predicted targets (locations connected to the grid) and low-voltage infrastructure density.
*   **GridKit:**
    *   **CSV:** Tabular files (`vertices.csv` and `links.csv`) representing a graph topology.

### 2.4 Licensing, Costs, and Restrictions
*   **Gridfinder:** **Creative Commons Attribution 4.0 International (CC BY 4.0)**. Free for all uses with attribution.
*   **GridKit / OpenInfraMap:** **Open Database License (ODbL)**. Free to use, but derivative works must also be ODbL and attribute OpenStreetMap contributors.
*   **Cost:** All listed sources are free of charge.

### 2.5 Dataset Size & Scope
*   **Gridfinder (Global Bulk):** ~1.0 GB total.
    *   `grid.gpkg`: ~725 MB (Full vector network).
    *   `lv.tif` & `targets.tif`: ~280 MB (Rasters).
*   **GridKit (Europe & NA Extracts):** ~4 MB (Highly compressed topological models).
*   **Geographic Coverage:** Global, with the highest accuracy in regions with good OpenStreetMap and satellite coverage.

### 2.6 Key Data Fields (Gridfinder)
*   `source`: Indicates if the line is from OpenStreetMap (confirmed) or predicted by the model.
*   `geometry`: The linestring representing the physical path of the power line.
*   `voltage`: (Where available in OSM) The rated voltage of the transmission line.

### 2.7 Estimated Effort for Scraping/Downloading
*   **Downloading:** **Low.** Direct download links are available on Zenodo and EnergyData.info.
*   **Processing:** **Moderate.** Requires GIS libraries (e.g., GeoPandas, GDAL/OGR, or Fiona) to ingest and query the GeoPackage.
*   **KG Integration:** **High.** Converting the physical linestrings into a topological graph (Nodes and Edges) requires spatial join operations (e.g., finding which lines connect to which power plant locations).

---

## 3. Value for Knowledge Graph
Integrating the global power grid allows the knowledge graph to:
*   Perform network analysis to identify critical infrastructure nodes.
*   Visualize energy dependencies between different administrative regions.
*   Estimate the extent of electrification in remote or underserved areas.
*   Link "Power Plant" entities via "Transmission Line" edges to "Consumer Center" (Cities) nodes.
