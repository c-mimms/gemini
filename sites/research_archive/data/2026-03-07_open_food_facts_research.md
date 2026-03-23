---
title: "Open Food Facts Database"
date: 2026-03-07
category: "Life Sciences"
tags: ["food", "nutrition", "consumer-data", "open-data", "diet"]
---

# Research Report: Open Food Facts Database

**Date:** 2026-03-07
**Topic:** Open Food Facts (Crowdsourced Food Product Knowledge)
**Status:** Completed

---

## 1. Brainstorming: Novel Dataset Ideas

The following dataset types were brainstormed as potential high-value, factual, and locally storable sources for a knowledge graph:

1.  **Open Food Facts Database**: [SELECTED] A global database of food products, including ingredients, nutrition, allergens, additives, and environmental impact (Eco-score).
2.  **MusicBrainz Database (The Music Encyclopedia)**: Structured data on artists, albums, tracks, labels, and their complex relationships (e.g., "remixed by", "covered by").
3.  **World Bank Open Data**: Over 16,000 socio-economic indicators (GDP, population, health metrics) for 217 economies, providing a deep statistical layer for historical and geographical queries.
4.  **USPTO/EPO Patent Metadata (Innovation History)**: Millions of patent records including titles, abstracts, inventors, and classifications, allowing for a graph of human technological evolution.
5.  **OpenStreetMap (OSM) Points of Interest (POIs)**: Extraction of structured factual metadata from the global map (monuments, historical sites, landmarks) with precise coordinates and attributes.

---

## 2. Selected Idea Research: Open Food Facts

### 2.1 Overview
Open Food Facts is a non-profit, collaborative project that has built the world's largest open database of food products. It contains deep, structured data on millions of items, making it an ideal "consumer knowledge" layer for a local knowledge graph.

### 2.2 Data Sources & URLs
*   **Main Data Portal:** [world.openfoodfacts.org/data](https://world.openfoodfacts.org/data)
*   **JSONL Export:** [static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz](https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz)
*   **MongoDB Dump:** [static.openfoodfacts.org/data/mongodb/](https://static.openfoodfacts.org/data/mongodb/)
*   **Parquet/Hugging Face:** [huggingface.co/datasets/openfoodfacts/openfoodfacts-products](https://huggingface.co/datasets/openfoodfacts/openfoodfacts-products)

### 2.3 Data Formats
*   **JSONL (NDJSON):** The primary recommendation for bulk processing. Each line is a full JSON object for a single product.
*   **MongoDB Dump:** Full BSON export of the database.
*   **CSV/TSV:** A simplified subset of fields (useful for quick analysis but loses nested structure like ingredients hierarchy).
*   **RDF (Turtle/XML):** Native linked-data format (limited availability compared to JSONL).
*   **Images:** Millions of product and nutrition label images are available via the AWS Open Data Program.

### 2.4 Licensing, Costs, and Restrictions
*   **License:** **Open Database License (ODbL)** for the database. **CC-BY-SA** for product images.
*   **Cost:** Free for all uses, including commercial.
*   **Restrictions:** Requires attribution ("Data from Open Food Facts") and any derived database must be shared under the same ODbL license (Share-Alike).

### 2.5 Dataset Size & Rate Limits
*   **Product Count:** ~3.7 million+ products (as of 2026).
*   **JSONL Compressed Size:** ~7 GB (`.gz`).
*   **JSONL Uncompressed Size:** ~45-50 GB.
*   **MongoDB Dump Size:** ~15 GB compressed, >35 GB uncompressed.
*   **Rate Limits:** No rate limits for data dumps. The JSON API has limits (100 req/min for product lookup), but dumps are the preferred method for knowledge graph ingestion.

### 2.6 Estimated Effort for Scraping/Downloading
*   **Downloading:** **Low.** Single large files are available via high-speed mirrors or AWS.
*   **Ingestion/Parsing:** **Moderate.**
    *   The JSON schema is deep and complex (hundreds of fields per product).
    *   Ingredients are provided as both raw strings and parsed hierarchies.
    *   Requires a streaming parser (e.g., Python's `ijson` or standard `json` line-by-line) due to the 50GB uncompressed size.
*   **Scraper Effort:** **Zero.** No scraper is needed; the data is provided as a clean, nightly bulk export.

---

## 3. Conclusion & Next Steps
Open Food Facts is a "Tier 1" dataset for a local knowledge graph focused on daily life, health, and consumer transparency. Its structured nature (ingredients list, nutrition grades) allows for complex queries that generic search engines struggle with (e.g., "List all cereals with no palm oil and >10g protein").

**Next Action:** Download a small sample (e.g., the first 10,000 lines of the JSONL file) to map the schema into a graph database (Neo4j or a local RDF triple store).
