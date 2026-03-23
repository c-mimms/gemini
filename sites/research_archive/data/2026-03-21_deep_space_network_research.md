---
title: "NASA Deep Space Network (DSN)"
date: 2026-03-21
category: "Space & Astronomy"
tags: ["deep-space", "nasa", "dsn", "antenna", "space-communication"]
---

# 2026-03-21 Deep Space Network (DSN) & Space Communications Infrastructure Research

## Goal
To evaluate and document data sources for a local knowledge graph regarding the global infrastructure used for deep space and satellite communications, including ground stations, antennas, and real-time status.

## Brainstormed Ideas
1.  **Global UNESCO Intangible Cultural Heritage**: Data on traditions, rituals, and knowledge practices.
2.  **Global Deep Space Network (DSN) and Space Communications Infrastructure**: Locations, technical specs, and real-time status of deep space antennas and ground stations.
3.  **Global Historical Pandemic and Epidemic Outbreaks**: Spatio-temporal data on historical disease spread.
4.  **Global Research Vessel Fleet and Capabilities**: Data on scientific ships, equipment, and mission history.
5.  **Global Particle Accelerator Facilities and Specifications**: Locations and technical parameters of accelerators worldwide.

## Selected Idea
**Global Deep Space Network (DSN) and Space Communications Infrastructure**

## Research Findings

### 1. Primary Data Sources & Locations

| Source | Description | Access URL/Link |
| :--- | :--- | :--- |
| **NASA DSN Now** | Real-time status of all NASA DSN antennas (Goldstone, Madrid, Canberra). | [dsn.xml](https://eyes.jpl.nasa.gov/dsn/data/dsn.xml) |
| **find-gs.com** | Aggregated database of 650+ global ground stations (ESA, Commercial, University). | [Kaggle Dataset](https://www.kaggle.com/datasets/findgs/ground-station-dataset) |
| **SatNOGS Network** | Open-source global network of amateur and research ground stations. | [SatNOGS API](https://network.satnogs.org/api/) |
| **ITU SpaceExplorer** | Official global registry of Earth stations and satellite filings. | [ITU SpaceExplorer](https://www.itu.int/go/ITUSpaceExplorer) |
| **Space-Track.org** | Catalog of satellites and ground-based sensors for orbital tracking. | [Space-Track API](https://www.space-track.org/basicspacedata/query/) |
| **ESA OPS Portal** | Technical specifications and precise locations for ESA ESTRACK sites. | [ESA OPS Portal](https://ops.esa.int) |

### 2. Data Formats
- **NASA DSN:** XML (Real-time polling).
- **find-gs.com:** CSV (Bulk download via Kaggle).
- **SatNOGS:** JSON (RESTful API).
- **ITU BR IFIC:** MS Access (.mdb) or SQLite via ISO image; CSV via SpaceExplorer export.
- **Space-Track:** JSON, XML, CSV, TLE.

### 3. Rate Limits, Licensing, and Costs
- **NASA DSN Now:** Free and public. Polling every 5 seconds is standard.
- **SatNOGS:** Open API (CC-BY-SA 4.0 or similar open license usually applies to data).
- **Space-Track.org:** Requires registration. Rate limits: <30 requests/min, 300/hour.
- **ITU BR IFIC:** Full ISO/DVD requires a subscription (often free for TIES users/Member States). SpaceExplorer web tool allows limited free exports.
- **ESA Navigation Office:** High-precision geodetic data may require formal requests for academic/research use.

### 4. Approximate Dataset Size
- **Ground Station Lists:** Small (< 100 MB for global lists including technical specs).
- **NASA DSN History:** Medium (GBs if pulling historical telemetry/status over years).
- **ITU Registry:** Large (The full ISO is several GBs).

### 5. Estimated Scraper/Download Effort
- **Low:** Writing a script to download the Kaggle CSV or poll the DSN XML/SatNOGS API. 
- **Medium:** Parsing the ITU MS Access/SQLite databases and mapping them to a standard schema for the knowledge graph.
- **Medium:** Setting up a persistent collector for real-time DSN status to build a historical activity log.

## Conclusion
This dataset is highly structured and provides a unique "physical-to-digital" bridge for a knowledge graph. Combining the ITU's official regulatory data with NASA's real-time activity and SatNOGS's crowd-sourced data would create a comprehensive view of how Earth communicates with the solar system.
