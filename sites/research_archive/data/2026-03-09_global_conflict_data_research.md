---
title: "Global Conflict Data (ACLED)"
date: 2026-03-09
category: "Law & Governance"
tags: ["conflict", "war", "acled", "geopolitics", "political-violence"]
---

# Research Report: Global Historical Conflict Data (UCDP/PRIO)

## Date: 2026-03-09

## Goal
To evaluate the **Uppsala Conflict Data Program (UCDP) / Peace Research Institute Oslo (PRIO)** datasets as a source for a local knowledge graph. These datasets provide deep factual knowledge on armed conflicts, fatalities, actors, and peace agreements globally.

---

## Brainstormed Ideas
1.  **Global Historical Conflict Data (UCDP/PRIO)** (Selected)
2.  **NASA Global Landslide Catalog**
3.  **World Bank Projects & Operations Database**
4.  **Global Dam Inventory (GRanD)**
5.  **OpenStreetMap (OSM) Global Hospital/Education POI Extracts**

---

## Selected Idea: Global Historical Conflict Data (UCDP/PRIO)

### 1. Where can this data be obtained?
The data is primarily managed by the **Uppsala Conflict Data Program (UCDP)** at Uppsala University, often in collaboration with the **Peace Research Institute Oslo (PRIO)**.
*   **Download Center**: [https://ucdp.uu.se/downloads/](https://ucdp.uu.se/downloads/)
*   **REST API**: `https://ucdpapi.pcr.uu.se/api/`

### 2. What is the format of the data?
*   **Bulk Downloads**: Available in **CSV, Excel, Stata (.dta)**, and **R (.RData)** formats.
*   **API**: Provides data in **JSON** format.

### 3. Rate limits, licensing, and costs?
*   **Licensing**: Most datasets are licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**. It is free to use, share, and adapt, provided appropriate attribution is given.
*   **Cost**: Free of charge.
*   **API Access**: As of February 2026, the REST API requires an **authentication token**. Users must contact the UCDP API maintainer with a project description to obtain a token. 
*   **API Limits**: The API enforces **paging** (typically 1,000 rows per page) for large resources like the Georeferenced Event Dataset (GED).

### 4. Approximate size of the dataset?
*   **Georeferenced Event Dataset (GED)**: The most granular dataset (Global version) is approximately **15-20 MB compressed** (CSV/Stata). When expanded or accessed as JSON via API, it contains hundreds of thousands of events.
*   **Yearly Summary Datasets**: Datasets like the *UCDP/PRIO Armed Conflict Dataset* or *Battle-Related Deaths* are much smaller, typically **500 KB to 2 MB**.
*   **Total Storage**: A full local mirror of all core UCDP datasets would likely require less than **500 MB** of storage in a raw format, though a processed knowledge graph representation may be larger.

### 5. Estimated effort to write a scraper or download script?
*   **Effort: Moderate**
*   **Download Script**: A simple Python script using `requests` or `wget` can easily automate the retrieval of the bulk CSV files from the Download Center.
*   **API Scraper**: Requires more effort due to the token requirement and the need to implement robust paging/iteration logic for the GED.
*   **Data Integration**: The data is highly structured with consistent IDs for actors and conflicts, making it relatively straightforward to map into a graph database (e.g., nodes for `Conflict`, `Actor`, `Event`, and `Country`).

---

## Conclusion
The UCDP/PRIO datasets are exceptional candidates for a local knowledge graph. They provide high-fidelity, georeferenced historical facts that are well-structured and free to use under attribution. The primary hurdle is the API token requirement, but bulk CSV downloads offer a reliable alternative for initial data ingestion.
