---
title: "World Register of Marine Species (WoRMS)"
date: 2026-03-09
category: "Life Sciences"
tags: ["marine-biology", "taxonomy", "ocean", "species", "biodiversity"]
---

# Research Report: World Register of Marine Species (WoRMS)

**Date**: 2026-03-09
**Topic**: World Register of Marine Species (WoRMS)
**Researcher**: Gemini CLI

## Brainstormed Ideas
1.  **Global Dam and Reservoir Database (GRanD)**: Comprehensive data on large dams, including location, capacity, and catchment areas.
2.  **Lighthouse and Navigational Aids (ARLHS/OSM)**: A global database of maritime navigational structures.
3.  **Historical Currency Exchange Rates**: Long-term longitudinal data on global currency fluctuations.
4.  **World Register of Marine Species (WoRMS)**: An authoritative taxonomic database of all marine organisms. (**Selected**)
5.  **Global Human Settlement Layer (GHSL)**: Spatial data on the growth of human settlements and population density.

---

## Selected Idea: World Register of Marine Species (WoRMS)

### Overview
The World Register of Marine Species (WoRMS) is an open-access inventory of all marine species, providing a comprehensive and authoritative list of names of marine organisms, including their synonymy. It is managed by an international board of taxonomic experts.

### 1. Where can this data be obtained?
*   **Official Website**: [marinespecies.org](https://www.marinespecies.org)
*   **REST API**: `https://www.marinespecies.org/rest/`
*   **Bulk Download**: Quarterly database dumps are available via a request form on their website.
*   **Web Services**: Supports both REST and SOAP protocols for programmatic access.

### 2. What is the format of the data?
*   **API Results**: Primarily **JSON**.
*   **Bulk Downloads**: Provided in **Darwin Core Archive (DwC-A)** format. This format is a standard for biodiversity data and typically consists of multiple **CSV** files (cores and extensions) bundled with an XML descriptor file (`meta.xml`).

### 3. Licensing, Rate Limits, and Costs
*   **Licensing**: Text content is generally licensed under **Creative Commons Attribution (CC-BY)**. However, redistribution of the entire database requires a formal agreement (Memorandum of Understanding) with the Flanders Marine Institute (VLIZ).
*   **Rate Limits**: The API is free but intended for real-time lookups. For large-scale data harvesting, WoRMS strongly requests the use of their quarterly bulk downloads to avoid overloading the servers.
*   **Update Requirements**: If the full dataset is redistributed, it must be updated at least four times per year.
*   **Costs**: Access is **free of charge**.

### 4. Approximate Dataset Size
*   **Taxon Names**: Over **500,000** names (including synonyms).
*   **Accepted Species**: Approximately **240,000+** valid marine species.
*   **Storage**: While exact MB/GB values vary by version, the CSV-based Darwin Core Archive is estimated to be in the range of **several hundred megabytes to a few gigabytes** when uncompressed, including distribution data and literature references.

### 5. Estimated Effort to Scrape/Download
*   **API Scraper**: **Low**. The REST API is well-documented and easy to interface with using standard libraries (e.g., Python `requests`).
*   **Bulk Integration**: **Medium**. Handling Darwin Core Archives requires parsing the `meta.xml` and relating multiple CSV files (e.g., matching taxa to their distributions or vernacular names).
*   **Request Process**: Requires a one-time effort to fill out the request form and wait for approval for the bulk dump.

### Conclusion
WoRMS is a high-value dataset for a local knowledge graph, offering structured biological and taxonomic data. Integrating it would provide a deep understanding of marine life, complementing other biodiversity datasets like GBIF. The use of DwC-A format makes it highly compatible with existing biodiversity informatics tools.
