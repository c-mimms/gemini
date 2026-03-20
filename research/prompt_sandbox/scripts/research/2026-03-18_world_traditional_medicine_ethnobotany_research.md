# Research Report: World Traditional Medicine & Ethnobotany Knowledge Graph

**Date:** 2026-03-18
**Topic:** World Traditional Medicine & Ethnobotany (Integrated Dataset)

## 1. Brainstormed Ideas
- **Global Amateur Radio Stations and Operators (Ham Radio)**: Licensing and technical station data from FCC (ULS) and QRZ.com, providing a network of locations and emergency communication capabilities.
- **Global Rare Disease Knowledge Base (Orphanet/OMIM)**: Factual data on rare diseases, associated genes, symptoms, and clinical phenotypic descriptions.
- **World Traditional Medicine & Ethnobotany (SELECTED)**: Data on plants used in traditional medicine, their chemical constituents (phytochemistry), and their recorded uses across various cultures (Indigenous, TCM, Ayurveda).
- **Global Architectural Heritage & Monuments (UNESCO/World Monuments Fund)**: Structured data on historical buildings, architectural styles, construction dates, and cultural significance.
- **Global Food Composition and Nutrition (USDA/FAO INFOODS)**: Detailed chemical breakdown of raw ingredients and nutritional composition beyond standard consumer labels.

## 2. Selected Idea: World Traditional Medicine & Ethnobotany
This project aims to build a localized knowledge graph that bridges botany, chemistry, and cultural history. By integrating datasets from diverse traditional medicine systems, we can create a powerful resource for understanding the relationship between plant species, their chemical "signatures," and their traditional therapeutic applications.

## 3. Research Findings

### A. Data Sources & URLs
1.  **Dr. Duke's Phytochemical and Ethnobotanical Databases (USDA):**
    - **Source:** [Ag Data Commons (Figshare)](https://agdatacommons.nal.usda.gov/articles/dataset/Dr_Duke_s_Phytochemical_and_Ethnobotanical_Databases/24966822)
    - **Bulk Link:** [Duke-Source-CSV.zip](https://ndownloader.figshare.com/files/43363335)
2.  **Native American Ethnobotany Database (NAEB):**
    - **Source:** [NAEB Datasette Mirror](https://naeb.datasette.io/)
    - **Bulk Link:** [CSV ZIP](https://naeb.datasette.io/-/copy/naeb.zip) | [SQLite DB](https://naeb.datasette.io/naeb.db)
3.  **Traditional Chinese Medicine (TCM) Databases:**
    - **TCMBank:** [TCMBank.cn](https://TCMBank.cn/) (Comprehensive molecular and clinical data).
    - **SymMap:** [SymMap Download](http://www.symmap.org/download/) (Symptom-Herb-Molecular mapping).
    - **TCMID:** [Zenodo Repo](https://zenodo.org/record/8055567) (Cleaned dataset).
4.  **Ayurvedic Pharmacopoeia (API) and Formulations:**
    - **AyurGenixAI:** [Kaggle Dataset](https://www.kaggle.com/datasets/ayurgenixai/ayurvedic-dataset) (15,000+ records).
    - **Indian-Medicine-Dataset:** [GitHub Repo](https://github.com/junioralive/Indian-Medicine-Dataset) (JSON/CSV formats).

### B. Data Format
- **USDA/NAEB:** CSV and SQLite (Easy to ingest into most graph databases).
- **TCMBank/TCMID:** mol2 (3D structures), TSV, and CSV.
- **Ayurveda:** CSV, JSON, and XLSX.
- **Metadata:** Most sources provide clear headers/schemas linking species names (Latin binomials) to chemicals or uses.

### C. Licensing, Costs, and Rate Limits
- **USDA (Dr. Duke's):** Public Domain (CC0). No cost or limits.
- **NAEB:** Publicly available (Open Data). Request for attribution to Indigenous communities and original researchers.
- **TCM Databases:** TCMBank and SymMap are free for academic use. Some commercial restrictions may apply to certain sub-tables.
- **Ayurveda (Kaggle/GitHub):** CC BY-NC-SA or similar open-source licenses.

### D. Dataset Size
- **Tabular Data (CSV/JSON):** Relatively small. Total for all mentioned sources is likely **< 5 GB uncompressed**.
- **Molecular Data (mol2/3D):** Larger, but still manageable for local storage (**~10-20 GB** if all 3D structures are included).
- **Total Footprint:** Estimated at **15-25 GB** for a comprehensive integrated dataset.

### E. Estimated Effort
- **Scraper/Downloader:** **Low.** Most sources provide direct bulk download links or well-structured mirrors.
- **Ingestion/Parsing:** **Moderate.**
    - Latin binomials (scientific names) must be normalized across datasets (using a tool like the GBIF Backbone Taxonomy or World Flora Online) to ensure "Echinacea purpurea" in one set matches the same in another.
    - Chemical names (SMILES/InChI) should be mapped to PubChem CIDs for consistent entity resolution.
- **Graph Construction:** **Moderate to High.** Linking symptoms/uses from different cultures (e.g., matching a TCM "syndrome" to a Western phenotypic symptom) requires careful ontology mapping.

## 4. Conclusion
The integration of these datasets would create a unique "Ethnobotany Knowledge Graph." This local resource would allow for complex queries like: *"Which plants used in both Ayurveda and Native American medicine for respiratory issues share common chemical compounds?"* The high degree of public domain data (especially from the USDA and NAEB) makes this a highly viable and high-value project for local storage.
