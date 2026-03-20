# Research Report: Global Mineral Resources and Rare Earth Deposits

**Date**: 2026-03-08
**Topic**: Global Mineral Resources and Rare Earth Deposits
**Goal**: Evaluate the feasibility of scraping/downloading a comprehensive dataset of mineral resources and rare earth deposits for a local knowledge graph.

---

## 1. Brainstormed Ideas
Below are the novel dataset types considered for this research task:

1.  **Global High-Speed Rail Networks & Infrastructure**: Detailed spatial data on rail corridors, speeds, and rolling stock specifications globally.
2.  **Archaeological Sites and Excavations (Public Records)**: Datasets of documented archaeological finds, site locations (where public), and artifact catalogs.
3.  **Global Mineral Resources and Rare Earth Deposits** (Selected): Specific locations of known mineral occurrences, mine production history, and reserve estimates.
4.  **Historical Satellite Imagery Metadata**: A catalog of satellite launches, orbits, and available imagery footprints (not the images themselves).
5.  **International Radio Frequency Allocations**: A global map/database of how the EM spectrum is allocated by country and service type.

---

## 2. Selected Idea: Global Mineral Resources and Rare Earth Deposits
This dataset was selected because it provides critical factual knowledge for geopolitical, economic, and geological analysis. Rare earth minerals, in particular, are of high strategic value.

### 2.1 Where can this data be obtained?
*   **USGS Mineral Resources Data System (MRDS)**: [USGS MRDS Website](https://mrdata.usgs.gov/mrds/). This is a global database of mineral resource reports.
*   **Mindat.org (OpenMindat API)**: [api.mindat.org](https://api.mindat.org). Mindat is the world's largest mineralogy database and locality index.
*   **British Geological Survey (BGS)**: Provides "World Mineral Production" statistics and spatial data for the UK and international regions.
*   **Natural Resources Canada (NRCan)**: Provides specific data for Canadian mineral deposits.

### 2.2 What is the format of the data?
*   **USGS MRDS**: Available in **CSV**, **Shapefile**, **KML**, and **ESRI File Geodatabase**. It is also accessible via OGC web services (WMS/WFS).
*   **Mindat**: Provided in **JSON** format via their REST API.
*   **BGS**: Typically provided as **PDF** reports (for production stats) or **Shapefiles** for spatial data.

### 2.3 Licensing, Rate Limits, and Costs
*   **USGS**: Public Domain. Data is free to use and distribute without restriction (attribution requested).
*   **Mindat**: 
    *   **License**: Moving toward **CC BY-SA** for core scientific data. Database structure itself is copyrighted.
    *   **Access**: Requires a "Level 1" account and a manual application for an API key. 
    *   **Limits**: Employs standard rate-limiting. Automated scraping of the web UI is prohibited; the API is the only sanctioned method.
*   **BGS**: Some data is Open Government License (OGL), but some premium datasets require a fee or specific licensing for commercial use.

### 2.4 Approximate Size of the Dataset
*   **USGS MRDS**: Approximately **304,643 records**. While the file size for a CSV is manageable (~500MB - 1GB), the relational complexity (35 linked tables) makes it a dense dataset.
*   **Mindat**: Millions of records (minerals, localities, photos). A full extract is not provided as a single dump, but filtered queries can yield large JSON payloads.

### 2.5 Estimated Effort for Scraping/Downloading
*   **USGS (Low Effort)**: Bulk download links are readily available. A simple Python script or even `wget` can retrieve the entire MRDS in minutes. Parsing the relational structure (if using FileGDB) would require `geopandas` or `fiona`.
*   **Mindat (Medium Effort)**: Requires applying for an API key and writing a script to paginate through results. Since Mindat is highly structured, mapping it to a knowledge graph is straightforward but requires respect for rate limits.

---

## 3. Conclusion
The **USGS MRDS** is the best starting point for a local knowledge graph due to its public domain status and ease of bulk access. Integrating **Mindat** via API would provide a much deeper level of detail (e.g., specific mineral properties and locality history) but requires a more complex implementation and approval for access.

---
**Status**: Ready for Scraper Development (USGS) or API Integration (Mindat).
