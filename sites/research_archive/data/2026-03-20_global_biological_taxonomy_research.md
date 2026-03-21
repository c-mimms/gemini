# Research Report: Global Biological Taxonomy (NCBI & Catalogue of Life)

**Date**: 2026-03-20
**Topic**: Global Biological Taxonomy
**Selected Idea**: Researching the primary global registries for biological classification to build a foundational "Tree of Life" for a local knowledge graph.

---

## 1. Brainstorming: Novel Dataset Ideas

The following dataset types were brainstormed as high-value, factual, and locally storable data for a knowledge graph:

1.  **Global Biological Taxonomy (NCBI Taxonomy & Catalogue of Life)**: (Selected) A deep hierarchical registry of all living organisms, providing a "Source of Truth" for biological names and relationships.
2.  **World Register of Marine Protected Areas (MPAtlas)**: Detailed data on marine conservation zones, including legal status, boundaries, and protection levels.
3.  **Global Radio & Television Station Metadata (FCC/ITU)**: Comprehensive data on transmitters, frequencies, call signs, and coverage areas for broadcasting.
4.  **International Postal Code & Administrative Boundary Mappings**: High-resolution mapping of postal systems to geographic and administrative boundaries (e.g., Geonames, UPU).
5.  **Global Historical Newspaper Metadata (Chronicling America/Library of Congress)**: Metadata for millions of newspaper issues, including titles, dates, locations, and archive locations.

---

## 2. Research Findings: Global Biological Taxonomy

Biological taxonomy is the science of naming, defining, and classifying groups of biological organisms. For a knowledge graph, two primary datasets serve as the "backbone":

### A. NCBI Taxonomy
The NCBI Taxonomy database is a curated classification and nomenclature for all of the organisms in the public sequence databases (GenBank).

*   **Where to obtain**: 
    *   **Bulk Download**: `ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/`
    *   **Key Files**: `taxdump.tar.gz` (standard) or `new_taxdump.tar.gz` (enhanced format).
*   **Data Format**: Custom tab-delimited text files (using `|` as a separator).
*   **Licensing**: **Public Domain** (US Government Work). No restrictions on use, though citation is requested.
*   **Size**: 
    *   Compressed: ~50–60 MB.
    *   Uncompressed: ~350–400 MB (core hierarchy).
    *   Mapping files (e.g., GI to TaxID) can reach several GBs.
*   **Estimated Effort**: **Low**. The formats are stable and easily parsed with simple scripts.

### B. Catalogue of Life (COL)
The Catalogue of Life is the most comprehensive and authoritative index of known species of animals, plants, fungi, and micro-organisms.

*   **Where to obtain**: 
    *   **Download Page**: [catalogueoflife.org/data/download](https://www.catalogueoflife.org/data/download)
    *   **Infrastructure**: [ChecklistBank](https://www.checklistbank.org/) (managed by GBIF and COL).
*   **Data Format**: 
    *   **Darwin Core Archive (DwC-A)**: Industry standard for biodiversity.
    *   **ColDP (COL Data Package)**: Richer tabular format.
*   **Licensing**: **CC BY 4.0** (Creative Commons Attribution 4.0 International).
*   **Size**: 
    *   The eXtended Release (COL XR) contains ~7.9 million names and ~2.5 million species.
    *   Compressed archives are typically several hundred MBs to low GBs.
*   **Estimated Effort**: **Medium**. While DwC-A is a standard, it requires more sophisticated parsing than simple text dumps (handling relational files within the archive).

---

## 3. Evaluation for Knowledge Graph

| Criteria | NCBI Taxonomy | Catalogue of Life |
| :--- | :--- | :--- |
| **Completeness** | High (focused on sequenced life) | Very High (global expert-curated checklist) |
| **Hierarchical Depth** | Deep | Deep |
| **Identifiers** | TaxIDs (industry standard for genomics) | COL IDs / Usage IDs |
| **Ease of Local Storage** | Excellent | Excellent |
| **Cross-referencing** | Links to NCBI sequences, PubMed, UniProt | Links to GBIF, IUCN Red List, and 230+ sources |

---

## 4. Scraper/Integration Strategy

1.  **Scraper Effort**: Writing a downloader for NCBI is trivial (FTP). For COL, using the ChecklistBank API to fetch the latest DwC-A is straightforward.
2.  **Storage**: A relational database (PostgreSQL) or a graph database (Neo4j) is ideal for storing the parent-child relationships (nodes and names).
3.  **Cross-linking**: The real value comes from mapping NCBI TaxIDs to COL IDs to bridge genomic data with general biological observations.

---

## 5. Conclusion
This dataset is **highly recommended** for the local knowledge graph. It provides the essential structure for any query involving life sciences, biodiversity, or medicine. NCBI's public domain status makes it particularly attractive for unrestricted local use.
