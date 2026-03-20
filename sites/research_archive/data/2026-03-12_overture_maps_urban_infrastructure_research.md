# Research Report: Global Urban Infrastructure (Overture Maps Foundation)

**Date**: 2026-03-12  
**Researcher**: Gemini CLI  
**Topic**: Global Urban Infrastructure and Building Footprints (Overture Maps)

---

## 1. Brainstormed Ideas
Before selecting this topic, the following novel dataset types were brainstormed:
1. **Global Urban Infrastructure (Overture Maps Foundation)**: Highly structured geospatial data including billions of building footprints, heights, and points of interest. (SELECTED)
2. **Historical Currency Exchange Rates**: Long-term records of global currency values and transitions over centuries.
3. **Maritime Piracy and Security Incidents**: Detailed logs of global maritime security events, including spatial and temporal data.
4. **Global Flora and Botanical Specimens**: Comprehensive databases of plant species distributions and herbarium records (beyond general biodiversity).
5. **Historical Newspaper Metadata and OCR**: Large-scale datasets of newspaper archives for historical event tracking.

---

## 2. Selected Idea: Overture Maps Foundation
Overture Maps is a collaborative project (founded by Meta, Amazon, Microsoft, and TomTom) that provides a massive, high-quality, and open map dataset. It is specifically designed to be "conflated," meaning it combines data from various sources (OpenStreetMap, Microsoft, Google Open Buildings, Esri) into a single, unified schema.

---

## 3. Research Findings

### Where can this data be obtained?
*   **Official Website**: [overturemaps.org](https://overturemaps.org/)
*   **Direct Access**: The data is hosted on **Amazon S3** (`s3://overturemaps-us-west-2/release/`) and **Azure Blob Storage**.
*   **Tools**: 
    *   **Overture Python Client**: `pip install overturemaps` (simplest way to download subsets).
    *   **DuckDB**: Highly recommended for querying the remote files directly via SQL.

### What is the format of the data?
*   **GeoParquet**: A cloud-native, columnar storage format optimized for large-scale geospatial queries. It includes spatial metadata that allows for efficient filtering and partitioning.
*   **Schema Layers**: The data is organized into "themes":
    *   **Buildings**: Over 2.3 billion building footprints.
    *   **Places**: ~50 million points of interest (businesses, landmarks).
    *   **Transportation**: Road, rail, and water networks.
    *   **Divisions**: Administrative boundaries.
    *   **Base**: Land cover and water bodies.

### Rate limits, licensing, and costs
*   **Licensing**: A "mixed" model to ensure compatibility:
    *   **ODbL v1.0**: Used for Buildings, Transportation, and Divisions (derived from OSM).
    *   **CDLA-Permissive-2.0**: Used for Places and Addresses.
*   **Costs**: The data itself is free and open. Egress costs from S3/Azure apply if you download the full dataset, but are minimal for specific regions.
*   **Rate Limits**: None, as it is hosted on public cloud buckets.

### How large is the dataset?
*   **Total Release**: Approximately **450 GB - 500 GB** in compressed GeoParquet format.
*   **Buildings Layer**: The largest component, containing over 2.3 billion features and taking up the majority of the storage.
*   **Granularity**: Individual cities can be downloaded in MBs, making it highly flexible for local use.

### Technical Implementation & Effort
*   **Effort**: **Low to Moderate**.
*   **Scraper/Download Script**: No complex "scraper" is needed. A simple Python script using the `overturemaps` library can pull data by bounding box.
*   **Knowledge Graph Integration**: The **Global Entity Reference System (GERS)** is a standout feature. It assigns a persistent UUID to every entity. This allows for:
    *   Linking a "Place" (e.g., a restaurant) to its containing "Building" via IDs.
    *   Stable updates: When the dataset is updated monthly, the IDs remain the same, allowing a local knowledge graph to update attributes without losing relationships.
    *   **Example Join**: Using DuckDB, one can join the Buildings and Places layers on `parent_id` in minutes.

---

## 4. Conclusion & Recommendation
Overture Maps is a "gold mine" for a local knowledge graph. Its high-quality building footprints and persistent GERS IDs provide the structural "skeleton" for a spatial world model. 

**Next Steps**: 
- Install the `overturemaps` Python client.
- Download a sample GeoParquet file for a local region (e.g., a home city) to test schema ingestion.
- Evaluate DuckDB for full-scale global processing.
