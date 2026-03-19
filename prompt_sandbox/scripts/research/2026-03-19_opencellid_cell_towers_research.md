# Research Report: Global Cell Tower Locations (OpenCellID)

**Date**: 2026-03-19  
**Topic**: Global Cell Tower Locations (OpenCellID)  
**Researcher**: Gemini CLI  

---

## 1. Brainstorming: Novel Dataset Ideas

The following dataset types were considered for inclusion in the local knowledge graph:

1.  **Global Cell Tower Locations (OpenCellID)**: Community-driven database of 40M+ cell tower coordinates and network parameters. High value for spatial and network analysis.
2.  **Global Address Point Data (OpenAddresses)**: Massive collection of 500M+ specific latitude/longitude points for street addresses worldwide. Essential for precise geocoding.
3.  **Global Mining Claims and Tenements**: GIS data on active mineral claims, typically sourced from national/state portals (e.g., BLM in the USA). High value for economic and geological research.
4.  **Global Language Distributions and Dialects (Glottolog)**: Genealogical and geographic data on thousands of world languages and dialects.
5.  **Global Postal Code Boundaries and Centroids**: High-resolution GIS data for postal regions, critical for logistics and regional analysis.

**Selected Idea**: **Global Cell Tower Locations (OpenCellID)**.  
*Rationale*: It is a highly structured, massive (40M+ rows), and manageable dataset (~4GB uncompressed) that provides unique factual data not yet covered in the existing research logs.

---

## 2. Research Findings: OpenCellID

### **Source & Access**
*   **Provider**: OpenCellID (maintained by Unwired Labs).
*   **URL**: [https://opencellid.org/](https://opencellid.org/)
*   **Access Method**: Bulk downloads are available after free registration. An API key is required to download the full database or country-specific subsets.

### **Data Format**
*   **Format**: Comma-Separated Values (CSV), typically compressed as `.gz`.
*   **Schema**:
    *   `radio`: Network type (GSM, UMTS, LTE, CDMA).
    *   `mcc`: Mobile Country Code.
    *   `net`: Mobile Network Code (MNC).
    *   `area`: Location Area Code (LAC) / Tracking Area Code (TAC).
    *   `cell`: Cell ID (CID).
    *   `lon` / `lat`: Longitude and Latitude coordinates.
    *   `range`: Estimated cell range in meters.
    *   `samples`: Number of measurements.
    *   `created` / `updated`: Unix Epoch timestamps.

### **Size & Scale**
*   **Compressed Size**: ~900 MB (`cell_towers.csv.gz`).
*   **Uncompressed Size**: ~3.3 GB to 4 GB.
*   **Row Count**: Approximately **40 million to 50 million** towers globally.

### **Licensing & Costs**
*   **License**: **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.
*   **Requirements**: Attribution to "OpenCellID" is mandatory. Any derivative works must be shared under the same license.
*   **Cost**: Free for community use. Commercial licenses (without the ShareAlike/Attribution requirements) are available through Unwired Labs.

### **Scraping & Implementation Effort**
*   **Estimated Effort**: **Low**.
*   **Implementation Strategy**:
    1.  Automate the download using a script that provides the OpenCellID API key.
    2.  Decompress the `.gz` file.
    3.  Load the CSV into a local SQLite or DuckDB database for efficient spatial querying.
    4.  (Optional) Index coordinates using R-Trees for fast geographic lookups.
*   **Rate Limits**: Free users are limited to **2 bulk downloads per day**, which is more than sufficient for periodic local updates.

---

## 3. Potential Use Cases for Knowledge Graph
*   **Geographic Resolution**: Answering "Which cell towers are near [Coordinate]?" or "What is the cell coverage like in [Region]?".
*   **Network Intelligence**: Mapping the reach of specific mobile network operators (MNCs) across different countries (MCCs).
*   **Offline Positioning**: Estimating location based on observed Cell IDs when GPS is unavailable.

---

## 4. Conclusion
The OpenCellID dataset is an ideal candidate for the local knowledge graph. It provides a massive, factual, and legally accessible spatial layer that enhances the system's ability to reason about global telecommunications infrastructure.
