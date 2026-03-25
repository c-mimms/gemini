# Research Report: Global Education Statistics and School Locations

## Brainstorming
As part of the ongoing effort to build a comprehensive local knowledge graph, the following novel dataset types were brainstormed:
1. **Global Waste Management and Landfill Infrastructure**: Data on landfill locations, capacity, and waste processing facilities.
2. **Global Education Statistics and School Locations**: Dataset of schools, universities, and educational attainment levels. (Selected)
3. **Global Industrial Clusters and Special Economic Zones**: Locations and types of industrial zones worldwide.
4. **Global Freshwater Quality and Monitoring Stations**: Real-time or historical data on river/lake water quality parameters.
5. **Global Forestry and Timber Production**: Data on forest cover types, logging concessions, and timber trade flows.

**Selected Idea**: **Global Education Statistics and School Locations**
This topic was selected because educational infrastructure is a fundamental component of societal factual knowledge. High-resolution school location data combined with educational indicators provides a rich layer for geographic and social analysis in a knowledge graph.

---

## Research Findings: Global Education Statistics and School Locations

### 1. Where can this data be obtained?
*   **UNICEF Giga & GeoSight**: The Giga initiative (joint UNICEF-ITU) aims to map every school in the world. 
    *   **Giga Maps**: [https://school-mapping.azurewebsites.net/](https://school-mapping.azurewebsites.net/)
    *   **GitHub**: [unicef/giga-global-school-mapping](https://github.com/unicef/giga-global-school-mapping) (includes data download scripts).
*   **OpenStreetMap (OSM)**: The most comprehensive crowdsourced database for schools globally.
    *   **Geofabrik**: [https://download.geofabrik.de/](https://download.geofabrik.de/) (Bulk extracts by region).
    *   **Overpass API**: Query `amenity=school` for real-time extraction.
*   **UNESCO Institute for Statistics (UIS)**: The primary source for global educational indicators and statistics.
    *   **Bulk Data Download Service (BDDS)**: [https://uis.unesco.org/en/bulk-data-download-service](https://uis.unesco.org/en/bulk-data-download-service)
*   **World Bank Education Data**: Aggregates national school censuses.
    *   **Data Catalog**: [https://datacatalog.worldbank.org/](https://datacatalog.worldbank.org/)
*   **National Portals**:
    *   **USA**: NCES EDGE (National Center for Education Statistics).
    *   **UK**: Get Information about Schools (GIAS).

### 2. What is the format of the data?
*   **Geospatial Data**: GeoJSON, Shapefile (SHP), and PBF (OpenStreetMap).
*   **Tabular Data**: CSV and Excel (often from UNESCO/World Bank).
*   **API Responses**: JSON (via UNICEF GeoSight or World Bank API).

### 3. Rate limits, licensing, and costs
*   **Licensing**:
    *   **OSM**: Open Database License (ODbL) - Free, requires attribution.
    *   **UNICEF Giga**: Generally shared as a "Public Good" (Open Data), often CC BY 4.0.
    *   **UNESCO/World Bank**: Open Data (CC BY 4.0).
*   **Costs**: None for open-access datasets.
*   **Rate Limits**: Overpass API (OSM) has rate limits for large queries; bulk downloads via Geofabrik are recommended for global extraction.

### 4. Approximate size of the dataset
*   **UNICEF Giga**: Currently maps over 2.1 million schools. A full CSV export is estimated at **200MB - 500MB**.
*   **OpenStreetMap (Global Schools)**: Filtered school data from the full PBF would likely be under **1GB** in GeoJSON format.
*   **UNESCO Indicators**: Aggregated statistics are relatively small, roughly **50MB - 100MB** for the full bulk set.

### 5. Estimated effort to write a scraper or download script
*   **Low**: For UNESCO, World Bank, and Geofabrik bulk downloads. These provide static links to flat files.
*   **Moderate**: For UNICEF Giga, utilizing their GitHub download scripts to automate the pull and processing.
*   **Moderate/High**: For building a unified global scraper that merges multiple national sources with OSM data to ensure maximum coverage and data cleaning.

---
**Date**: 2026-03-24
**Author**: Gemini Research Agent
