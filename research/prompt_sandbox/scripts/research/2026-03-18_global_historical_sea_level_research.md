# Research Report: Global Historical Sea Level and Tide Gauge Data (PSMSL)

**Date:** 2026-03-18
**Topic:** Global Historical Sea Level and Tide Gauge Data (PSMSL)

## 1. Brainstormed Ideas
- **Global Telephony Infrastructure and Numbering Plans (ITU-T)**: Technical standards for phone numbers, mobile network codes (MCC/MNC), and international dialing.
- **World Digital Heritage Sites (3D Scans and Architectural Metadata)**: High-resolution scans and metadata for endangered or significant historical sites worldwide from projects like CyArk.
- **Global Scientific Research Grants and Funding Metadata (NIH/NSF/European Commission)**: A comprehensive record of what research has been funded, by whom, and for what amount (Dimensions/NIH RePORTER).
- **Global Historical Sea Level and Tide Gauge Data (PSMSL)**: Centuries of recorded sea level changes from tide gauges around the world. (SELECTED)
- **Global Historical Census and Demographic Data (IPUMS)**: Granular social and demographic snapshots across centuries from over 100 countries.

## 2. Selected Idea: Global Historical Sea Level and Tide Gauge Data (PSMSL)
The Permanent Service for Mean Sea Level (PSMSL) is the global data bank for long-term sea level information from tide gauges. Established in 1933, it provides a foundational dataset for climate science, geophysics, and coastal engineering. This data is critical for a knowledge graph aimed at answering questions about long-term environmental shifts, historical sea levels, and regional coastal stability.

## 3. Research Findings

### A. Data Sources & URLs
1.  **Main Portal:** [psmsl.org](https://psmsl.org/)
2.  **Bulk Download Page:** [https://psmsl.org/data/obtaining/](https://psmsl.org/data/obtaining/)
3.  **Direct Download (Zipped):** [https://psmsl.org/data/obtaining/rlr.zip](https://psmsl.org/data/obtaining/rlr.zip) (RLR Data) and [https://psmsl.org/data/obtaining/met.zip](https://psmsl.org/data/obtaining/met.zip) (Metric Data).

### B. Data Format
The PSMSL data is distributed in highly accessible, plain-text formats:
-   **Station Data (.rlrdata / .metdata):** Space-delimited text files.
    -   **Columns:** Year, Month (or annual flag), Mean Sea Level (in mm), and a quality/missing-day flag.
    -   **Missing Values:** `-99999`.
-   **Metadata (filelist.txt / catalogue.dat):** Semi-colon or fixed-width text files containing station IDs, geographic coordinates (Lat/Lon), station names, and country codes.
-   **Ancillary Data:** Documentation on Revised Local Reference (RLR) datums and station history is provided as supplemental text files.

### C. Licensing, Costs, and Rate Limits
-   **License:** Creative Commons Attribution 4.0 International (CC BY 4.0).
-   **Cost:** Free of charge for all uses.
-   **Requirements:** Attribution is required. Users should cite PSMSL and the primary publication (Holgate et al., 2013).
-   **Rate Limits:** No operational rate limits for bulk downloads via the website.

### D. Dataset Size
-   **Total Size (Global):** Approximately **20 MB** zipped for the entire global historical record of monthly and annual averages.
-   **Uncompressed Size:** ~100-150 MB. 
-   **Note:** This dataset is extremely efficient because it provides processed averages rather than high-frequency raw sensor data (which is hosted by partner organizations like UHSLC).

### E. Estimated Effort
-   **Downloader:** **Very Low.** A single `wget` or `curl` command can retrieve the entire global dataset.
-   **Parser/Ingestion:** **Low.** The space-delimited text format is trivial to parse in Python, Go, or Node.js.
-   **Knowledge Graph Mapping:** **Moderate.**
    -   Mapping station IDs to modern geographic entities (countries, coastal cities) is straightforward using the provided Lat/Lon.
    -   The real value lies in the temporal linkage—connecting centuries of sea level trends to other historical events or climate indices.

## 4. Conclusion
The PSMSL dataset is a "gold standard" scientific dataset that is perfectly suited for a local knowledge graph. Its small size and simple format make it an easy target for scraping/downloading, while its high factual density and historical depth (some records dating back to the early 19th century) provide immense value for answering complex questions about planetary history and change.
