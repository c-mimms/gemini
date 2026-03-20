# Knowledge Graph Data Research: World Database on Protected Areas (WDPA)

## Date: 2026-03-07

## Brainstormed Ideas
1.  **World Database on Protected Areas (WDPA)**: Locations, designations, and governance of all protected areas globally.
2.  **Global Dam and Reservoir Database (GRanD)**: Comprehensive data on dams, reservoirs, and their characteristics.
3.  **Historical Population Census Data (NHGIS/IPUMS)**: Spatiotemporal population data for historical analysis.
4.  **Global Registry of Migratory Species (GROMS)**: Tracking patterns and biological information of migratory animals.
5.  **Global Patent Database**: Structured data on inventions, assignees, and dates from major patent offices.

## Selected Idea: World Database on Protected Areas (WDPA)

### Overview
The World Database on Protected Areas (WDPA) is the most comprehensive global database of terrestrial and marine protected areas. It is a joint project between UN Environment Programme World Conservation Monitoring Centre (UNEP-WCMC) and the International Union for Conservation of Nature (IUCN).

### Research Findings

#### 1. Where can this data be obtained?
- **Primary Website**: [ProtectedPlanet.net](https://www.protectedplanet.net)
- **Direct Downloads**: Full global datasets are available for download after creating a free account.
- **Official API**: [api.protectedplanet.net](https://api.protectedplanet.net) (requires a personal API token).
- **Cloud Platforms**: Also available on Google Earth Engine as `WCMC/WDPA/current/polygons`.

#### 2. What is the format of the data?
- **Spatial Formats**: ESRI Shapefile, File Geodatabase (GDB).
- **Non-Spatial Formats**: CSV (attribute data only).
- **Structure**: Includes polygon geometries (91%) and point locations (9%), with detailed attributes such as name, designation type (National Park, Nature Reserve, etc.), status, and year of establishment.

#### 3. Are there any rate limits, licensing restrictions, or costs associated with scraping/downloading it?
- **Licensing**: 
    - **Non-Commercial Use**: Free for educational and scientific purposes.
    - **Commercial Use**: Strictly restricted; commercial entities must use the Integrated Biodiversity Assessment Tool (IBAT).
    - **Redistribution**: Prohibited. The data cannot be redistributed in whole or part via third-party apps or services.
- **Costs**: Free for non-commercial use.
- **Rate Limits**: The API requires a token and has standard rate limiting for personal use.

#### 4. How large is the dataset approximately?
- **Compressed Size**: Approximately 1GB to 3GB for the global ZIP file.
- **Uncompressed Size**: Can exceed 10GB+ depending on the format, as spatial geometries for 285,000+ protected areas are highly detailed.

#### 5. What would be the estimated effort to write a scraper or download script for this data?
- **Effort**: **Low**.
- **Approach**: Since the full dataset is available as a direct download (ZIP), a script would simply need to handle authentication (if automated) or download the file manually once a month. For more granular updates or specific queries, the official API is well-documented. R packages like `wdpar` already exist to automate this process.

### Conclusion
The WDPA is an excellent candidate for a knowledge graph, providing deep factual and spatial links between geographic locations and environmental conservation status. While the size is significant, it is manageable for local storage. The main constraint is the strict non-commercial licensing and redistribution policy.
