# Research Report: Harmonized Tariff Schedule (HTS) and Global Trade Classifications

## Date: 2026-03-20

## Brainstormed Ideas
1.  **Global Postal Code and Administrative Boundary Data**: Mapping of postal codes to coordinates and administrative regions (e.g., GeoNames).
2.  **Harmonized Tariff Schedule (HTS) and Trade Classifications**: A complex, hierarchical system for classifying all traded goods globally (WCO/National Customs).
3.  **Global Wildfire and Thermal Anomalies Data**: Real-time and historical satellite-derived data on fires (NASA FIRMS).
4.  **Global Public Health Indicators**: Comprehensive health metrics and statistics by country/region (WHO GHO).
5.  **Standard Physical Constants and Metrology Data**: Foundational scientific constants and unit definitions (CODATA/NIST).

## Selected Idea: Harmonized Tariff Schedule (HTS) and Trade Classifications
The Harmonized System (HS) is a standardized numerical method of classifying traded products. It is used by customs authorities around the world to identify products when assessing duties and taxes and for gathering statistics.

## Research Findings

### 1. Where can this data be obtained?
- **U.S. International Trade Commission (USITC)**: Provides the official U.S. Harmonized Tariff Schedule (HTS).
    - **REST API**: `https://hts.usitc.gov/reststop`
    - **Bulk Downloads**: [Data.gov](https://catalog.data.gov/dataset/harmonized-tariff-schedule-of-the-united-states-2026) or the [USITC Export Tool](https://hts.usitc.gov/view/export).
- **United Nations Comtrade**: Provides a free, global 6-digit HS nomenclature JSON file.
    - **URL**: `https://comtradeapi.un.org/files/v1/app/reference/HS.json`
- **World Customs Organization (WCO)**: Maintains the global HS nomenclature. While they sell official digital versions for a fee (~€70), the 6-digit international core is widely available for free via UN and national customs agencies.

### 2. What is the format of the data?
- **JSON**: Available via the USITC REST API and UN Comtrade.
- **CSV/Excel**: Available for bulk download from USITC and Data.gov.
- **XML**: Official WCO digital publications are often in XML.

### 3. Rate limits, licensing, and costs
- **USITC API/Bulk**: Public domain (U.S. Government work), no authentication required, no explicit rate limits for reasonable use.
- **UN Comtrade**: Open access for the reference HS nomenclature JSON.
- **WCO Official Files**: Paid (€70 for the digital version), but the information itself is a global standard and can be reconstructed from open national schedules.

### 4. Approximate size of the dataset
- **U.S. HTS (Full Schedule)**: Approximately **100-200 MB** in JSON format.
- **Global 6-digit HS Nomenclature**: Approximately **5-10 MB** in JSON format.
- **Historical Archives**: Decades of historical data are available, totaling several gigabytes if all revisions are collected.

### 5. Estimated effort to write a scraper or download script
- **Low**: For bulk downloads, it is a simple `curl` or `wget` operation. 
- **Moderate**: For the USITC REST API, a simple Python script using `requests` can traverse the chapters (01-99) to build a local database. The API is well-documented and predictable.

## Conclusion
The Harmonized Tariff Schedule is a high-value, deeply structured dataset that is essential for any knowledge graph aiming to understand global commerce, logistics, and product classification. The availability of unauthenticated APIs and bulk downloads from the USITC makes it an ideal candidate for local ingestion.
