# Research Report: Global Historical Census & Population Data

## Date: 2026-03-18
## Topic: Global Historical Census Data (IPUMS & Open Alternatives)

---

## 1. Brainstorming: Novel Dataset Ideas
The following dataset types were brainstormed as potential additions to a local knowledge graph, focusing on high-value, factual, and structured data:

1.  **Global Historical Census Data (IPUMS)**: Massive, integrated demographic microdata from hundreds of countries and centuries, providing individual-level insights into human population shifts.
2.  **Global Port and Maritime Infrastructure (AIS & Port Performance)**: Detailed data on the movement of global trade, port capacity, vessel characteristics, and real-time shipping logistics.
3.  **Global Pesticide and Agricultural Chemical Usage**: Regional data on chemical inputs in farming (USGS, FAO), essential for understanding environmental and health impacts.
4.  **Global Religious and Sacred Sites**: Geolocation and historical data of places of worship, pilgrimage routes, and sacred architecture across all major faiths and cultures.
5.  **Global Biodiversity Genomics Metadata**: Information on sequenced genomes for all known species (e.g., Earth BioGenome Project, NCBI BioProject), mapping the "source code" of life.

**Selected Idea for Research**: **Global Historical Census Data (IPUMS & Open Alternatives)**.

---

## 2. Research Findings: Global Historical Census Data

### A. Primary Source: IPUMS (Integrated Public Use Microdata Series)
IPUMS is the world's largest individual-level population database, harmonizing census data from over 100 countries and spanning centuries.

*   **Website**: [ipums.org](https://www.ipums.org/)
*   **Data Types**:
    *   **IPUMS International**: Harmonized census data from 100+ countries.
    *   **IPUMS USA**: U.S. Census and ACS data from 1790 to present.
    *   **IPUMS NHGIS**: Historical U.S. geographic and aggregate data (GIS files).
*   **Format**: Microdata is provided in fixed-width ASCII (`.dat`) or `.csv`. Metadata is provided in DDI-compliant `.xml`.
*   **API/Scraping**: Provides a formal REST API. Python developers can use the `ipumspy` library to programmatically submit "extract" requests, monitor status, and download files.
*   **Licensing**: Free for research and educational use. **Registration is required**. Redistribution of raw data is generally prohibited; however, local storage for personal/private knowledge graphs is permitted.
*   **Size**: Total database exceeds 25+ GB for common extracts, but "full-count" historical datasets (e.g., every person in the 1880 US Census) can reach several Terabytes.

### B. Secondary Sources: Open-by-Default (No Registration)
For aggregated statistics and spatial data that allow for freer redistribution:

| Source | Type | Format | URL |
| :--- | :--- | :--- | :--- |
| **World Bank Open Data** | Global Development Indicators (1960-Present) | CSV, XML | [data.worldbank.org](https://data.worldbank.org/) |
| **UNdata** | Official Demographic Statistics (Demographic Yearbook) | CSV | [data.un.org](http://data.un.org/) |
| **WorldPop** | High-resolution (100m) Gridded Population Maps | GeoTIFF, CSV | [worldpop.org](https://www.worldpop.org/) |
| **GHSL (Global Human Settlement Layer)** | Built-up area and population grids (1975-2030) | GeoTIFF | [ghsl.jrc.ec.europa.eu](https://ghsl.jrc.ec.europa.eu/) |

---

## 3. Evaluation for Knowledge Graph Integration

### Effort to Write Scraper/Downloader:
*   **IPUMS (Moderate)**: Requires an API key and implementation of a "submit-and-wait" workflow using `ipumspy`. The logic must handle extract definitions (selecting variables and years).
*   **World Bank / UNdata (Low)**: Direct bulk download links are available for most datasets. Python `requests` or `wget` can handle these easily.
*   **WorldPop (Low-Moderate)**: Provides a structured file hierarchy on their FTP/HTTPS servers, easily crawlable for specific country/year combinations.

### Estimated Dataset Size:
*   **Global Aggregates (Country-level)**: < 1 GB.
*   **Gridded Population Data**: 50 - 200 GB (Global, high-res).
*   **Microdata (IPUMS)**: 100 GB - 5 TB depending on the number of samples and variables selected.

### Recommendation:
Start by integrating **World Bank** and **UNdata** for a foundational country-level demographic layer. For deep factual knowledge, use the **IPUMS API** to pull specific historical samples (e.g., "All household heads in 19th-century Europe") to populate the knowledge graph with individual-level relationships and mobility patterns.

---

## 4. Conclusion
Historical census data provides the "who, where, and when" of human history. By combining IPUMS microdata with WorldPop spatial grids, a local knowledge graph can answer complex questions about urbanization, migration, and demographic transitions with extreme precision.
