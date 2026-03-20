# Knowledge Graph Research: Global Historical Tropical Cyclone and Tornado Tracks

**Date:** 2026-03-19
**Topic:** Global Historical Tropical Cyclone and Tornado Tracks (IBTrACS & NOAA SPC)
**Researcher:** Gemini CLI

---

## 1. Brainstormed Ideas
Below are 5 novel dataset types evaluated for inclusion in the local knowledge graph:

1.  **Global Historical Tropical Cyclone and Tornado Tracks (IBTrACS/NOAA)**: High-resolution spatial data on the exact paths, wind speeds, and pressures of historical storms. (Selected for this research).
2.  **Global Desalination Plant Database**: Detailed inventory of desalination infrastructure (Reverse Osmosis vs. Thermal, capacity, energy source).
3.  **Global Chemical Facility/Hazardous Materials Inventory (e.g., US TRI)**: Locations and reported chemical releases/storages for industrial sites worldwide.
4.  **OpenStreetMap (OSM) Power Grid Infrastructure**: A deep dive into the transmission lines, substations, and transformers that form the global power grid.
5.  **Global Seamount and Undersea Feature Names (GEBCO/SCUFN)**: Names, coordinates, and depths of all named features on the ocean floor.

---

## 2. Selected Idea: Global Historical Tropical Cyclone and Tornado Tracks
This dataset provides a comprehensive spatial and temporal record of extreme meteorological events. It allows the knowledge graph to answer questions about the history of disasters at specific geographic coordinates, correlate storm intensity with climate cycles, and map the trajectory of "named" historical events.

### Where can this data be obtained?
- **Tropical Cyclones (IBTrACS):** The International Best Track Archive for Climate Stewardship (IBTrACS) is the global gold standard.
    - **Portal:** [NCEI IBTrACS](https://www.ncei.noaa.gov/products/international-best-track-archive)
    - **Direct Access (v04):** `https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/`
- **USA Tornadoes (NOAA SPC):** The Storm Prediction Center provides the definitive U.S. record from 1950 to present.
    - **Portal:** [SPC Severe Weather GIS (SVRGIS)](https://www.spc.noaa.gov/gis/svrgis/)
    - **Direct Link:** `https://www.spc.noaa.gov/gis/svrgis/zipped/tornado.zip`
- **Canada Tornadoes:** Available via the Environment Canada Open Data portal.
- **Europe (ESWD):** The European Severe Weather Database (ESWD) provides structured data for European events (requires registration for bulk access).

### What is the format of the data?
- **IBTrACS:** Provides data in **CSV**, **netCDF**, and **Shapefile** formats. The CSV includes two header rows (column names and units).
- **NOAA SPC:** Provides **Shapefiles** (WGS84) and **CSV** files. The shapefiles include both "point" (touchdown) and "line" (path) geometries.
- **Coordinate System:** Standard **WGS84 (EPSG:4326)** is used for almost all spatial attributes.

### Are there any rate limits, licensing restrictions, or costs associated with scraping/downloading it?
- **Licensing:** Both IBTrACS and NOAA SPC are products of the U.S. Federal Government and are in the **Public Domain**.
- **Costs:** Completely free to download and redistribute.
- **Restrictions:** No strict rate limits for the FTP/HTTPS bulk downloads. Formal attribution to NOAA/NCEI is requested in publications/derivative works.
- **Caveat:** Historical data (pre-1950 for cyclones, pre-1970 for tornadoes) varies in quality and reporting standards (e.g., the transition to the Enhanced Fujita scale in 2007).

### How large is the dataset approximately?
- **Full Global IBTrACS CSV:** ~150–200 MB.
- **Full U.S. Storm Events (CSV):** ~500 MB to 1 GB (includes all storm types).
- **Historical Tornado Track Shapefiles:** ~50 MB.
- **Total Integrated Dataset:** Roughly **1–2 GB** for a comprehensive global historical record including all metadata and geometries.

### What would be the estimated effort to write a scraper or download script for this data?
- **Effort: Medium.**
- **Details:** 
    - **Download:** A simple shell script using `curl` or `wget` can retrieve the bulk files.
    - **Processing:** The primary complexity is spatial. To ingest this into a Knowledge Graph, one must:
        1.  Parse the multiple header rows in IBTrACS CSVs.
        2.  Convert track geometries (LineStrings) into a sequence of nodes or a spatial attribute.
        3.  Handle the "Best Track" logic where multiple agencies may report on the same storm (IBTrACS handles much of this, but the data includes agency-specific columns).
    - **KG Mapping:** Storm entities should be linked to `Time`, `Location` (Path), `Intensity` (Pressure/Wind), and `Impact` (Fatalities/Loss) nodes.

---

## 3. Implementation Strategy
1.  **Phase 1:** Download the Global IBTrACS CSV and the SPC Tornado Track shapefile.
2.  **Phase 2:** Use a Python script (Pandas/GeoPandas) to clean the data and normalize column names across the different sources.
3.  **Phase 3:** Extract "Storm" entities, using unique IDs like the IBTrACS `SID` or the SPC `om` (occurrence number).
4.  **Phase 4:** Generate RDF triples or Graph nodes connecting storms to the years, basins, and intensity levels they reached.
