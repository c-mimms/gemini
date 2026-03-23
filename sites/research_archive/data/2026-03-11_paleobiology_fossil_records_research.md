---
title: "Paleobiology & Fossil Records Database"
date: 2026-03-11
category: "Life Sciences"
tags: ["paleontology", "fossils", "evolution", "deep-time", "biology"]
---

# Research Report: Paleobiology & Fossil Records (PBDB)

**Date:** 2026-03-11
**Topic:** Paleobiology and Fossil Records
**Researcher:** Gemini CLI

---

## 1. Brainstorming: Novel Dataset Types
The following dataset types were brainstormed as potential candidates for the local knowledge graph:

1.  **Human Anatomy & Medical Knowledge (e.g., UMLS, FMA):** A deep, structured representation of human biology and medical terminology.
2.  **Paleontology & Fossil Records (e.g., Paleobiology Database):** A comprehensive record of life on Earth throughout geological time. (SELECTED)
3.  **Classical Musicology & Scores (e.g., MusicBrainz, IMSLP):** Detailed metadata on composers, works, and musical structures.
4.  **Global Philately & Postal History:** A massive dataset of stamps, postal routes, and historical geopolitical changes.
5.  **Traditional Ethnobotany & Medicinal Plants:** Data on historical and cultural uses of plants for medicine and nutrition.

---

## 2. Selected Idea: Paleontology & Fossil Records
Paleontology offers a unique dimension to a knowledge graph by providing a temporal and evolutionary context to biological entities. The **Paleobiology Database (PBDB)** is the primary resource for this data.

### Research Findings

#### Where can this data be obtained?
The data is primarily managed by the **Paleobiology Database (PBDB)**.
- **Main Website:** [https://paleobiodb.org/](https://paleobiodb.org/)
- **API Documentation:** [https://paleobiodb.org/data1.2/](https://paleobiodb.org/data1.2/)
- **Bulk Download Generator:** [https://paleobiodb.org/cgi-bin/bridge.pl?a=displayDownloadGenerator](https://paleobiodb.org/cgi-bin/bridge.pl?a=displayDownloadGenerator)

#### What is the format of the data?
The PBDB API supports multiple structured formats:
- **JSON:** Ideal for hierarchical data (e.g., taxonomic trees).
- **CSV / TSV:** Best for flat occurrence data and bulk processing.
- **RIS:** Specifically for bibliographic references.

#### Licensing, Rate Limits, and Costs
- **Licensing:** Most data is released under the **Creative Commons Attribution 4.0 International (CC-BY 4.0)** license.
- **Costs:** Access is free for public data.
- **Rate Limits:** No strict rate limits are published, but the API provides a "Download Generator" for very large queries to ensure stability.
- **Attribution:** Use of the data requires citation of the Paleobiology Database.

#### Dataset Size
- **Total Occurrences:** Over **2.1 million** fossil occurrences.
- **Storage Size:** A full compressed download (tar.gz or zip) of all occurrences is approximately **100 MB to 120 MB**. Uncompressed CSV data for the entire database is estimated at **500 MB to 1 GB**, making it highly suitable for local storage.

#### Estimated Scraping/Download Effort
- **Effort Level:** **Very Low**.
- **Implementation:** The API is exceptionally well-structured. A simple Python script using `requests` can fetch the entire occurrences list or taxonomic tree in single calls:
  - `GET https://paleobiodb.org/data1.2/occs/list.csv?all_records&show=coords,loc,paleoloc,time,strat,ident,tax`
  - `GET https://paleobiodb.org/data1.2/taxa/list.json?all_records`

---

## 3. Potential for Knowledge Graph Integration
Integrating PBDB data allows the knowledge graph to:
- Map the historical distribution of species across deep time.
- Connect modern biological taxa to their extinct ancestors.
- Provide geographical context for fossil finds relative to modern borders and geological formations.
- Link fossils to the original scientific literature that described them.
