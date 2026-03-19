# Knowledge Graph Data Research: NASA Exoplanet Archive

## Date: 2026-03-06

## Brainstormed Ideas
1.  **NASA Exoplanet Archive**: Detailed properties of discovered exoplanets (mass, radius, orbit, host star).
2.  **USGS Earthquake Catalog**: Historical and real-time global seismic data (magnitudes, locations, depths).
3.  **National Gallery of Art (NGA) Open Access**: Metadata for over 150,000 artworks (artist, medium, date, dimensions).
4.  **OpenStreetMap (OSM) Planet Dumps**: Massive GIS dataset for everything from roads to buildings and local landmarks.
5.  **Project Gutenberg Metadata**: Bibliographic data for tens of thousands of public domain books.

---

## Selected Idea: NASA Exoplanet Archive
The NASA Exoplanet Archive is a world-class resource for astronomical data, specifically focusing on confirmed planets outside our solar system and the stars they orbit. This data is highly structured and provides a deep, factual foundation for astronomical knowledge.

### Research Findings

#### 1. Source and Access
- **Primary URL**: [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/)
- **Programmatic Access (TAP)**: The Table Access Protocol (TAP) is the recommended method for querying tables using ADQL (Astronomical Data Query Language, similar to SQL).
    - Base URL: `https://exoplanetarchive.ipac.caltech.edu/TAP/`
- **Legacy API**: Still available for certain older tables.
    - Base URL: `https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?`

#### 2. Data Formats
The archive supports multiple formats for both TAP and API queries:
- **CSV** (Comma-Separated Values)
- **TSV** (Tab-Separated Values)
- **JSON**
- **IPAC Table** (ASCII format)
- **XML/VOTable** (Standard for Virtual Observatory tools)

#### 3. Licensing, Costs, and Rate Limits
- **Licensing**: NASA-generated data is generally in the **Public Domain** (CC0). It is free to use, reproduce, and distribute for any purpose. 
- **Citation**: While the data is free, users are "strongly urged" to cite the NASA Exoplanet Archive and the original scientific publications.
- **Costs**: Free.
- **Rate Limits**:
    - **Standard API Key**: 1,000 requests per hour.
    - **DEMO_KEY**: 30 requests per hour / 50 requests per day.
    - Large bulk downloads are encouraged through the dedicated bulk service to avoid hitting API limits.

#### 4. Dataset Size
- **Planetary Systems (ps) Table**: Contains records for ~5,000+ confirmed planets. This table is relatively small (tens of MBs in CSV format).
- **Mission-Specific Tables**: Mission tables like UKIRT or Kepler can contain tens of millions of rows (e.g., UKIRT has 66M+ targets), which can reach into the GB range.
- For a local knowledge graph, focusing on confirmed planets and their basic properties is a high-value, low-storage-cost starting point.

#### 5. Estimated Scraping/Download Effort
- **Effort Level**: **Very Low** for confirmed planets.
- **Strategy**: A simple Python script using `requests` to fetch the `ps` (Planetary Systems) table via the TAP service in CSV or JSON format.
- **Example Query**: `https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=SELECT+*+FROM+ps&format=csv`
- For larger mission tables, more complex ADQL queries and pagination may be required, increasing effort to **Low/Moderate**.

### Potential for Knowledge Graph
This data can be used to build a robust astronomical ontology, linking planets to stars, stellar systems, and discovery missions. It allows for complex queries like "Which planets discovered in the last 5 years are in the habitable zone of their star?" or "What is the most common discovery method for Earth-sized planets?"
