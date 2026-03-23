---
title: "Global Lighthouse Database"
date: 2026-03-15
category: "History & Culture"
tags: ["lighthouses", "maritime", "navigation", "coastal", "history"]
---

# Research Report: Global Lighthouse & Navigational Aids Database

**Date:** 2026-03-15
**Topic:** Global Lighthouse & Navigational Aids Database
**Researcher:** Gemini CLI

---

## 1. Brainstorming: Novel Dataset Ideas

The following dataset types were brainstormed as potential additions to the local knowledge graph:

1.  **Global Lighthouse Database**: A comprehensive collection of lighthouses, lightships, and major navigational aids worldwide, including geographic coordinates, light characteristics (flash patterns, colors), and historical context.
2.  **International Nuclear Reactor Information System (IAEA PRIS)**: Detailed technical and operational history of every nuclear power reactor globally, including construction dates, grid connections, and outage logs.
3.  **Olympic Games Historical Results (1896-Present)**: Every athlete, event, medal, and country participation record from the modern Olympic era.
4.  **Global Film & Cinema Metadata (Open Repositories)**: Cultural data covering filmography, release dates, genres, and production companies (alternatives to proprietary IMDB data).
5.  **Historical US Census Data (1790-1950)**: Demographic snapshots of the United States population over two centuries, now in the public domain.

**Selected Idea:** **Global Lighthouse Database**

---

## 2. Selected Idea Research: Global Lighthouse Database

### Overview
Lighthouses represent a unique intersection of maritime history, structural engineering, and navigational science. A global database of these structures provides high-value factual data for spatial analysis and historical record-keeping.

### Data Sources & Access
There are several high-quality sources for this data:

1.  **NGA List of Lights (National Geospatial-Intelligence Agency)**
    *   **Description:** The official US government publication (Pubs 110-116) covering lighthouses and fog signals outside the US.
    *   **Access:** Modern REST API.
    *   **URL:** `https://msi.pub.kubic.nga.mil/api/publications/ngalol/lights-buoys`
    *   **Format:** JSON.
    *   **Documentation:** [Swagger UI](https://msi.nga.mil/api/swagger-ui.html).

2.  **ARLHS World List of Lights (WLOL)**
    *   **Description:** Maintained by the Amateur Radio Lighthouse Society, listing over 15,000 lighthouses.
    *   **Access:** Searchable database and Wikidata property `P1630`.
    *   **URL:** [wlol.arlhs.com](https://wlol.arlhs.com/)
    *   **Format:** Can be extracted via Wikidata SPARQL queries or as historical `.dat`/`.csv` files.

3.  **OpenSeaMap / OpenStreetMap (OSM)**
    *   **Description:** Community-driven maritime data mapped on the OSM platform.
    *   **Access:** Overpass API for bulk extraction.
    *   **Format:** JSON, GeoJSON, XML.
    *   **Query Example:** `node["man_made"="lighthouse"]; out body;`

4.  **USCG Light List (US Coast Guard)**
    *   **Description:** Covers navigational aids within US territorial waters.
    *   **Access:** Weekly XML downloads.
    *   **URL:** [USCG NavCenter](https://www.navcen.uscg.gov/?pageName=lightLists)

### Data Format & Characteristics
*   **Format:** Predominantly **JSON** and **XML** from official sources; **CSV/GeoJSON** via community tools.
*   **Fields:** Name, Location (Lat/Long), Height, Focal Plane, Light Characteristic (e.g., "Fl W 5s"), Range (nautical miles), Structure Description, and unique IDs (NGA, ARLHS, Admiralty).

### Licensing, Costs, & Limits
*   **NGA & USCG:** Public Domain (US Government work). No cost, no licensing restrictions for redistribution.
*   **OpenStreetMap/OpenSeaMap:** Open Database License (ODbL). Requires attribution and "share alike" for modifications.
*   **ARLHS:** Generally open for personal/educational use; bulk redistribution may require permission or attribution.
*   **Rate Limits:** Standard API etiquette (avoiding aggressive polling) is required for NGA and Overpass servers.

### Estimated Dataset Size
*   **NGA Global List:** ~30,000 records.
*   **ARLHS List:** ~15,000 records.
*   **Combined Size:** Approximately **20-60 MB** in raw JSON/XML format. It is highly compressed and suitable for local storage.

### Implementation Effort
*   **Effort Level:** **Low to Medium**.
*   **Scraper/Downloader:** 
    *   A Python script using `requests` can easily pull the NGA data in one or two calls.
    *   A SPARQL query can fetch the ARLHS-linked Wikidata in seconds.
    *   The USCG XML files require a simple parser.
    *   Total development time for a unified aggregator: **4-6 hours**.

---

## 3. Conclusion
The Global Lighthouse Database is an excellent candidate for the knowledge graph. It provides global coverage, high-precision spatial data, and is available in machine-readable formats under favorable (often public domain) licensing.
