# Knowledge Graph Research: Historical Patents Data

## 1. Brainstorming: Novel Dataset Types
The following dataset types were brainstormed as potential high-value sources for a local knowledge graph:

1.  **Historical Patents Data (Selected)**: Full text and metadata of patents from major global offices. Represents the history of human innovation and technological evolution.
2.  **Global Soil Grids**: High-resolution spatial data on soil properties (pH, organic matter, etc.) from ISRIC (World Soil Information). Essential for agricultural and environmental context.
3.  **Publicly Available Legal Cases (Case Law)**: Court opinions and rulings (e.g., Caselaw Access Project, HUDOC for Europe). High-value for legal and social history knowledge.
4.  **Music Metadata (MusicBrainz/Discogs)**: Deeply linked data on artists, releases, labels, and creative relationships. Highly structured and ideal for graph nodes.
5.  **Global Dam and Reservoir Database (GRanD)**: Detailed information on large dams, their reservoirs, and hydrological impact globally.

---

## 2. Selected Idea: Historical Patents Data
Historical patent data provides a structured record of technological breakthroughs, inventor networks, and the evolution of specific industries. It includes bibliographic data (titles, inventors, dates), classifications (IPC/CPC), and full-text descriptions/claims.

### Research Findings

#### **Where can this data be obtained?**
*   **USPTO (United States Patent and Trademark Office):**
    *   **Open Data Portal (ODP):** [data.uspto.gov](https://data.uspto.gov/) - Gateway for all bulk datasets and APIs.
    *   **PatentsView:** [patentsview.org](https://patentsview.org/download) - Provides pre-processed, relational tables (CSV) which are easier to ingest into a graph.
    *   **Bulk Data Storage System (BDSS):** Raw XML files for patent grants and applications.
*   **EPO (European Patent Office):**
    *   **Bulk Data Download Service (BDDS):** [EPO BDDS](https://www.epo.org/en/searching-for-patents/data/bulk-data-sets) - As of January 2025, many key datasets (EBD, Full-Text, DOCDB, INPADOC) are now **free**.
*   **WIPO (World Intellectual Property Organization):**
    *   **PATENTSCOPE:** Provides PCT (Patent Cooperation Treaty) data. Bulk access is typically paid (subscription), but smaller sets (up to 10k records) can be exported for free.

#### **What is the format of the data?**
*   **XML:** The industry standard for full-text data and bibliographic metadata (following WIPO ST.36 or ST.96 standards).
*   **JSON:** Used for specific APIs like the USPTO Patent Examination Data System (PEDS).
*   **CSV/TSV:** Available through research-oriented platforms like PatentsView (USPTO data) or EPO PATSTAT (which is a paid statistical database).

#### **Licensing, Rate Limits, and Costs**
*   **USPTO:** Public domain. No licensing fees or restrictions. Rate limits apply to the Bulk Data API (e.g., 20 downloads of the same file per year per key).
*   **EPO:** Most bulk data is now free (as of 2025). Some advanced statistical products like PATSTAT still carry a fee (approx. €1,250/year).
*   **WIPO:** Bulk data via SFTP is relatively expensive (e.g., 3,900 CHF/year for full-text). Manual exports from the web interface are free but limited.

#### **Approximate Size**
*   **Metadata Only:** Tens of gigabytes (GB).
*   **Full Text (Metadata + Descriptions + Claims):** 500 GB to 1 TB+ (compressed) for the historical backfile.
*   **Weekly Updates:** ~100MB to 200MB for patent grants; ~10GB for applications (including images).

#### **Estimated Effort to Scrape/Download**
*   **Effort: Medium to High.**
    *   **Low Effort (Metadata):** Downloading and parsing CSV files from PatentsView.
    *   **High Effort (Full Context):** Writing a robust parser for the complex WIPO-standard XML files to extract descriptions and claims for thousands of weekly files. Ingesting TB-scale data will require efficient indexing (e.g., Elasticsearch or a specialized graph database).

---

## 3. Implementation Strategy for Knowledge Graph
1.  **Phase 1 (Metadata):** Start with PatentsView CSV files to create nodes for `Inventors`, `Companies` (Assignees), and `Patents` with their basic relationships (dates, classifications).
2.  **Phase 2 (Linking):** Use the IPC/CPC classification codes to link patents to specific technological fields already in the knowledge graph.
3.  **Phase 3 (Full Text):** Progressively ingest full-text descriptions to perform entity extraction (e.g., identifying specific chemicals or components mentioned in a patent) to deepen the graph's knowledge of *how* things are built.
