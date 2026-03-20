# Research Report: Global Scientific Research Metadata (OpenAlex)

**Date**: 2026-03-17
**Topic**: Global Scientific Research Metadata (OpenAlex)
**Researcher**: Gemini CLI

---

## 1. Brainstorming: Novel Dataset Types
The following dataset types were brainstormed as potential additions to the local knowledge graph:

1.  **Global Scientific Research Metadata (OpenAlex) (Selected)**: A complete, open-access replacement for Microsoft Academic Graph (MAG), mapping millions of scholarly works, authors, institutions, and citations.
2.  **Global Renewable Energy Potential (Global Solar/Wind Atlas)**: High-resolution spatial data providing theoretical and technical energy potential for solar and wind power globally.
3.  **Global Historical Climate and Weather Events (EM-DAT)**: A comprehensive database of natural disasters (floods, droughts, earthquakes) and their socio-economic impacts since 1900.
4.  **Global Linguistic Typology (WALS/PHOIBLE)**: Structural, grammatical, and phonological features of thousands of world languages, enabling cross-linguistic analysis.
5.  **Global Pipeline and Power Grid Infrastructure (Open Infrastructure Map)**: Detailed spatial data on the physical layout of global energy transmission networks, substations, and major pipelines.

---

## 2. Selected Idea: Global Scientific Research Metadata (OpenAlex)

### Overview
OpenAlex is a fully open index of the world's scholarly research system. It is the spiritual successor to Microsoft Academic Graph (MAG) and provides the "knowledge of knowledge"—a massive graph connecting every academic paper to its authors, their institutions, and the papers they cite. For a local knowledge graph, this dataset is foundational for understanding the history and progression of human scientific discovery.

### Research Findings

#### A. Where can this data be obtained?
*   **Official Website**: [OpenAlex.org](https://openalex.org/)
*   **REST API**: [https://api.openalex.org](https://docs.openalex.org/api) (Includes a "Polite Pool" for users who identify themselves).
*   **Bulk Download (S3 Snapshot)**: The entire dataset is hosted on Amazon S3 and can be mirrored using the AWS CLI:
    ```bash
    aws s3 sync "s3://openalex" "local-openalex-path" --no-sign-request
    ```
*   **Snapshot Browser**: [openalex.s3.amazonaws.com/browse.html](https://openalex.s3.amazonaws.com/browse.html)

#### B. What is the format of the data?
*   **Snapshot Format**: **JSON Lines (.jsonl.gz)**. The data is partitioned into entities (Works, Authors, Sources, Institutions, Concepts, Publishers) and then further by update date.
*   **API Format**: Standard **JSON** (with JSON-LD context).
*   **Legacy Format**: They also provide a version formatted to match the old MAG schema (TAB-separated columnar files) for compatibility with existing tools.

#### C. Licensing, Rate Limits, and Costs
*   **Licensing**: The metadata itself is licensed under **CC0 (Creative Commons Public Domain Dedication)**. It is free for any use, commercial or otherwise, without attribution (though attribution is encouraged).
*   **API Limits**: 100,000 requests per day for the free tier; the "Polite Pool" (providing an email) offers faster and more reliable service.
*   **Costs**: Completely free. There are no costs for the API or for downloading the S3 snapshots (AWS egress costs are covered by OpenAlex).

#### D. Approximate Dataset Size
*   **Compressed Snapshot**: ~330 GB (as of March 2026).
*   **Uncompressed Snapshot**: ~1.6 TB.
*   **Content Volume**: Metadata for >250 million works, >250 million authors, >100,000 institutions, and >250,000 sources (journals, etc.).

#### E. Estimated Effort for Scraping/Downloading
*   **Downloading (Low Effort)**: Using `aws s3 sync` is a "one-command" operation to mirror the entire dataset.
*   **Processing (High Effort)**: Due to the 1.6 TB uncompressed size, ingesting this data into a local knowledge graph requires significant computational resources. It requires streaming JSON parsers (like `ijson` or `jq`) and a robust graph database (like Neo4j or a high-performance triple store) to handle the millions of edges.

---

## 3. Conclusion
OpenAlex is perhaps the most significant "open" dataset for a general-purpose knowledge graph. While its size is daunting, the CC0 license and the structured nature of its JSON Lines snapshots make it a high-priority target for a long-term local mirror. Initial integration should focus on specific "Concepts" (e.g., Artificial Intelligence, Physics) or high-impact "Works" to manage local storage constraints.

---
**Status**: Ready for Data Mirroring (S3) or Selective API Ingestion.
