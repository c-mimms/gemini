# Research Report: Chemical Property Datasets (PubChem)
**Date:** 2026-03-06
**Topic:** Chemical Property Datasets for Local Knowledge Graph
**Selected Dataset:** PubChem (NIH/NLM)

---

## 1. Brainstormed Ideas
Before selecting PubChem, the following dataset types were considered for their potential value to a local knowledge graph:

1.  **Chemical Property Datasets (PubChem, ChemSpider)**: Detailed factual data on molecular structures, physical properties, safety, and bioactivity. (SELECTED)
2.  **Global Biological Taxonomy (GBIF, Catalogue of Life)**: Hierarchical classification of all known life, including species names, habitats, and occurrences.
3.  **Historical Patent Data (USPTO Bulk Data)**: Full-text records of innovation history, providing deep technical and legal knowledge.
4.  **Public Health & Epidemiology Data (WHO GHO, CDC WONDER)**: Statistics on disease prevalence, mortality, and healthcare infrastructure globally.
5.  **Astronomical Catalogs (Gaia Archive, SIMBAD)**: Positional and physical data for hundreds of millions of celestial objects.

---

## 2. Research Findings: PubChem

### Overview
PubChem is the world's largest collection of freely accessible chemical information, maintained by the National Center for Biotechnology Information (NCBI) at the NIH. It is a fundamental source of "ground truth" for chemistry and pharmacology.

### Data Acquisition
*   **Bulk Download (Preferred for local KG):** Available via FTP at `ftp://ftp.ncbi.nlm.nih.gov/pubchem/`. 
*   **Programmatic Access:** PUG-REST API (`https://pubchem.ncbi.nlm.nih.gov/rest/pug/`) for targeted queries.
*   **Web Interface:** For manual verification and exploratory search.

### Data Format
*   **SDF (Structure-Data File):** The industry standard for chemical structures and associated properties. Usually provided as compressed GZip files (`.sdf.gz`).
*   **RDF (Resource Description Framework):** Best for Knowledge Graph integration. PubChem provides a massive RDF distribution in Turtle (`.ttl.gz`) or XML format.
*   **Other Formats:** CSV, XML, JSON, and ASN.1 are available for specific subsets like BioAssays.

### Licensing & Costs
*   **Licensing:** Most data is in the **Public Domain**. Since it is a US Government resource, there are no licensing fees.
*   **Restrictions:** Some third-party annotations may have specific terms, but the core structural and property data is free.
*   **Costs:** Free to download and use.

### Rate Limits & Storage
*   **API Limits:** 5 requests per second, 400 requests per minute. Not suitable for full database mirroring.
*   **FTP Usage:** No specific rate limits, but users are expected to be "good citizens" by using a single connection and avoiding peak hours.
*   **Size (Estimated):**
    *   **SDF (Full Compound):** ~100 GB+ (Compressed), ~500 GB+ (Uncompressed).
    *   **RDF (Full):** Several Terabytes (TB) when fully expanded.
    *   **BioAssay Data:** ~100 GB+.

### Implementation Effort
*   **Scraper/Downloader:** Low effort. A simple `bash` script using `wget -m` or `lftp` can mirror the FTP directories.
*   **Parsing/Ingestion:** Moderate effort. 
    *   **SDF:** Requires libraries like `RDKit` (Python) or `OpenBabel` to parse molecular structures.
    *   **RDF:** Requires a triple store (e.g., Apache Jena, GraphDB) or a high-performance RDF parser like `oxigraph`.
*   **Knowledge Graph Mapping:** High effort. Mapping PubChem's internal IDs (CIDs, SIDs) to other entities (like Wikipedia/Wikidata or medical databases) requires careful alignment.

---

## 3. Conclusion & Recommendation
PubChem is an ideal candidate for a local knowledge graph due to its structure and public domain status. However, due to its size (TB-scale for RDF), a selective ingestion strategy is recommended—focusing on the top 1 million most common/important compounds first—rather than a full mirror of the entire database.
