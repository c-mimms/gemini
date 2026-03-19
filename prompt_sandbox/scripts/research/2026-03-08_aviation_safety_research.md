# Research Report: Aviation Safety & Accident Data (NTSB)

## Date: 2026-03-08
## Topic: Aviation Safety & Accident Data (NTSB)

---

## 1. Brainstormed Ideas
Below are 3-5 novel dataset types researched or considered for this task:

1.  **Aviation Safety & Accident Reports (SELECTED)**: Deeply structured data from the NTSB (National Transportation Safety Board) regarding civil aviation accidents. High factual value for linking aircraft, airlines, locations, and technical failures.
2.  **Global Historical Conflict Data (ACLED/UCDP)**: Time-series data on political violence and protest events around the world. Useful for geopolitical analysis and historical mapping.
3.  **Global Satellite Launch & Space Object Catalog (UCS/JSR)**: Comprehensive list of all objects launched into space, their orbits, purposes, and owners. Excellent for a knowledge graph of space exploration.
4.  **Pharmaceutical Clinical Trials (ClinicalTrials.gov)**: Massive database of clinical studies conducted around the world. High complexity and value for medical/scientific knowledge.
5.  **National Heritage & Archaeological Sites**: Datasets of protected cultural sites and archaeological findings (e.g., UNESCO, national registries).

---

## 2. Selected Idea Research: Aviation Safety & Accident Data (NTSB)

### Overview
The National Transportation Safety Board (NTSB) is an independent U.S. government investigative agency responsible for civil transportation accident investigation. Their aviation database contains information about every civil aviation accident in the United States and its territories since 1962.

### Where can this data be obtained?
-   **NTSB API Developer Portal**: [data.ntsb.gov/api/developer/index.html](https://data.ntsb.gov/api/developer/index.html). Provides programmatic access to Aviation, Safety Recommendations, and Data Dictionary APIs.
-   **CAROL Query Tool**: [data.ntsb.gov/carol-main-public/query-builder](https://data.ntsb.gov/carol-main-public/query-builder). Allows for custom searches and bulk exports of results.
-   **Monthly/Weekly Bulk Downloads**: [NTSB Aviation Query Page](https://www.ntsb.gov/Pages/AviationQuery.aspx). Offers full relational databases in Microsoft Access (MDB) format (e.g., `avall.zip`, `updaymonth.zip`).

### Format of the Data
-   **JSON**: Available via the API and CAROL export.
-   **CSV**: Available via CAROL export (flattened summary).
-   **MDB (Microsoft Access)**: Used for the full relational database downloads.
-   **Text (Pipe-delimited)**: Historically used in older archives.

### Rate Limits, Licensing, and Costs
-   **Licensing**: Data produced by the NTSB is a work of the U.S. Government and is in the **Public Domain**.
-   **Costs**: Free to access and download.
-   **Rate Limits**: The API likely has rate limits (requires account signup for keys), but the bulk MDB downloads and CAROL exports have no strict programmatic limits other than server capacity.

### Dataset Size
-   The full dataset spanning from 1962 to the present is approximately **500 MB to 2 GB** depending on the format (compressed MDBs are smaller).
-   Individual monthly update files are typically a few dozen megabytes.

### Estimated Effort to Scrape/Download
-   **Low to Moderate**: 
    -   Downloading the MDB files and converting them to a more modern format (like SQLite or Parquet) is the most efficient way to get the full history. 
    -   Using the API for incremental updates would require a small Python script using `requests` and an API key.
    -   The schema is complex (relational), so mapping it into a knowledge graph would require significant data modeling effort (linking events, aircraft, engines, and findings).

---

## 3. Conclusion
The NTSB Aviation Accident database is a premier source of structured technical and safety data. Its public domain status and availability in both API and bulk formats make it an ideal candidate for ingestion into a local knowledge graph.
