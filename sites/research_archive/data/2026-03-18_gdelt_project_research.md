# Research Report: GDELT Project (Global Database of Events, Language, and Tone)
**Date:** 2026-03-18
**Topic:** GDELT Project

## 1. Brainstormed Ideas
Below are the 3-5 novel dataset types brainstormed for this research task:
1.  **GDELT Project (Global Database of Events, Language, and Tone)**: A real-time monitor of global human society, covering news, events, and sentiment in over 100 languages.
2.  **Global Historical Fortifications & Military Architecture**: A structured dataset of forts, castles, and defensive structures with spatial and historical context.
3.  **Biodiversity Heritage Library (BHL)**: A massive repository of digitized taxonomic literature and biological knowledge.
4.  **Global Power Grid Infrastructure**: Spatial data on transmission lines and substations, complementing existing power plant databases.
5.  **Open Reaction Database (ORD)**: Structured data on chemical reactions and syntheses, essential for scientific knowledge graphs.

## 2. Selected Idea
The selected idea for this research run is the **GDELT Project**. It is one of the most comprehensive and dynamic open datasets available for building a global knowledge graph, as it connects people, locations, and events in near real-time across the entire planet.

## 3. Research Findings

### Where can this data be obtained?
The GDELT Project provides multiple avenues for data acquisition:
*   **Direct HTTP Downloads:** A master file list of all GDELT 2.0 files is maintained at `http://data.gdeltproject.org/gdeltv2/masterfilelist.txt`. Individual zip files can be downloaded directly from the `data.gdeltproject.org` domain.
*   **Amazon S3:** The data is part of the AWS Open Data program, accessible at `s3://gdelt-open-data`.
*   **Google BigQuery:** The entire dataset is hosted on BigQuery (`gdelt-bq:gdeltv2`), allowing for massive-scale SQL queries without needing to download raw files.
*   **APIs:** GDELT DOC 2.0 and GEO 2.0 APIs are available for targeted searches and geographic visualizations.

### What is the format of the data?
*   **Raw Files:** Zipped **CSV** (specifically Tab-Separated Values). The data is split into three main streams:
    *   **Events:** Physical actions (e.g., protests, diplomatic meetings) coded using the CAMEO system.
    *   **Mentions:** Every mention of an event in the news.
    *   **Global Knowledge Graph (GKG):** Connects people, organizations, locations, and themes/emotions found in each article.
*   **Query Results:** BigQuery returns standard SQL results which can be exported as CSV, JSON, or Avro.

### Are there any rate limits, licensing restrictions, or costs?
*   **Licensing:** GDELT is an open platform. All data is available for **unlimited and unrestricted use**, including commercial, academic, and governmental applications, **without any fees**.
*   **Rate Limits:** There are no formal rate limits for the direct file downloads, though standard courtesy in scraping is encouraged. BigQuery access follows Google Cloud's standard pricing (though GDELT provides some free tier access).
*   **Costs:** Data downloads are free. Storage and processing for a local knowledge graph would be the primary costs.

### How large is the dataset approximately?
*   **Historical Archive (1979–Present):** Multi-petabyte scale when uncompressed.
*   **Daily Growth:** GDELT 2.0 updates every 15 minutes. A single year of the Global Knowledge Graph (GKG) can exceed **2.5 TB** (zipped).
*   **Granularity:** Event files are relatively small (MBs), but the GKG and Mentions files are significantly larger.

### Estimated effort to write a scraper or download script?
*   **Low Effort (Targeted Download):** Writing a Python script to parse `masterfilelist.txt` and download files for specific dates or event types is straightforward (1-2 days).
*   **Medium Effort (Real-time Sync):** Building a robust pipeline that monitors the 15-minute updates and ingests them into a database requires a more sophisticated orchestration (e.g., using Airflow or a persistent worker).
*   **High Effort (Local Indexing):** Processing the full petabyte-scale GKG into a graph database (like Neo4j or a custom RDF store) would be a major engineering undertaking due to the sheer volume and complexity of the relationships.

## 4. Conclusion
GDELT is a "gold mine" for a local knowledge graph. For a local setup, the most effective strategy would be to ingest the "Events" stream and a filtered subset of the "GKG" (focusing on specific themes or regions) to keep the storage requirements manageable while still capturing the core "who, what, when, where" of global events.
