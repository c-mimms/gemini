# Knowledge Graph Data Research: Global Urban Transit Schedules (GTFS)

**Date:** 2026-03-18
**Topic:** Global Urban Transit Schedules (GTFS)
**Researcher:** Gemini CLI

---

## 1. Brainstormed Ideas
Below are the novel dataset types brainstormed for this research cycle:

1.  **Global Urban Transit Schedules (GTFS)**: Comprehensive schedules, routes, and stop data for buses, metros, trains, and ferries worldwide. High value for spatial and connectivity analysis.
2.  **Barcode of Life Data System (BOLD)**: A global database of DNA sequences used for species identification (DNA barcoding). Provides a deep biological layer for a knowledge graph.
3.  **Global High-Resolution Population Density (GHSL/WorldPop)**: Gridded population data mapping exactly where people live at a 100m to 1km resolution globally.
4.  **Global Chemical Regulatory & Safety Data (GHS/ECHA)**: Safety Data Sheets (SDS) and official chemical classifications (GHS) for millions of substances.
5.  **Historical Newspaper Digital Archives (Metadata/OCR)**: Bulk access to historical news text (e.g., Chronicling America, Trove) for building event timelines and NLP analysis.

**Selected Idea for Deep Research:** Global Urban Transit Schedules (GTFS)

---

## 2. Selected Idea: Global Urban Transit Schedules (GTFS)

### Overview
GTFS (General Transit Feed Specification) is the industry-standard format for public transit schedules and associated geographic information. A local knowledge graph containing this data can answer complex questions about urban mobility, connectivity between landmarks, and the temporal accessibility of different regions.

### Research Findings

#### Where can this data be obtained?
*   **Mobility Database (MobilityData):** The primary official successor to TransitFeeds. It provides a [GitHub catalog](https://github.com/MobilityData/mobility-database-catalogs) in CSV and JSON formats containing direct URLs to thousands of agency feeds.
*   **Transitland:** A community-driven platform that "atomizes" GTFS data into a searchable database. It offers a GraphQL and REST API for querying specific routes, stops, and operators across agencies.
*   **National Portals:** Many countries maintain high-quality national aggregators:
    *   **France:** [transport.data.gouv.fr](https://transport.data.gouv.fr/)
    *   **UK:** [Bus Open Data Service (BODS)](https://www.bus-data.dft.gov.uk/)
    *   **USA:** Individual agency portals (MTA, LA Metro, etc.) and the National Transit Database (NTD).

#### What is the format of the data?
*   **Primary Format:** ZIP files containing a set of relational CSV files (`.txt`).
*   **Key Files:**
    *   `stops.txt`: Names and lat/long coordinates of every transit stop.
    *   `routes.txt`: Higher-level grouping of trips (e.g., "Line 1").
    *   `trips.txt`: Specific occurrences of a route.
    *   `stop_times.txt`: The core schedule (which trip stops where and when).
    *   `calendar.txt`: Service availability (weekdays vs. weekends).
    *   `shapes.txt`: (Optional) Precise polyline coordinates for the transit routes.

#### Rate limits, licensing, or costs?
*   **Licensing:**
    *   **Metadata:** The catalogs (Mobility Database) are typically CC0.
    *   **Feeds:** Licensing varies by agency. Most use **CC-BY** (Attribution required) or the **Open Database License (ODbL)**. Some major agencies (e.g., Transport for London) require a free API key and agreement to specific terms.
*   **Costs:** Generally free to download for research and personal use.
*   **Rate Limits:** High-volume aggregators like Transitland have API rate limits, but direct downloads from agency URLs or S3 buckets usually only have standard HTTP limits.

#### How large is the dataset approximately?
*   **Current Global Snapshot:** Approximately **150 GB - 250 GB** (uncompressed) for all ~2,500+ active open feeds worldwide.
*   **Historical Archives:** If tracking every version change over several years, the data grows into the **1 TB - 5 TB** range.
*   **Individual Feed Size:** Varies from a few Kilobytes for small town bus systems to 500 MB+ for massive networks like NYC or London.

#### Estimated effort to write a scraper or download script?
*   **Effort Level:** Medium.
*   **Technical Steps:**
    1.  Parse the Mobility Database CSV to get a list of active URLs.
    2.  Write a robust downloader that handles redirects, SSL issues, and provides progress tracking.
    3.  Implement a parser (using Python libraries like `partridge` or `gtfslib`) to validate the ZIP contents.
    4.  Load the data into a relational database. **PostgreSQL with PostGIS** is highly recommended for transit data due to its spatial capabilities.
    5.  Handle updates: GTFS feeds expire and are updated frequently (weekly or monthly).

---

## 3. Conclusion & Recommendation
The GTFS dataset is one of the most factual and structured "real-world" datasets available. It is highly recommended for the local knowledge graph as it provides a permanent record of how cities are physically connected. 

**Next Steps:**
1.  Develop a Python script to fetch the Mobility Database catalog.
2.  Prototype a downloader for a subset of major cities (e.g., New York, London, Paris, Tokyo).
3.  Design a schema to link GTFS stops to other knowledge graph entities like POIs (Points of Interest) and street addresses.
