# Research Report: Geological Events (Earthquakes & Volcanism)

**Date:** 2026-03-06  
**Topic:** Geological Events (Global Earthquakes and Volcanic Eruptions)  
**Status:** Completed

---

## 1. Brainstorming: Novel Dataset Ideas

The following dataset types were brainstormed as potential high-value sources for a local knowledge graph:

1.  **Global Historical Conflict Data (ACLED)**: Detailed records of armed conflict events, dates, locations, actors, and fatalities.
2.  **Human Protein Atlas / Genetic Variants (ClinVar)**: Scientific data on human proteins, tissue expression, and genetic associations with diseases.
3.  **Global Agricultural Statistics (FAOSTAT)**: Detailed data on crop production, livestock, food security, and agricultural trade by country/year.
4.  **World Heritage Sites & Protected Areas (UNESCO/WDPA)**: Geospatial and descriptive data on cultural and natural heritage sites.
5.  **Geological Events (Earthquakes & Volcanism)**: [SELECTED] Historical and real-time records of seismic and volcanic activity worldwide.

---

## 2. Selected Idea Research: Geological Events

### 2.1 Overview
This dataset encompasses global seismic events (earthquakes) and volcanic activity (eruptions and emissions). It provides a deep factual record of Earth's geological history, which is essential for a knowledge graph capable of answering historical, geographical, and scientific questions.

### 2.2 Data Sources & URLs

#### **USGS Earthquake Catalog (ComCat)**
*   **Source:** United States Geological Survey (USGS).
*   **Primary API Endpoint:** [FDSN Event Web Service](https://earthquake.usgs.gov/fdsnws/event/1/)
*   **Search Interface:** [USGS Earthquake Search](https://earthquake.usgs.gov/earthquakes/search/)
*   **Real-time Feeds:** [GeoJSON Feed](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)

#### **Global Volcanism Program (GVP)**
*   **Source:** Smithsonian Institution.
*   **Main Website:** [volcano.si.edu](https://volcano.si.edu)
*   **Interactive Data App:** [E3 App (Earthquakes, Eruptions, Emissions)](https://volcano.si.axismaps.io/)
*   **Bulk Exports:** Often found on the "Download Data" sections or via mirrors like NOAA (NCEI).

### 2.3 Data Formats
*   **USGS:** GeoJSON, CSV, KML, QuakeML (XML), and Text.
*   **GVP:** CSV, GeoJSON, Shapefile (for GIS), XML, and ASCII.

### 2.4 Licensing, Costs, and Restrictions
*   **USGS:** 
    *   **License:** Public Domain (U.S. Government work). No copyright restrictions.
    *   **Cost:** Free.
    *   **Attribution:** Requested but not legally required.
*   **GVP:** 
    *   **License:** Public Domain (Smithsonian Institution).
    *   **Cost:** Free.
    *   **Restrictions:** **Mandatory citation** is required for any use of the data. Specific citation formats are provided on their website.

### 2.5 Dataset Size & Rate Limits
*   **Size:** 
    *   **Earthquakes:** A 20,000-event CSV is ~2–5 MB; GeoJSON is ~10–20 MB. The full global catalog (1900–present) is several hundred MBs (CSV) to several GBs (GeoJSON).
    *   **Volcanoes:** The Holocene Volcano List and Eruption history are relatively small (tens of megabytes).
*   **Rate Limits:** 
    *   **USGS:** Single query limit of **20,000 events**. For larger downloads, requests must be "chunked" by time (e.g., month-by-month or year-by-year).
    *   **GVP:** No explicit rate limit for manual downloads, but automated scraping should be respectful.

### 2.6 Estimated Effort for Scraping/Downloading
*   **USGS:** **Low.** A simple Python script using `requests` can iterate through a date range (e.g., 1900-2026) and save monthly CSV files.
*   **GVP:** **Low to Moderate.** While structured CSVs are available via the E3 app, some deeper descriptive data may require custom scraping of individual volcano profile pages on `volcano.si.edu`.

---

## 3. Conclusion & Next Steps
The geological events dataset is an excellent candidate for local storage. It is well-structured, publicly available without cost, and provides high-density factual information.

**Next Action:** Develop a Python script to chunk the USGS historical catalog and download the Smithsonian's Holocene Eruption list as a baseline for the Knowledge Graph's geological layer.
