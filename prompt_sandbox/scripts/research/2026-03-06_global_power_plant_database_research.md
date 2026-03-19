# Research Report: Global Power Plant Database (WRI)

**Date:** 2026-03-06  
**Topic:** Global Power Generation Infrastructure (Energy Knowledge)  
**Status:** Completed

---

## 1. Brainstorming: Novel Dataset Ideas

The following dataset types were brainstormed as potential high-value sources for a local knowledge graph. These focus on structured, factual data that provides a "ground truth" for global infrastructure, economics, and environmental science.

1.  **Global Power Plant Database (WRI)**: [SELECTED] A comprehensive, open-source database of nearly 35,000 power plants worldwide, including their location, capacity, fuel type, and ownership.
2.  **World Database on Protected Areas (WDPA)**: The most comprehensive global database on terrestrial and marine protected areas (National Parks, Nature Reserves, etc.), providing essential GIS boundaries and legal status.
3.  **The GDELT Project (Global Database of Events, Language, and Tone)**: A massive, real-time monitor of global news that extracts actors, locations, and over 300 categories of physical actions (protests, diplomatic meetings, etc.) into a structured format.
4.  **UN FAOSTAT (Agriculture & Food Statistics)**: Global data on agricultural production, livestock, land use, and food security by country and year—fundamental for economic and demographic knowledge.
5.  **International Seismological Centre (ISC) Bulletin**: The definitive historical record of the world's seismicity, providing highly accurate, peer-reviewed data on earthquake locations, magnitudes, and phases.

---

## 2. Selected Idea Research: Global Power Plant Database (WRI)

### 2.1 Overview
The Global Power Plant Database, maintained by the World Resources Institute (WRI), is a foundational dataset for understanding global energy infrastructure. It provides a granular look at how the world generates power, allowing for complex queries regarding energy transition, carbon intensity, and national grid capacities.

### 2.2 Data Sources & URLs
*   **Official Project Page:** [wri.org/data/global-power-plant-database](https://www.wri.org/data/global-power-plant-database)
*   **GitHub Repository:** [github.com/wri/global-power-plant-database](https://github.com/wri/global-power-plant-database)
*   **Direct Download (v1.3.0):** Typically available via a ZIP file on the WRI data portal or as a CSV in the GitHub `output_database` directory.
*   **Google Earth Engine:** Accessible as a `FeatureCollection` for spatial analysis.

### 2.3 Data Formats
*   **Primary Format:** CSV (Comma-Separated Values).
*   **GIS Formats:** GeoJSON (often available via mirrors or derived from the CSV).
*   **Metadata:** JSON/TXT files describing the sources and methodology for each country.

### 2.4 Licensing, Costs, and Restrictions
*   **License:** **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
    *   *Permissions:* You are free to share, copy, and adapt the data for any purpose, even commercially.
    *   *Requirements:* You must give appropriate credit and provide a link to the license.
*   **Cost:** Free.
*   **Restrictions:** As of early 2022, WRI indicated that the project is no longer actively maintained (v1.3.0 is the final version). Users should be aware that data for newer plants (post-2021) may be missing.

### 2.5 Dataset Size & Scope
*   **Number of Entries:** ~34,936 power plants.
*   **Geographic Coverage:** 167 countries.
*   **Total Capacity:** ~14,000 GW (Gigawatts).
*   **File Size:**
    *   **Compressed (ZIP):** ~5–10 MB.
    *   **Uncompressed (CSV):** ~20–25 MB.
*   **Local Storage Impact:** Extremely low. The entire dataset fits easily in memory on modern systems.

### 2.6 Key Data Fields
*   `name`: Name of the power plant.
*   `gppd_idnr`: Unique identifier.
*   `capacity_mw`: Installed electrical capacity in megawatts.
*   `latitude` / `longitude`: Precise geolocation.
*   `primary_fuel`: The main energy source (Coal, Gas, Hydro, Nuclear, Solar, Wind, etc.).
*   `owner`: The company or entity that owns the plant.
*   `estimated_generation_gwh`: Modeled annual electricity generation.

### 2.7 Estimated Effort for Scraping/Downloading
*   **Downloading:** **Very Low.** A single `wget` or `curl` command can retrieve the entire database.
*   **Processing:** **Low.** Standard data libraries (Pandas, DuckDB, SQLite) can ingest and query the CSV in seconds.
*   **KG Integration:** **Moderate.** Mapping the `owner` field to a corporate entity KG (like OpenCorporates or Wikidata) would add significant value but requires entity resolution.

---

## 3. Conclusion & Recommendation
The Global Power Plant Database is an "easy win" for a local knowledge graph. Its small size, high level of structure, and permissive license make it a perfect candidate for immediate ingestion. It provides the "physical layer" for questions about geography, economics, and climate.

**Next Action:** Download the v1.3.0 CSV from GitHub and create a script to map the `primary_fuel` and `owner` fields to a local graph schema.
