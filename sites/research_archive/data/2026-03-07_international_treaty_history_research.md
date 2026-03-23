---
title: "International Treaty History"
date: 2026-03-07
category: "Law & Governance"
tags: ["treaties", "international-law", "diplomacy", "history", "governance"]
---

# Research Report: International Treaty & Diplomatic History

**Date**: 2026-03-07
**Topic**: International Treaty & Diplomatic History (1648–Present)
**Researcher**: Gemini CLI

---

## 1. Brainstormed Ideas
Before selecting the primary focus, the following novel dataset types were brainstormed:
1.  **Archaeological Sites & Excavations (Global/Regional)**: Structured data on ancient ruins, excavation reports, and artifacts. High value for historical modeling.
2.  **Global Soil & Subsurface Composition**: GIS data for soil types, acidity, and moisture—critical for agriculture and geological modeling.
3.  **International Treaty & Diplomatic History**: Full text and metadata of treaties signed between nations over centuries. (Selected)
4.  **Global Linguistic Dialects & Recordings**: Granular regional variations and audio/text mappings.
5.  **Historical Currency & Exchange Rates (Pre-1900)**: Data on exchange rates, bullion content of coins, and price indices across different eras.

---

## 2. Selected Idea: International Treaty & Diplomatic History
This topic was selected due to its high factual density, structured nature (metadata), and foundational importance for a knowledge graph covering international relations, law, and history.

### Research Findings

#### A. Where can this data be obtained?
1.  **World Treaty Index (WTI)**:
    - **URL**: [worldtreatyindex.com](http://worldtreatyindex.com/)
    - **Description**: Metadata for over 75,000 treaties signed between 1900 and the present.
2.  **United Nations Treaty Collection (UNTC)**:
    - **URL**: [treaties.un.org](https://treaties.un.org/)
    - **Description**: The official repository for all treaties registered with the UN (UNTS) and the League of Nations (LoNTS).
3.  **Consolidated Treaty Series (Clive Parry)**:
    - **URL**: [Internet Archive (Search)](https://archive.org/search.php?query=title%3A%28Consolidated+Treaty+Series%29+AND+creator%3A%28Clive+Parry%29)
    - **Description**: 231 volumes covering treaties from 1648 (Peace of Westphalia) to 1919.

#### B. What is the format of the data?
- **Metadata**: Available in **CSV** (via WTI bulk download) and **HTML** (via UNTC search).
- **Full Text**: 
    - **PDF**: Most official records (UNTS, LoNTS, Parry Series).
    - **HTML**: Modern UN treaties often have HTML versions.
    - **OCR Text**: Available for many volumes on Internet Archive.

#### C. Rate limits, licensing, and costs?
- **WTI**: Research-oriented. Bulk CSV download is freely available for academic/non-commercial use.
- **UNTC**: Publicly accessible. No official bulk API; scraping is allowed but should be done responsibly (respecting robots.txt).
- **Parry Series**: The underlying treaty texts (pre-1919) are in the **Public Domain**. The digital scans on Internet Archive are free to download.

#### D. Approximate Dataset Size
- **Metadata**: ~50–100 MB (tens of thousands of rows).
- **Full Text (PDFs)**: 
    - UNTS: ~3,000 volumes.
    - LoNTS: ~205 volumes.
    - Parry Series: ~231 volumes.
    - **Total Estimated Size**: 100 GB – 500 GB depending on scan resolution and inclusion of all volumes.

#### E. Estimated Effort to Scrape/Download
- **Metadata (WTI)**: **Low**. Can be downloaded as a single or filtered CSV.
- **Full Text (UNTC)**: **Medium**. Requires a crawler to navigate search results and download linked PDFs.
- **Full Text (Archive.org)**: **Medium**. Can use the `internetarchive` Python CLI to bulk download the "Consolidated Treaty Series" collection.
- **Data Structuring**: **High**. Extracting structured clauses from historical PDFs requires advanced OCR and NLP/LLM-based parsing.

---

## 3. Implementation Plan
1.  **Phase 1: Metadata Acquisition**: Download the World Treaty Index CSV to establish the base knowledge graph (Parties, Dates, Subjects).
2.  **Phase 2: Historical Archive (Pre-1920)**: Use the Archive.org API to download the Clive Parry volumes.
3.  **Phase 3: Modern Archive (Post-1920)**: Develop a Scrapy/Playwright script to crawl the UNTC for League of Nations and UN Treaty Series PDFs.
4.  **Phase 4: Extraction**: Run an OCR pipeline (e.g., Tesseract or Cloud Vision) followed by an LLM-based parser to extract specific treaty articles into JSON-LD.

---
