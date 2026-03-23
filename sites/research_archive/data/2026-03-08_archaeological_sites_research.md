---
title: "Global Archaeological Sites"
date: 2026-03-08
category: "History & Culture"
tags: ["archaeology", "history", "cultural-heritage", "gis", "antiquity"]
---

# Research Report: Global Archaeological Sites & Excavations

## Date: 2026-03-08

## Brainstormed Ideas
1.  **Classical Music Metadata & Scores (Musicology)**: Deep structured data on composers, compositions, instrumentation, and MusicXML/MIDI links.
2.  **Global Archaeological Sites & Excavations**: Structured data on historical sites, artifacts found, and excavation history (Arches project, Pleiades, Open Context, ARIADNEplus).
3.  **Space Mission Histories & Telemetry (COSPAR/NSSDCA)**: Detailed records of every satellite, probe, and manned mission since Sputnik, including trajectory data and mission objectives.
4.  **Global Hydrological Data (Rivers, Reservoirs, Dams)**: Real-time and historical water levels, flow rates, and infrastructure details for major river basins (GRDC, Global Dam Watch).
5.  **International Postal Codes & Geographic Boundaries**: High-resolution boundaries for every postal code globally (Geonames, OpenStreetMap based, or official gov data).

## Selected Idea: Global Archaeological Sites & Excavations
This dataset provides a foundation for spatial-temporal history in the knowledge graph. It allows for mapping civilizations, trade routes, and the progression of human settlement.

### Research Findings

#### 1. Where can this data be obtained?
- **Pleiades (Ancient Places Gazetteer)**: The primary source for ancient geography.
    - [Latest JSON Dump](http://atlantides.org/downloads/pleiades/json/pleiades-places-latest.json.gz)
    - [CSV Dumps](http://atlantides.org/downloads/pleiades/csv/)
- **Open Context**: Publishes primary field research data (excavation logs, zooarchaeology).
    - [Query API](https://opencontext.org/query/)
    - [GitHub Data Repository](https://github.com/ekansa/Open-Context-Data)
- **ARIADNEplus**: A massive European/Global aggregator of archaeological datasets.
    - [ARIADNE Portal](https://portal.ariadne-infrastructure.eu/)
    - SPARQL Endpoint for Linked Open Data.

#### 2. Format of the Data
- **Pleiades**: JSON (Comprehensive), CSV, RDF/Turtle.
- **Open Context**: JSON, CSV, XML, and specialized formats for 3D models/media.
- **ARIADNEplus**: RDF (Linked Data), Metadata in various schema (CIDOC-CRM).

#### 3. Rate Limits, Licensing, and Costs
- **Licensing**: 
    - **Pleiades**: Creative Commons Attribution 3.0 (CC-BY 3.0) or later.
    - **Open Context**: Generally CC-BY or CC0 (Public Domain).
    - **ARIADNEplus**: Varies by contributing institution, but metadata is usually open.
- **Costs**: Free for non-commercial research use.
- **Rate Limits**: Bulk downloads for Pleiades are unrestricted. Open Context API has standard rate limiting for high-frequency queries.

#### 4. Estimated Size
- **Pleiades**: ~100 MB (compressed) for the full gazetteer.
- **Open Context**: 1+ TB when including media (photos, 3D scans); the structured data alone is in the low Gigabyte range.
- **ARIADNEplus**: 100+ TB (Aggregated metadata, LiDAR, and 3D archives across dozens of partners).

#### 5. Estimated Effort to Scrape/Download
- **Pleiades**: **Low Effort**. A simple `wget` or `curl` script can retrieve the daily JSON dump. Parsing is straightforward JSON.
- **Open Context**: **Medium Effort**. Requires iterating through the API or cloning multiple GitHub repositories. Handling heterogeneous project data (zooarchaeology vs. ceramics) requires custom mapping.
- **ARIADNEplus**: **High Effort**. Requires SPARQL expertise and potentially handling large-scale metadata harvesting (OAI-PMH) from multiple endpoints.

## Conclusion
Pleiades is a high-priority "quick win" for the knowledge graph due to its small size and high-quality spatial data. Open Context and ARIADNEplus should be integrated incrementally, focusing first on metadata and structured tabular data before attempting to mirror heavy media assets.
