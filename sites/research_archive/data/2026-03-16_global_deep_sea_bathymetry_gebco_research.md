---
title: "Global Deep-Sea Bathymetry (GEBCO)"
date: 2026-03-16
category: "Earth & Environment"
tags: ["ocean", "bathymetry", "gebco", "seafloor", "geospatial"]
---

# Knowledge Graph Research: Global Deep Sea Bathymetry & Undersea Feature Names (GEBCO)

**Date**: 2026-03-16
**Topic**: Deep Sea Bathymetry and Undersea Feature Names
**Researcher**: Gemini CLI

---

## 1. Brainstorming: Novel Dataset Types
The following dataset types were brainstormed as potential additions to the local knowledge graph:

1.  **Global Historical Cinema/Film Technical Metadata**: Deep technical specs (lenses, aspect ratios, frame rates) from archives like the AFI Catalog.
2.  **Global Biological Weapons/Pathogen Research Labs (OSINT)**: Locations and biosafety levels of high-risk research facilities based on open-source intelligence.
3.  **Global Space Weather/Ionospheric Data**: Historical records of geomagnetic storms and solar activity from NOAA SWPC.
4.  **Global Deep Sea Bathymetry and Undersea Feature Names (GEBCO)**: Mapping the ocean floor topography and the official names of undersea geological features.
5.  **Global Rare Earth Element (REE) Mining & Processing Facilities**: Tracking the critical mineral supply chain and refinery locations.

**Selected Idea**: *Global Deep Sea Bathymetry and Undersea Feature Names (GEBCO)*.

---

## 2. Research Findings: GEBCO Dataset

### Where can this data be obtained?
The data is managed by the General Bathymetric Chart of the Oceans (GEBCO) and the International Hydrographic Organization (IHO).

*   **Bathymetric Grid (Topography)**:
    *   **Primary Portal**: [download.gebco.net](https://download.gebco.net) (and the new beta at [betadownload.gebco.net](https://betadownload.gebco.net)).
    *   **Programmatic Access**: OPeNDAP server via CEDA or the [OpenTopography API](https://opentopography.org).
*   **Undersea Feature Names (Gazetteer)**:
    *   **IHO DCDB Gazetteer**: [www.ngdc.noaa.gov/gazetteer/](https://www.ngdc.noaa.gov/gazetteer/).
    *   **GEBCO Website**: [www.gebco.net/data_and_products/undersea_feature_names/](https://www.gebco.net/data_and_products/undersea_feature_names/).

### What is the format of the data?
*   **Bathymetry**:
    *   **netCDF**: The native format for the global grid.
    *   **GeoTIFF**: Tiled or user-defined areas, ideal for GIS integration.
    *   **Esri ASCII Raster**: Common for legacy GIS tools.
*   **Gazetteer (Feature Names)**:
    *   **Geospatial**: Shapefile (.shp), KML, TopoJSON.
    *   **Tabular**: CSV, TSV, JSON, and **Linked Places Format (LPF)** (excellent for knowledge graphs).

### Are there any rate limits, licensing restrictions, or costs?
*   **Cost**: Free of charge.
*   **Licensing**: The data is **Public Domain**. Most platforms (like OpenTopography) distribute it under **CC BY 4.0** to ensure proper attribution.
*   **Restrictions**: Must not be used for navigation or safety-at-sea. Attribution is mandatory (e.g., citing the GEBCO Compilation Group).
*   **Rate Limits**: Standard web portals have no strict limits for browser downloads; API access via OpenTopography or OPeNDAP may have typical tiered limits for high-volume users.

### How large is the dataset approximately?
*   **Bathymetry (GEBCO_2024/2025)**:
    *   **Compressed**: ~4 GB.
    *   **Uncompressed**: ~7.5 GB to 8 GB for the global 15 arc-second grid.
*   **Gazetteer**:
    *   **Record Count**: ~4,500 to 4,800 named features.
    *   **File Size**: < 10 MB (highly efficient for text-based knowledge graphs).

### Estimated effort to write a scraper or download script?
*   **Effort**: **Low to Medium**.
    *   **Gazetteer**: **Low**. A simple `curl` or `requests` call can fetch the JSON or CSV version of the gazetteer.
    *   **Bathymetry**: **Medium**. While downloading the 4GB file is easy, processing a 7.5GB raster grid to extract specific depth data for coordinates or to generate local "terrain cards" for a knowledge graph requires specialized libraries like `gdal` or `xarray`.
    *   **Integration**: The Linked Places Format (LPF) for the gazetteer makes it natively compatible with many graph-based data structures.

---

## 3. Conclusion
The GEBCO dataset is a high-value addition to a local knowledge graph. The combination of the semantic layer (named features like the "Mariana Trench") and the raw physical layer (actual depth readings) allows the graph to answer questions ranging from "Where is the deepest point on Earth?" to "What is the topography of the Mid-Atlantic Ridge?".
