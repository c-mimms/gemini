# Research Report: Global Corporate Ownership (LEI Data)
**Date:** 2026-03-25
**Topic:** Global Corporate Ownership & Entity Relationships

---

## 1. Brainstorming: Novel Dataset Ideas
The following novel dataset types were brainstormed as potential sources for a local knowledge graph:

1.  **Global Corporate Ownership (LEI Data)**: (SELECTED) Data from GLEIF showing corporate hierarchies ("who owns whom") for millions of entities worldwide.
2.  **Endangered Languages & Dialects**: Geographic and linguistic data for at-risk languages, speaker counts, and vitality status.
3.  **Internet Exchange Points (IXPs) & Infrastructure**: Technical specs and locations of the physical hubs of the internet and major data centers.
4.  **Global Postal Code & Administrative Boundaries**: Mapping of postal codes to administrative regions across multiple countries.
5.  **World Heritage & Protected Cultural Sites**: Detailed metadata on UNESCO and national cultural monuments, including historical significance and coordinates.

---

## 2. Selected Idea: Global Corporate Ownership (LEI Data)
The Global Legal Entity Identifier (LEI) system provides a publicly accessible database of corporate entities and their ownership structures, which is essential for mapping global economic relationships.

### Research Findings

#### Where can this data be obtained?
The data is provided by the **Global Legal Entity Identifier Foundation (GLEIF)**.
- **Bulk Downloads (Golden Copy):** [GLEIF Golden Copy Files](https://www.gleif.org/en/lei-data/gleif-golden-copy-files)
- **RESTful API:** `https://api.gleif.org/api/v1/`
- **Documentation:** [GLEIF API Docs](https://api.gleif.org/api/v1/docs)

#### What is the format of the data?
GLEIF provides data in three primary formats:
- **XML:** The native format (LEI-CDF and RR-CDF standards).
- **CSV:** Flattened versions for easier ingestion into spreadsheets or simple databases.
- **JSON:** Available via the API and structured bulk downloads.

#### Rate limits, licensing, and costs
- **Licensing:** Provided under a **Creative Commons (CC0)** "Public Domain Dedication" license. It is Open Data and can be freely used, modified, and redistributed.
- **Costs:** All data access (bulk and API) is **free of charge**.
- **Rate Limits:** The bulk downloads have no strict rate limits beyond standard server capacity. The API is designed for lookups and filtering rather than mass scraping.

#### How large is the dataset approximately?
- **Records:** Over **3.2 million entities** (as of early 2026).
- **Size:** Compressed (ZIP) XML Golden Copy files are approximately **1GB**. Uncompressed, the data likely spans several gigabytes.
- **Frequency:** Golden Copies are published **3 times daily**.

#### Estimated effort to write a scraper or download script
- **Effort Rating: Moderate**
- **Details:** Writing a script to download the daily ZIP files is trivial. Parsing the XML (CDF format) to extract Level 2 relationships ("Who owns whom") requires understanding the GLEIF hierarchy schema, but the data is highly structured and well-documented, making it very suitable for a knowledge graph.

---

## 3. Conclusion
The GLEIF dataset is an exceptionally high-value target for a local knowledge graph. Its CC0 licensing, high structure, and comprehensive coverage of corporate ownership make it a foundational piece for any system aiming to answer questions about global finance and corporate influence.
