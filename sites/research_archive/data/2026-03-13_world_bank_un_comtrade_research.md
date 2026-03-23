---
title: "World Bank & UN Comtrade Trade Data"
date: 2026-03-13
category: "Law & Governance"
tags: ["trade", "economics", "world-bank", "comtrade", "international"]
---

# Research Report: Global Economic Indicators and Trade Flows (World Bank & UN Comtrade)

**Date**: 2026-03-13  
**Topic**: World Bank Open Data & UN Comtrade  
**Researcher**: Gemini CLI  

---

## 1. Brainstorming: Novel Dataset Types
The following dataset types were brainstormed as potential additions to the local knowledge graph:

1.  **World Bank Open Data & UN Comtrade (Selected)**: Comprehensive global economic development indicators (GDP, population, health) and detailed international trade statistics.
2.  **Global Folklore and Mythology (ATU Index)**: A highly structured classification system (Aarne-Thompson-Uther) for international folk tales and mythological motifs.
3.  **NASA GeneLab / NCBI SRA Metadata**: Metadata for biological and genomic experiments, specifically focusing on space-related research and large-scale terrestrial sequencing.
4.  **Global Internet Infrastructure (BGP/ASN)**: Data regarding the physical and logical structure of the internet, including Border Gateway Protocol (BGP) routing and Autonomous System Number (ASN) allocations.
5.  **International Energy Agency (IEA) Energy Statistics**: Detailed global data on energy production, consumption, and carbon emissions.

---

## 2. Research Findings: World Bank Open Data & UN Comtrade

### Overview
This dataset combines the World Bank's development indicators with the United Nations' international trade statistics. It is foundational for any knowledge graph aiming to understand global economic trends, country-level development, and the movement of goods between nations.

### Where can this data be obtained?
- **World Bank Indicators**: [World Bank Data Catalog](https://datacatalog.worldbank.org/) or via the [Indicators API (v2)](https://datahelpdesk.worldbank.org/knowledgebase/articles/889387-api-documentation).
- **UN Comtrade**: [UN Comtrade Database](https://comtrade.un.org/data/) or the [World Integrated Trade Solution (WITS)](https://wits.worldbank.org/).
- **Bulk Downloads**: The World Bank provides ZIP files for entire databases (e.g., World Development Indicators). UN Comtrade requires a "Premium" subscription for true bulk downloads, though "Registered" users can download substantial subsets.

### Data Format
- **API**: JSON, XML, RDF.
- **Bulk**: CSV, XML, Excel (.xls/.xlsx).
- **Specialized**: Official boundaries are available as Shapefiles, GeoJSON, and GeoPackage.

### Rate Limits, Licensing, and Costs
- **World Bank**:
    - **Licensing**: Default is **Creative Commons Attribution 4.0 (CC-BY 4.0)**. Free for commercial and non-commercial use with attribution.
    - **API Limits**: No API key required. Max 32,500 records per request via the `per_page` parameter. Throttling applies for high-volume requests.
- **UN Comtrade**:
    - **Licensing**: Copyrighted by the United Nations. Free access is generally for **internal use only**. Re-dissemination or commercial use requires a specific license.
    - **API Limits (Free/Registered)**: 
        - Guest: 50,000 records per query, 100 requests per hour.
        - Registered: 100,000 records per query, 500 calls per day.
    - **Costs**: Bulk downloads and commercial redistribution licenses require a **Premium Subscription**.

### Dataset Size
- **World Bank Indicators**: Ranges from a few megabytes (specific indicator sets) to **several hundred megabytes** for the full World Development Indicators (WDI) database.
- **UN Comtrade**: Extremely large. A full global dataset for a single year can exceed **450 million records**, resulting in compressed files over **55 GB**.

### Estimated Effort for Scraper/Download Script
- **World Bank (Low Effort)**: Very easy to implement using the bulk ZIP download links or Python libraries like `wbgapi` or `pandas_datareader`.
- **UN Comtrade (Medium Effort)**: Requires managing API pagination and potentially handling large volumes of CSV data. Since free users have record limits per call, a script would need to loop through years and countries systematically while respecting the daily 500-call limit.

---

## 3. Recommendation for Knowledge Graph Integration
The **World Bank World Development Indicators (WDI)** should be the first priority due to its liberal CC-BY 4.0 license and ease of bulk download. **UN Comtrade** data should be added selectively (e.g., top 10 products per country) to keep local storage manageable and remain within the "internal use" terms of the free license.
