---
title: "Global Cave & Karst Systems Database"
date: 2026-03-17
category: "Earth & Environment"
tags: ["caves", "karst", "geology", "speleology", "geography"]
---

# Research Report: Global Subterranean Infrastructure (Caves and Karst Systems)

**Date**: 2026-03-17  
**Topic**: Global Subterranean Infrastructure (Caves and Karst Systems)  
**Researcher**: Gemini CLI  

---

## 1. Brainstorming: Novel Dataset Ideas

The following dataset types were brainstormed as potential additions to the local knowledge graph:

1.  **Global Subterranean Infrastructure (Caves and Karst Systems)**: Databases of known cave systems, their dimensions, geology, and biological features. (SELECTED)
2.  **Global Botanical Garden Collections (BGCI PlantSearch)**: Living collections of plant species across thousands of gardens worldwide, essential for biodiversity knowledge.
3.  **Global Historical Currency & Inflation Data**: Long-term historical records of currency exchange rates and purchasing power across different eras and regions.
4.  **Global Particle Accelerator and High-Energy Physics Facilities**: Metadata on experimental facilities, their technical specifications, and historical research output.
5.  **Global Historical Typography and Printing (Incunabula Short Title Catalogue)**: Factual data on the earliest printed books (before 1501), including locations, printers, and editions.

---

## 2. Selected Idea: Global Subterranean Infrastructure (Caves and Karst Systems)

This topic focus on the "unseen" physical and geological features of the Earth's crust, specifically karst landscapes and the caves within them. This data provides critical spatial and environmental knowledge for the local knowledge graph.

---

## 3. Detailed Research Findings

### A. Key Datasets and Sources

#### 1. WOKAM (World Karst Aquifer Map)
*   **Description**: A global geodatabase of karstifiable rocks (carbonates and evaporites), identifying areas where caves and subterranean systems are most likely to exist.
*   **Source**: BGR (German Federal Institute for Geosciences and Natural Resources) / WHYMAP.
*   **URL**: [WHYMAP WOKAM Official Page](https://www.whymap.org/whymap/EN/Maps_Data/Wokam/wokam_node_en.html)
*   **Format**: ESRI Shapefile (Vector).
*   **License**: CC BY 4.0.
*   **Size**: ~21.0 MB (compressed ZIP).
*   **DOI**: `10.25928/b2.21_sfkq-r406`

#### 2. WoKaS (World Karst Spring hydrograph database)
*   **Description**: A global database of karst spring discharge observations, providing hydrological data for subterranean systems.
*   **Source**: Figshare (Olarinoye, Hartmann, et al.).
*   **URL**: [Figshare - WoKaS Database](https://doi.org/10.6084/m9.figshare.9638939.v2)
*   **Format**: CSV.
*   **License**: CC BY 4.0.
*   **Size**: ~24.7 MB.
*   **DOI**: `10.6084/m9.figshare.9638939.v2`

#### 3. Grottocenter (WikiCaves)
*   **Description**: The most comprehensive global database for cave metadata, including names, locations (coordinates), lengths, depths, and organization data.
*   **Source**: Wikicaves Association / UIS (International Union of Speleology).
*   **URL**: [grottocenter.org](https://www.grottocenter.org) (Data portal: [data.grottocenter.org](https://data.grottocenter.org))
*   **Format**: CSV (Advanced Search export), JSON-LD (KarstLink), and Monthly JSON Dumps.
*   **License**: CC BY-SA (Creative Commons Attribution-ShareAlike).
*   **Size**: Tens to hundreds of MBs (31,000+ cave entries as of 2013, significantly larger now).
*   **Standards**: KarstLink (RDF, JSON-LD, Turtle) and UISIC field definitions (over 680 fields).

### B. Technical Evaluation

*   **Rate Limits / Restrictions**: 
    *   WOKAM and WoKaS have no specific rate limits for bulk downloads.
    *   Grottocenter's full JSON dump is typically restricted to association members/partners, but the **Advanced Search CSV export** and **JSON-LD API** are accessible for general research.
*   **Estimated Effort**: 
    *   **Low to Moderate**. 
    *   WOKAM requires `geopandas` or `fiona` (Python) to parse Shapefiles into coordinates/polygons.
    *   WoKaS is a standard CSV, easily parsed with `pandas`.
    *   Grottocenter data can be ingested via their JSON-LD endpoints or a bulk CSV export from the search interface. KarstLink support makes it highly suitable for semantic knowledge graphs.
*   **Storage Requirements**: Total estimated local storage for all three datasets is under **500 MB**, making it very efficient for local storage.

---

## 4. Conclusion and Next Steps

The combination of WOKAM (geology), WoKaS (hydrology), and Grottocenter (infrastructure) provides a complete three-tiered view of global subterranean systems. 

**Recommended Action**: Download the WOKAM shapefile and WoKaS CSV first, as they are high-quality, static scientific datasets with open CC BY 4.0 licenses. Grottocenter should be used for specific cave-level metadata using its KarstLink-compliant exports.
