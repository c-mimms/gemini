---
title: "Global Art Museum Open-Access Collections"
date: 2026-03-10
category: "History & Culture"
tags: ["art", "museums", "open-access", "culture", "cultural-heritage"]
---

# Research Report: Global Art and Museum Open Access Data

**Date**: 2026-03-10
**Topic**: Global Art and Museum Open Access Data (The Met, Smithsonian, Rijksmuseum, etc.)
**Status**: Completed

## 1. Brainstormed Ideas
- **Art and Museum Catalogs (Met, Smithsonian, Rijksmuseum)**: Rich cultural and historical data with structured metadata. (SELECTED)
- **Human Genome and Genetic Variation (NCBI/ClinVar)**: Highly factual biological data on human genetics.
- **MusicBrainz Metadata**: An open music encyclopedia with deep relational data.
- **International Postal Data (UPU)**: Global addressing systems and postal logistics information.
- **World Heritage Sites (UNESCO)**: Geographical and historical data on globally significant sites.

## 2. Selected Idea: Art and Museum Catalogs
This research focuses on harvesting metadata from the world's leading museums that have adopted "Open Access" policies (CC0 licensing). This data provides deep, factual knowledge about human history, geography, materials, cultures, and provenance.

## 3. Research Findings

### A. Data Sources and Access
| Museum | Primary Access Method | Specific URL/API |
| :--- | :--- | :--- |
| **The Metropolitan Museum of Art (The Met)** | GitHub / REST API | [metmuseum/openaccess](https://github.com/metmuseum/openaccess) |
| **Smithsonian Institution** | AWS S3 (Open Data) | `s3://smithsonian-open-access/metadata/edan/` |
| **Rijksmuseum** | Data Portal / API | [data.rijksmuseum.nl](https://data.rijksmuseum.nl) |
| **Cleveland Museum of Art (CMA)** | GitHub / REST API | [ClevelandMuseumArt/openaccess](https://github.com/ClevelandMuseumArt/openaccess) |
| **Art Institute of Chicago (AIC)** | S3 Bulk Download | [artic-api-data.s3.amazonaws.com/artic-api-data.tar.bz2](https://artic-api-data.s3.amazonaws.com/artic-api-data.tar.bz2) |

### B. Data Format
- **The Met**: CSV (bulk) and JSON (API).
- **Smithsonian**: Line-delimited JSON (NDJSON) compressed in `.bz2`.
- **Rijksmuseum**: JSON and XML (OAI-PMH).
- **Cleveland**: JSON and CSV (GitHub).
- **Art Institute of Chicago**: JSON (bulk dump of API responses).

### C. Licensing and Restrictions
- **Licensing**: Most are **CC0 (Creative Commons Zero)**, meaning they are in the public domain and can be used for any purpose without attribution.
- **Rate Limits**: 
    - The Met API has moderate limits (no explicit number, but standard web scraping etiquette applies).
    - Cleveland and Chicago APIs are very open.
    - Bulk downloads (GitHub/S3) have no rate limits once downloaded.
- **Costs**: Free.

### D. Dataset Size
- **Total Combined**: ~12.5 million+ records.
- **Smithsonian**: ~11 million metadata records.
- **The Met**: ~492,000 records.
- **Rijksmuseum**: ~800,000 records.
- **AIC**: ~120,000 records.
- **CMA**: ~61,000 records.

### E. Estimated Effort for Scraper/Ingestion
- **Effort Level**: **Low to Medium**.
- **Implementation**:
    - **Met/Cleveland**: Very easy; download the CSV from GitHub using `git lfs`.
    - **Smithsonian**: Requires `boto3` or `aws-cli` to sync from S3, and a script to iterate through `.bz2` NDJSON files.
    - **AIC**: Download the 2.5GB tarball and parse the JSON files.
    - **Knowledge Graph Ingestion**: High-value entities include `Object`, `Artist`, `Culture`, `Time Period`, `Geography`, and `Material`. These map well to a graph structure (e.g., `Artist` -[CREATED]-> `Object`).

## 4. Conclusion
Art and museum datasets are high-value targets for a local knowledge graph. They provide a massive amount of cross-referenced data connecting history, geography, and art. The Smithsonian dataset alone provides enough scale to test graph performance, while the Met and Cleveland datasets offer extremely clean, well-documented CSVs for quick prototyping.
