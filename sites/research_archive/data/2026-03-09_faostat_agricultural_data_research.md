# Research Report: FAOSTAT (Global Agricultural and Food Statistics)
**Date:** 2026-03-09
**Topic:** FAOSTAT - Food and Agriculture Organization Corporate Statistical Database

---

## 1. Brainstormed Ideas
During the initial phase of this research, the following novel dataset types were considered:
1.  **Global Dam and Reservoir Inventory**: Comprehensive data on the world's dams, including height, capacity, and construction dates (e.g., GRanD database).
2.  **FAOSTAT (Global Agricultural and Food Statistics)**: Extensive data from the UN on crop production, livestock, food security, and agricultural trade across all countries. (**SELECTED**)
3.  **Global Medicinal Plant Knowledge**: Structured data on plant species used in traditional medicine, their chemical properties, and therapeutic uses.
4.  **OpenStreetMap POIs (Points of Interest)**: High-granularity data on global infrastructure like hospitals, libraries, and heritage sites.
5.  **International Space Launch History**: A complete record of every space launch, including launch vehicles, payloads, orbits, and mission status.

---

## 2. Selected Idea: FAOSTAT
FAOSTAT is the world's most comprehensive source of agricultural and food statistics. It is maintained by the Food and Agriculture Organization (FAO) of the United Nations. The dataset is vital for understanding global food security, economic trends in agriculture, and land use patterns.

---

## 3. Research Findings

### Where can this data be obtained?
The data is available through several official channels:
*   **Bulk Download Portal:** `https://www.fao.org/faostat/en/#data/bulk`
*   **Direct URL Pattern:** `https://fenixservices.fao.org/faostat/static/bulkdownloads/[DatasetCode]_E_All_Data.zip`
*   **Beta API (SDMX):** `https://nsi-release-ro-statsuite.fao.org/rest/data/` (Supports XML and JSON).
*   **R/Python Packages:** Libraries like `FAOSTAT` (R) or `pandas` (for direct CSV ingestion) can be used to programmatically fetch data.

### What is the format of the data?
*   **Primary Distribution:** Structured **CSV** files.
*   **Container:** Files are provided as **.zip** archives.
*   **Data Models:** 
    *   **Normalized (Long):** Preferred for database ingestion (Area, Item, Element, Year, Value, Unit).
    *   **Wide:** Year-by-year columns.
*   **Metadata:** Included in the zip files as supplementary CSVs (Flags, Units, Definitions).

### Licensing, Rate Limits, and Costs
*   **Licensing:** **Creative Commons Attribution 4.0 International (CC BY 4.0)**. The data is free for commercial and non-commercial use, provided attribution is given to FAOSTAT.
*   **Rate Limits:** There are no strict rate limits for bulk downloads, though API users should practice reasonable request spacing.
*   **Costs:** **Free**. There is no cost to access or download the data.

### Approximate Dataset Size
*   **Per Domain:** Compressed files range from **5 MB** (e.g., Land Cover) to **500+ MB** (e.g., Detailed Trade Matrix).
*   **Uncompressed:** Major domains can exceed **2 GB to 5 GB** in CSV format.
*   **Total Core Database:** The entire core repository is estimated at **10-20 GB compressed**, expanding to significantly more when indexed in a graph database.

### Estimated Scraping/Download Effort
*   **Effort Level:** **Low to Medium**.
*   **Process:** 
    1.  Fetch the list of all dataset codes (available via an API call or HTML parsing of the bulk page).
    2.  Iterate through codes to download ZIP files via the static URL pattern.
    3.  Extract CSVs and map `AreaCode`, `ItemCode`, and `ElementCode` to a standard ontology.
*   **Complexity:** The primary challenge is mapping the high-dimensional data (millions of time-series records) into a performant knowledge graph structure.

---

## 4. Conclusion
FAOSTAT is a "Gold Mine" for a knowledge graph. It provides deep, factual, and time-series data on everything from the number of chickens in Thailand to the amount of coffee exported by Brazil in 1975. Its open licensing and structured CSV format make it highly suitable for automated ingestion.
