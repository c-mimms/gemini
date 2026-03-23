# Research Report: Global Architectural Heritage & Listed Buildings

## Goal
The goal of this research is to evaluate datasets related to global architectural heritage and listed buildings for inclusion in a local knowledge graph.

## Brainstormed Ideas
1.  **Global Seamount & Undersea Feature Database**: Data on undersea mountains and features.
2.  **International Treaty and Agreement Repository**: Historical and active international treaties.
3.  **Global Architectural Heritage & Listed Buildings**: Structured data on historical buildings and monuments.
4.  **Global Frequency Allocations & Spectrum Usage**: Radio spectrum usage mapping.
5.  **Chemical Synthesis & Reaction Databases (Open Source)**: Data on chemical reactions and outcomes.

## Selected Idea: Global Architectural Heritage & Listed Buildings
This dataset provides deep, factual knowledge about human history, culture, and geography, making it a high-value addition to a knowledge graph.

## Research Findings

### Where can this data be obtained?
-   **UNESCO World Heritage List**: [UNESCO Data Portal](https://whc.unesco.org/en/list/xml) (Bulk XML/CSV).
-   **Wikidata**: [Wikidata Query Service](https://query.wikidata.org/) for items with the "listed building" or "heritage status" property (P1435).
-   **OpenStreetMap (OSM)**: Data extraction via [Overpass Turbo](https://overpass-turbo.eu/) for tags like `heritage=*`.
-   **National Heritage Lists**:
    -   **United Kingdom**: [Historic England NHLE](https://historicengland.org.uk/listing/the-list/data-downloads/).
    -   **United States**: [National Register of Historic Places (NPS)](https://www.nps.gov/subjects/nationalregister/database-research.htm).
    -   **France**: [Base Mérimée](https://www.data.gouv.fr/fr/datasets/liste-des-immeubles-proteges-au-titre-des-monuments-historiques/).

### Format of the data
-   **JSON/GeoJSON**: Common for API responses and GIS data.
-   **CSV/TSV**: Standard for bulk tabular data.
-   **XML**: Provided by UNESCO and some legacy government systems.
-   **Shapefiles**: Available for geographic boundary data.

### Rate limits, licensing, or costs
-   **Licensing**: Government data (NPS, Historic England) is typically Open Government Licence or Public Domain. OSM is ODbL. Wikidata is CC0.
-   **Rate Limits**: Overpass API and Wikidata Query Service have strict rate limits for high-volume requests.
-   **Costs**: Generally free for public data.

### Approximate Size
-   **UNESCO**: < 10 MB.
-   **National Databases**: 100 MB - 1 GB depending on metadata.
-   **Global Aggregated (OSM/Wikidata)**: 2 GB - 10 GB when including full descriptions and spatial data.

### Estimated Scraper Effort
-   **Low to Medium**:
    -   Bulk downloads from UNESCO and national registries are straightforward to parse.
    -   Wikidata SPARQL queries are efficient for gathering global identifiers.
    -   Normalization across different national schemas is the most significant effort.
