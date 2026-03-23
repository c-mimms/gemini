---
title: "Global Pipeline Infrastructure"
date: 2026-03-18
category: "Technology & Infrastructure"
tags: ["pipelines", "oil-gas", "infrastructure", "energy", "gis"]
---

# Knowledge Graph Research: Global Pipeline Infrastructure

**Date**: 2026-03-18
**Topic**: Global Pipeline Infrastructure (Oil, Gas, Water)
**Researcher**: Gemini CLI

---

## 1. Brainstorming: Novel Dataset Ideas
The following dataset types were brainstormed as potential candidates for the local knowledge graph, focusing on factual, structured, and locally storable data:

1.  **Global Pipeline Infrastructure (Oil, Gas, Water)**: Spatial and technical data on transport networks. *[SELECTED]*
2.  **Global Particle Accelerator Database**: Specifications and locations of research, medical, and industrial accelerators.
3.  **Global Botanical Garden Collections (BGCI)**: Taxonomy and location data for ex-situ plant conservation, linking species to institutions.
4.  **Global Braille and Tactile Standards**: Linguistic and technical specifications for accessibility systems across countries.
5.  **Ethnobotanical Knowledge Bases**: Databases documenting the traditional medicinal and ritual uses of plants by various cultures.

---

## 2. Research Findings: Global Pipeline Infrastructure

### Overview
Pipeline infrastructure is a critical component of global energy and water security. Mapping these networks provides deep insights into resource flow, geopolitical dependencies, and environmental risks.

### Data Sources & Availability
1.  **Oil & Gas Pipelines**:
    *   **Global Energy Monitor (GEM)**: Provides the **Global Oil Infrastructure Tracker (GOIT)** and **Global Gas Infrastructure Tracker (GGIT)**. These are the gold standards for open-access pipeline data.
    *   **National Energy Technology Laboratory (NETL)**: Maintains the **Global Oil and Gas Infrastructure (GOGI)** database, a massive geodatabase with over 4.8 million records of wells, pipelines, and facilities.
2.  **Water & Wastewater Pipelines**:
    *   **OpenStreetMap (OSM)**: The most granular source for water distribution networks. Data can be extracted via Overpass Turbo using tags like `man_made=pipeline` + `substance=water`.
    *   **HydroSHEDS / HydroWASTE**: A spatially explicit global database of wastewater treatment plants and outfall locations.
    *   **Global Inter-Basin Hydrological Transfer Database**: Focuses on large-scale water transfer projects (canals and pipelines) between basins.

### Data Formats
*   **GEM**: CSV, Excel.
*   **NETL GOGI**: File Geodatabase (GDB), Shapefiles.
*   **OSM**: PBF, XML, GeoJSON (via conversion).
*   **HydroWASTE**: Shapefile, CSV.

### Licensing, Costs, and Rate Limits
*   **GEM**: CC BY 4.0 (Open Access).
*   **NETL**: Open Access / Public Domain.
*   **OSM**: ODbL (Open Database License).
*   **HydroWASTE**: CC BY 4.0.
*   **Costs**: None for the primary open-access versions.
*   **Rate Limits**: Standard API limits apply for Overpass Turbo (OSM), but bulk downloads (Planet.osm) have no limits.

### Dataset Size (Approximate)
*   **GEM Oil/Gas**: ~10-50 MB (Tabular).
*   **NETL GOGI**: ~1-5 GB (Spatial).
*   **OSM Pipeline Extracts**: ~500 MB - 2 GB (filtered for global pipelines).
*   **HydroWASTE**: ~100 MB.

### Estimated Effort to Scrape/Integrate
*   **GEM**: **Low**. Direct CSV downloads available.
*   **NETL**: **Medium**. Requires handling ESRI File Geodatabases and potentially large spatial joins.
*   **OSM**: **Medium-High**. Requires setting up a filtering pipeline (e.g., `osmium` or `osmosis`) to extract specific tags from the global planet file.
*   **Integration**: **Medium**. The primary challenge is de-duplicating and merging spatial geometries from different sources (e.g., where GEM and OSM overlap).

---

## 3. Conclusion & Recommendation
Global Pipeline Infrastructure is a high-value addition to the Knowledge Graph. It bridges the gap between natural resources (oil, gas, water) and human infrastructure. I recommend starting with the **Global Energy Monitor** datasets for energy and **OpenStreetMap filtered extracts** for water. These can be stored locally in a PostGIS-enabled database or as a set of GeoParquet files for high-performance querying.
