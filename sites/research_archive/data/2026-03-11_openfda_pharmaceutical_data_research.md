# Research Report: Global Pharmaceutical & Drug Information (OpenFDA)

## Date: 2026-03-11
## Researcher: Gemini CLI

---

## 1. Brainstormed Ideas

As part of this research cycle, the following novel dataset types were identified as high-value candidates for a local knowledge graph:

1.  **Global Pharmaceutical & Drug Information (OpenFDA)**: Comprehensive database of drug properties, adverse event reports, recall enforcement, and NDC directories.
2.  **Global Nuclear Reactor Database (IAEA PRIS)**: Technical specifications, construction history, and operational status of all commercial power reactors worldwide.
3.  **Global Music Metadata (MusicBrainz)**: A massive, structured, open-source database of recordings, artists, albums, and release dates.
4.  **Global Historical Currency Exchange Rates (IMF/World Bank)**: Multi-decade time-series data for global currency values and economic context.
5.  **Global Historical Air Quality (OpenAQ)**: Decades of sensor data for major pollutants (PM2.5, PM10, NO2, SO2, O3) from thousands of global stations.

---

## 2. Selected Idea: Global Pharmaceutical & Drug Information (OpenFDA)

The **OpenFDA** dataset was selected for its high factual density and immediate utility in providing deep medical and chemical knowledge to the local knowledge graph.

### 2.1 Overview
The FDA (U.S. Food and Drug Administration) provides the `openFDA` platform to make its regulatory and public health data accessible. This includes millions of records on drug labeling, adverse reactions reported by patients/physicians, and official recall notices.

### 2.2 Where can this data be obtained?
*   **Direct Bulk Download**: [openFDA Downloads Page](https://open.fda.gov/data/downloads/)
*   **Programmatic Index**: [https://api.fda.gov/download.json](https://api.fda.gov/download.json) (A machine-readable JSON file listing all current bulk download links).
*   **Interactive API**: [https://api.fda.gov/](https://api.fda.gov/) (Useful for testing or specific lookups).

### 2.3 Data Format
*   **Type**: Zipped JSON (`.json.zip`).
*   **Structure**: Highly nested JSON objects that follow the same schema as the REST API results.
*   **Partitioning**: Large datasets (like Adverse Events) are split into hundreds or thousands of numbered parts for easier handling.

### 2.4 Rate Limits, Licensing, and Costs
*   **Licensing**: Most data is in the **Public Domain**. Some specific classification schemas (like USP Drug Classification) may have specific attribution requirements or use-case restrictions, but generally, the data is free for public use.
*   **Costs**: Free.
*   **Limits**: 
    *   **API**: 1,000 requests per day (anonymous) or 240,000 requests per day (with a free API key).
    *   **Bulk Downloads**: No specific limits stated; designed for high-volume retrieval.

### 2.5 Dataset Size
*   **Compressed**: Approximately **23 GB**.
*   **Uncompressed**: Approximately **100 GB**.
*   **Individual Components**:
    *   **Drugs@FDA**: ~8.8 MB compressed (High-level info on approvals).
    *   **Drug Labeling**: ~4 GB compressed (Full text of package inserts).
    *   **Drug Adverse Events**: ~15+ GB compressed (Millions of reports).

### 2.6 Estimated Scraping/Download Effort
*   **Complexity**: **Low to Moderate**.
*   **Method**: 
    1.  Fetch `https://api.fda.gov/download.json`.
    2.  Filter the JSON to find the `drug` category endpoints.
    3.  Iterate through the `export` partitions and download via `curl` or `requests`.
    4.  Extract and parse into a local database (e.g., PostgreSQL or a Graph DB).
*   **Timeline**: A production-ready ingestion script could be written in **1-2 days**.

---

## 3. Conclusion
The OpenFDA dataset is a premier source of structured pharmaceutical knowledge. Its public domain status and availability via a programmatic index make it an ideal candidate for ingestion into a local knowledge graph.
