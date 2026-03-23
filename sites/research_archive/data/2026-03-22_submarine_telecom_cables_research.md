# Research Report: Global Submarine Telecom Cable Systems

## Date: 2026-03-22
## Topic: Global Submarine Telecom Cable Systems

---

## 1. Brainstorming Session

For this task run, the following novel dataset types were brainstormed as potential additions to a local knowledge graph:

1.  **Global Submarine Telecom Cable Systems**: Geographic and technical data on the backbone of the global internet, including landing points, owners, and cable lengths.
2.  **International Space Station (ISS) Microgravity Experiments Database**: Detailed records of scientific experiments conducted on the ISS, including results, principal investigators, and mission dates.
3.  **Global Volcanic Emissions & Ash Clouds (VAAC)**: Historical and real-time data on volcanic eruptions and the resulting ash cloud trajectories, used for aviation safety.
4.  **Traditional Ethnobotanical Knowledge (TEK) Databases**: Structured data on the traditional use of plants for medicinal or nutritional purposes by various cultures worldwide.
5.  **Global Hydroelectric Dam Technical Specifications**: Engineering data on major hydroelectric projects, including turbine types, generation capacity, and reservoir volumes.

### Selected Idea
**Global Submarine Telecom Cable Systems** was selected for research due to its high factual value, its critical role in global infrastructure, and the availability of structured geographic data that can be integrated into a knowledge graph.

---

## 2. Research Findings: Global Submarine Telecom Cable Systems

### Where can this data be obtained?
The most authoritative and comprehensive source for this data is **TeleGeography**. While they provide a paid API for commercial use, they maintain several public resources that can be leveraged for research and local storage:

*   **Public API (JSON)**: TeleGeography's interactive map (`submarinecablemap.com`) uses a JSON-based API. The main entry point for cable data is often found at: `https://www.submarinecablemap.com/api/v3/cable/all.json`
*   **GeoJSON Data**: Individual cable geometries can be fetched from: `https://www.submarinecablemap.com/api/v3/cable/[cable-id].json`
*   **GitHub Repositories**: TeleGeography maintains a public repository at [telegeography/www.submarinecablemap.com](https://github.com/telegeography/www.submarinecablemap.com) which occasionally includes static exports of the data.
*   **NOAA / Data.gov**: For cables specifically in U.S. waters, NOAA provides GeoJSON and KML datasets at [catalog.data.gov/dataset/submarine-cables](https://catalog.data.gov/dataset/submarine-cables).

### What is the format of the data?
*   **GeoJSON**: The primary format for the geographic polylines representing the cable routes.
*   **JSON**: Used for the metadata associated with each cable (name, length, owners, Ready for Service (RFS) date, landing points).
*   **CSV**: Available through community-cleaned versions on platforms like Kaggle.
*   **KML/Shapefile**: Commonly used in GIS-focused repositories like ArcGIS Hub or NOAA.

### Are there any rate limits, licensing restrictions, or costs associated with scraping/downloading it?
*   **Licensing**: TeleGeography's public data is typically provided under **CC BY-NC-SA 4.0** (Attribution-NonCommercial-ShareAlike). This means it is free for personal, educational, and research use, but commercial use requires a paid license.
*   **Rate Limits**: The public API on `submarinecablemap.com` does not have an explicitly published rate limit for small-scale use, but automated scraping should be done responsibly (e.g., with delays between requests) to avoid IP blocking.
*   **Costs**: Downloading the data from public repositories or the map's API is free. Accessing the official TeleGeography Global Bandwidth Research Service API is a premium paid product.

### How large is the dataset approximately?
*   The entire global dataset (approx. 550+ cables and 1,500+ landing points) is relatively small in terms of raw storage.
*   **Metadata (JSON)**: ~5-10 MB.
*   **Geometries (GeoJSON)**: ~20-50 MB depending on the level of detail/resolution of the polylines.
*   Total storage requirement is well under **100 MB**, making it ideal for local storage.

### What would be the estimated effort to write a scraper or download script for this data?
*   **Effort**: Low to Moderate.
*   **Strategy**:
    1.  Fetch the master list from `https://www.submarinecablemap.com/api/v3/cable/all.json`.
    2.  Iterate through the `id` of each cable.
    3.  Fetch the detailed JSON/GeoJSON for each cable from `https://www.submarinecablemap.com/api/v3/cable/[id].json`.
    4.  Parse and save to a local SQLite or DuckDB instance for the knowledge graph.
*   **Time Estimate**: A robust Python script using `requests` and `json` could be written and verified in **2-4 hours**.

---

## 3. Conclusion
The Global Submarine Telecom Cable Systems dataset is a "gold mine" for a local knowledge graph. It provides concrete, factual links between geographic locations (landing points), corporate entities (owners), and physical infrastructure (cables). Its manageable size and structured JSON format make it an excellent candidate for immediate ingestion.
