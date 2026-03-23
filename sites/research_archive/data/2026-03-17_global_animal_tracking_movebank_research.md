---
title: "Global Animal Tracking (Movebank)"
date: 2026-03-17
category: "Life Sciences"
tags: ["animal-tracking", "ecology", "movebank", "migration", "wildlife"]
---

# Research Report: Global Animal Tracking and Migration Routes (Movebank)

**Date:** 2026-03-17
**Topic:** Global Animal Tracking and Migration Routes (Movebank)
**Researcher:** Gemini CLI

---

## 1. Brainstormed Ideas
Below are the novel dataset types considered during this research session:

1.  **Global Animal Tracking and Migration Routes (Movebank)**: High-resolution tracking data for thousands of species, offering insights into movement patterns, seasonal migrations, and habitat use.
2.  **Global Disaster Loss and Damage Database (DesInventar)**: Granular historical data on natural and technological disasters, including human and economic impacts at local levels.
3.  **Global Linguistic Diversity and Structural Features (Glottolog/WALS)**: Deep metadata on the world's languages, including genealogy, phonology, and grammatical structures.
4.  **Global Human Migration and Refugee Flows (UNHCR/IOM)**: Factual data on the movement of people across borders due to conflict, climate, or economic factors.
5.  **Global Telecommunications Towers and Mobile Coverage (OpenCellID)**: Open dataset of cell tower locations and signal characteristics, mapping the physical infrastructure of mobile networks.

---

## 2. Selected Idea
**Global Animal Tracking and Migration Routes (Movebank)**

This dataset was selected because it provides a unique "movement" dimension to biological knowledge, complementing existing datasets on species distribution (GBIF) and marine life (WoRMS). It is highly structured, factual, and represents real-world sensor data from thousands of individual animals across the globe.

---

## 3. Research Findings

### **Where can this data be obtained?**
The data is hosted at [Movebank.org](https://www.movebank.org/), a free online platform for animal tracking data managed by the Max Planck Institute of Animal Behavior. 
*   **Web Interface:** Searchable database of thousands of studies.
*   **API:** Movebank provides a "Direct Read" service for automated data retrieval.
    *   **Endpoint:** `https://www.movebank.org/movebank/service/direct-read?`
    *   **Authentication:** Requires a Movebank account (Basic Auth).

### **What is the format of the data?**
*   **CSV (Comma-Separated Values):** The primary and most efficient format for bulk data transfer via the API.
*   **JSON:** Available for smaller metadata or event queries.
*   **Spatial Formats:** KML (Google Earth) and ESRI Shapefiles can be exported via the web interface.
*   **Reference Data:** Metadata about animals (species, sex, age) and tags (sensor type) are provided in separate tables linked by ID.

### **Are there any rate limits, licensing restrictions, or costs?**
*   **Cost:** Free to use.
*   **Licensing:** Data is owned by the original researchers. Each "study" has its own license:
    *   **CC0 / Public Domain:** No restrictions.
    *   **CC BY / Attribution:** Requires citation of the data owner.
    *   **CC BY-NC / Non-Commercial:** Restrictions on commercial use.
    *   **Restricted:** Some studies require explicit permission from the researcher before the API will grant access.
*   **Rate Limits:** 
    *   Strict limit of **one concurrent request per IP address**.
    *   Global limit of 20 concurrent requests across all users.
    *   Large requests should be chunked (e.g., by year or individual ID) to prevent timeouts.

### **How large is the dataset approximately?**
*   The database contains over **3 billion locations** and continues to grow.
*   Total size is in the **terabyte (TB) range** if downloading the entire raw sensor archive (including high-frequency acceleration and GPS data).
*   Subset downloads (e.g., specific species or regions) are typically in the **MB to GB range**.

### **What would be the estimated effort to write a scraper/download script?**
*   **Effort:** Moderate.
*   **Complexity:** The API is well-documented but requires handling:
    1.  Authentication and session management.
    2.  Study discovery (iterating through thousands of study IDs).
    3.  License acknowledgement (accepting terms for each study).
    4.  Retry logic and chunking for large datasets to respect the 1-request-per-IP limit.
*   **Tools:** The `move2` R package or Python `requests` library are standard starting points.

---

## 4. Conclusion
Movebank is an exceptional source of factual, time-series data for a local knowledge graph. It allows for complex queries like "Where do Arctic Terns migrate in December?" or "What is the typical flight altitude of a Wandering Albatross?". Integrating this data would significantly enhance the spatial and temporal reasoning capabilities of the local knowledge graph.
