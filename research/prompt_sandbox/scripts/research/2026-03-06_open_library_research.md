# Research Report: Open Library Data Dumps

**Date:** 2026-03-06  
**Topic:** Open Library Data Dumps (Books, Authors, and Works)  
**Status:** Completed

---

## 1. Brainstorming: Novel Dataset Ideas

The following dataset types were brainstormed as potential high-value sources for a local knowledge graph:

1.  **Open Library Data Dumps (Books, Authors, Works)**: [SELECTED] A massive, public-domain record of almost every book ever published, including bibliographic metadata, author biographies, and work-edition relationships.
2.  **Global Power Plant Database (Energy Infrastructure)**: GIS-enabled dataset of ~30,000 power plants worldwide, including capacity, fuel type, and ownership. (Source: World Resources Institute).
3.  **World Flora Online (Taxonomic Plant Data)**: The definitive global taxonomic resource for all known plant species, providing hierarchy, synonyms, and geographic distribution.
4.  **Marine Regions (Maritime Boundaries & GIS)**: Standardized GIS data for oceans, seas, and maritime boundaries (EEZ), essential for mapping historical maritime events.
5.  **Global Historical Shipwrecks (AWOIS/WRECKS)**: GIS datasets of shipwrecks, including names, dates, coordinates, and cargos, providing a unique "underwater" historical record.

---

## 2. Selected Idea Research: Open Library Data Dumps

### 2.1 Overview
The Open Library (an Internet Archive project) provides comprehensive datasets of its entire catalog. This is a foundational "knowledge of all books" source, offering structured data on authors, works, and specific editions. It is an ideal backbone for a literary or historical knowledge graph.

### 2.2 Data Sources & URLs
*   **Primary Developers Page:** [openlibrary.org/developers/dumps](https://openlibrary.org/developers/dumps)
*   **Bulk Download Repository (Archive.org):** [archive.org/details/ol_exports](https://archive.org/details/ol_exports) (Provides Torrent and HTTPS links for monthly snapshots).

### 2.3 Data Formats
*   **Format:** Compressed Tab-Separated Values (`.txt.gz`).
*   **Structure:** Each file (Authors, Works, Editions) contains 5 columns: `Type`, `Key`, `Revision`, `Last Modified`, and `JSON`. The `JSON` column contains the full structured record.

### 2.4 Licensing, Costs, and Restrictions
*   **License:** **CC0 (Public Domain Dedication)**. All data contributions are in the public domain.
*   **Cost:** Free.
*   **Restrictions:** No formal restrictions on data dumps. (Live API usage requests a `User-Agent` and a limit of ~1 request per second, but dumps are the preferred method for bulk access).

### 2.5 Dataset Size & Rate Limits
*   **Approximate Compressed Size (Monthly Snapshot):**
    *   **Editions:** ~9.2 GB
    *   **Works:** ~2.9 GB
    *   **Authors:** ~0.5 GB
    *   **Complete History:** ~30 GB (includes all revisions).
*   **Estimated Uncompressed Size:** ~250 GB+ for a full import.
*   **Rate Limits:** Not applicable to data dumps.

### 2.6 Estimated Effort for Scraping/Downloading
*   **Downloading:** **Low.** Direct torrent links make downloading efficient.
*   **Processing:** **Moderate.** Due to the size (45GB+ uncompressed for editions), processing requires efficient streaming JSON parsers or tools like **DuckDB** or **PostgreSQL** (with `jsonb`).
*   **Scripting:** Existing Python tools (e.g., `LibrariesHacked/openlibrary-search`) can be adapted to parse the TSV-JSON format.

---

## 3. Conclusion & Next Steps
The Open Library dataset is a "Tier 1" source for a local knowledge graph. Its CC0 license and structured format make it extremely valuable for long-term local storage.

**Next Action:** Develop a pipeline to download the "Authors" and "Works" files (the smallest and most central files) and import them into a local graph or relational database to test query performance.
