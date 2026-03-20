# Research Report: Astronomical Catalogs (Stars & Messier Objects)

## Date: 2026-03-07
## Topic: Astronomical Catalogs for Knowledge Graphs

### 1. Brainstormed Ideas
- **Astronomical Catalogs (Stars & Messier Objects)**: Detailed data on stars (coordinates, magnitude, distance, spectral type) and deep-sky objects (Messier, NGC). (SELECTED)
- **Global Historical Conflict/Battle Database**: Structured data on historical battles, wars, casualties, and participants across centuries.
- **National Heritage/Registered Historic Places**: Official government lists of historical buildings, monuments, and sites with architectural and historical descriptions.
- **Global Biological Pathways/Metabolic Maps**: Highly structured biochemical data (e.g., KEGG/Reactome-like) detailing chemical interactions within organisms.
- **Historical Population/Census Data**: Aggregated decadal population data for cities and countries over the last 500+ years.

### 2. Selected Idea: Astronomical Catalogs (Stars & Messier Objects)
This dataset provides a factual foundation for questions regarding the universe's structure, stellar properties, and deep-sky objects. It is highly structured and fits perfectly into a graph-based or relational local database.

### 3. Research Findings

#### A. Where can this data be obtained?
- **Messier Catalog**: 
    - **Datastro**: [Messier Catalog Export](https://www.datastro.eu/explore/dataset/catalogue-de-messier/export/) (Highly recommended for structured data).
    - **GitHub (messier-api)**: [messier.json](https://github.com/osricdienda/messier-api/blob/master/data/messier.json)
- **HYG Database (Hipparcos, Yale Bright Star, and Gliese)**:
    - **The Astronomy Nexus**: [HYG Database Page](http://www.astronexus.com/hyg) (Contains ~120,000 stars).
- **NASA Bright Star Catalog**:
    - **NASA Open Data Portal**: [Bright Star Catalog](https://data.nasa.gov/Space-Science/Bright-Star-Catalog/29ur-65nc) (Focuses on naked-eye stars).

#### B. Data Formats
- **Messier**: JSON, CSV, GeoJSON, Excel.
- **HYG Database**: CSV (available as `.zip` or `.gz`).
- **NASA Bright Star**: CSV, JSON.

#### C. Rate Limits, Licensing, and Costs
- **Licensing**: Most of these datasets are Public Domain or released under Creative Commons (CC-BY). The HYG database is open data for any use. NASA data is public domain.
- **Rate Limits**: These are bulk downloads, so there are no API rate limits once the file is downloaded.
- **Costs**: Free.

#### D. Approximate Size
- **Messier Catalog**: Very small (< 1 MB).
- **HYG Database (120k stars)**: Approximately 10-30 MB (CSV).
- **Extended Catalogs (e.g., Gaia)**: These can reach TBs, but for a general knowledge graph, HYG (120k stars) or the Bright Star catalog (9k stars) is sufficient.

#### E. Estimated Effort to Scrape/Download
- **Effort**: Low.
- **Method**: Direct bulk download via `curl` or `wget`. No complex scraping is required. A simple Python script can parse the CSV/JSON and insert it into a local knowledge graph or database.

### 4. Conclusion & Next Steps
The Astronomical Catalogs are a "low-hanging fruit" for the knowledge graph. They provide high-value factual data with minimal effort. The HYG database should be the primary source for stars, and Datastro should be used for Messier objects due to its inclusion of image URLs and detailed metadata.
