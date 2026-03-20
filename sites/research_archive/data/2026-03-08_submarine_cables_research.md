# Research Report: Global Infrastructure & Connectivity (Submarine Cables)

**Date**: 2026-03-08
**Topic**: Submarine Cables
**Researcher**: Gemini CLI

---

## 1. Brainstormed Ideas
For this task, the following novel dataset types were considered for potential integration into the local knowledge graph:

1.  **Global Historical Conflict/Battle Records**: Specific dates, locations, combatants, and outcomes of historical battles (e.g., Correlates of War dataset, battlefields.org).
2.  **Archaeological Sites and Excavations**: Data on registered archaeological sites worldwide, including civilization, age, and significant finds (e.g., Open Context, ARIADNE+).
3.  **Endangered Language Audio/Text Corpora**: Recordings and transcripts of languages at risk of extinction (e.g., ELAR - Endangered Languages Archive).
4.  **Global Infrastructure & Connectivity (Submarine Cables)**: Locations, landing points, and capacities of international submarine telecommunications cables.
5.  **Historical Climate/Paleoclimate Data**: Deep historical climate records derived from ice cores, tree rings, and sediment (e.g., NOAA World Data Service for Paleoclimatology).

---

## 2. Selected Idea: Submarine Cables
The selected topic for this research cycle is **Global Infrastructure & Connectivity (Submarine Cables)**. This data provides a fascinating spatial and relational layer for a knowledge graph, connecting countries, companies, and historical timelines of global communication infrastructure.

---

## 3. Research Findings

### A. Data Sources
The primary and most comprehensive public source for submarine cable data is **TeleGeography's Submarine Cable Map**. While their GitHub repository is archived, the interactive map remains active and serves data through a public API.

*   **Primary Website**: [https://www.submarinecablemap.com](https://www.submarinecablemap.com)
*   **API Endpoints**:
    *   **Cables (GeoJSON)**: `https://www.submarinecablemap.com/api/v3/cable/cable-geo.json`
    *   **Landing Points (GeoJSON)**: `https://www.submarinecablemap.com/api/v3/landing-point/landing-point-geo.json`
    *   **All Cables Metadata (JSON)**: `https://www.submarinecablemap.com/api/v3/cable/all.json`
    *   **Individual Cable Details**: `https://www.submarinecablemap.com/api/v3/cable/{slug}.json` (e.g., `2africa.json`)

### B. Data Format
*   **Format**: Primarily **JSON** and **GeoJSON**.
*   **Structure**: The GeoJSON files contain line geometries (cables) and point geometries (landing sites). The metadata JSONs include cable names, owners, length (km), Ready For Service (RFS) dates, and website URLs.

### C. Licensing & Costs
*   **Licensing**: The data is **Copyright © TeleGeography**.
*   **Usage**: It is free for viewing and non-commercial research. Commercial use or redistribution of the raw data requires a paid license from TeleGeography.
*   **Costs**: Free for the public API access and personal/research use cases. High-precision GIS data (RPLs) are sold as premium products.

### D. Dataset Size
*   **Estimated Size**: Very compact. The primary GeoJSON and metadata files are likely **< 20 MB** combined. Even a full crawl of individual cable slugs for detailed metadata would likely stay under **50 MB**.

### E. Implementation Effort
*   **Effort Level**: **Low (1/10)**.
*   **Strategy**:
    1.  Fetch `all.json` to get a list of all cable slugs.
    2.  Download `cable-geo.json` and `landing-point-geo.json` for spatial mapping.
    3.  Iterate through the slugs in `all.json` to fetch detailed records for each cable to populate the knowledge graph with owners and technical specs.

---

## 4. Conclusion
The Submarine Cable dataset is a "low-hanging fruit" with extremely high value for a knowledge graph. It provides concrete links between geography (landing points), corporations (owners), and history (RFS dates). The data is well-structured and easy to retrieve using simple HTTP requests.
