---
title: "Global Railway Infrastructure"
date: 2026-03-09
category: "Technology & Infrastructure"
tags: ["railways", "transport", "infrastructure", "openstreetmap", "gis"]
---

# Research Report: Global Railway Infrastructure

## Date: 2026-03-09

## 1. Brainstorming: Novel Dataset Ideas
The following dataset types were brainstormed for potential inclusion in the local knowledge graph. These focus on high-value, factual, and structured data that can be stored locally.

1.  **Global Postal and Administrative Boundaries (Hierarchical)**: A deep dataset mapping postal codes to neighborhoods, cities, and administrative regions worldwide.
2.  **Global Dams and Reservoirs**: Technical specifications for dams (height, type, capacity) and the reservoirs they create, including river system associations.
3.  **Public Human Genetic Variants**: Aggregated factual associations (e.g., ClinVar) between genetic variants and phenotypes, excluding personal health information.
4.  **Global Railway Infrastructure (Selected)**: Comprehensive mapping of the world's railway tracks, stations, gauges, electrification status, and operators.
5.  **Historical Currency Exchange Rates**: Long-term longitudinal data of exchange rates across centuries for economic and historical analysis.

---

## 2. Selected Idea: Global Railway Infrastructure
**Why?**: Railway data is highly structured, spatial, and represents a critical layer of global logistics and history. It is essential for answering questions about transportation networks, connectivity, and infrastructure development.

### Research Findings

#### Where can this data be obtained?
- **OpenStreetMap (OSM) / OpenRailwayMap**: The most detailed source. It contains fine-grained data on tracks, signals, and stations.
- **World Food Programme (WFP) / Humanitarian Data Exchange (HDX)**: Provides a curated "Global Railways" dataset that is often easier to use for global analysis than raw OSM data.
- **Natural Earth**: Best for small-scale (low detail) global visualizations.
- **World Bank Data Catalog**: Provides datasets focused on infrastructure quality and economic impact.

#### What is the format of the data?
- **GeoJSON**: Widely used for spatial data; easy to parse in Python/JavaScript.
- **OSM PBF**: Compressed binary format for OpenStreetMap data; requires specialized tools (e.g., `osmium`, `osm2geojson`).
- **Shapefile (SHP)**: Standard GIS format, available via HDX and Natural Earth.
- **KML**: Available on HDX for Google Earth compatibility.

#### Licensing, Rate Limits, and Costs
- **OpenStreetMap**: Open Database License (ODbL). Free to use but requires attribution and "share-alike" for derivative works.
- **HDX (WFP)**: Typically CC-BY-IGO (Creative Commons Attribution International Organization). Free with attribution.
- **Natural Earth**: Public Domain. No restrictions.
- **Rate Limits**: Bulk downloads of OSM data (via Geofabrik or HDX) have no rate limits. Overpass API (for live querying) has usage limits.

#### Approximate Size of the Dataset
- **Global OSM Railway Data**: Filtered railway-only data from the global OSM planet file is approximately **1-2 GB** in PBF format and **5-10 GB** when converted to GeoJSON.
- **HDX Global Railways**: The Shapefile/GeoJSON from HDX is significantly smaller, around **200-500 MB**, as it simplifies some geometry and excludes technical signaling data.

#### Estimated Effort to Scrape/Download
- **Low Effort**: Downloading the global Shapefile from HDX and converting it to a local database (PostGIS or SQLite/SpatiaLite).
- **Moderate Effort**: Filtering the global OSM Planet file (60GB+) using `osmium` to extract only `railway` tags and converting to GeoJSON. This requires high RAM and CPU for the initial filter.
- **High Effort**: Building a custom scraper to pull station-specific metadata (e.g., photos, historical plaques) from Wikipedia or regional rail operator sites to augment the spatial data.

---

## 3. Conclusion
The **Global Railway Infrastructure** dataset is an excellent candidate for the knowledge graph. The most efficient path forward is to start with the **HDX Global Railways** dataset for a baseline, then supplement it with high-detail **OpenRailwayMap** data for specific regions of interest.
