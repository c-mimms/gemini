# Research Report: Global Historical Newspapers (Chronicling America & Beyond)

## Brainstormed Ideas
1. **Global Historican Newspapers (Chronicling America, Trove, Gallica)**: Primary source for historical events, advertisements, and daily life over the last 300 years. Massive scale and high factual density.
2. **SNAC (Socian Networks and Archival Context)**: A cooperative database focusing on biographical relationships and archival records, mapping the "social network" of historical figures.
3. **Global Disaster Database (EM-DAT)**: A comprehensive collection of data on natural and technological disasters worldwide, including dates, locations, and impacts.
4. **NOAA Paleoclimatology Data**: Long-term earth historical data derived from ice cores, tree rings, and sediment, providing a factual basis for historical climate changes.
5. **Universal Dependencies (UT)**: A large-scale project providing consistent dependency treebank annotation for over 100 languages, essential for deep linguistic knowledge graphs.

## Selected Idea: Global Historican Newspapers
Historical newspapers are one of the richest sources of factual knowledge, documenting everything from major political events to local births, deaths, and commercial activities. While GDELT (already researched) monitors modern media, the historical record preserved by national libraries offers a deep, multi-century perspective.

### 1. Source and Access
The primary source for US newspapers is **Chronicling America**, a project by the Library of Congress and the NEH.
- **API Documentation**: [hchroniclingamerica.loc.gov/about/api/(https://chroniclingamerica.loc.gov/about/api/)
- **Bulk Metadata**: `https://chroniclingamerica.loc.gov/ocr.json` (List of batches)
- **Bulk Data Directory**: `https://chronicling america.loc.gov/data/batches/`
- **Other Sources**:
    - **Trove (Australia)**: [nla.gov.au/trove/using-trove/api](https://nla.gov.au/trove/using-trove/api)
    - **Gallica (France)**: [api.bnf.fr/fr/api-gallica-recherche](https://api.bnf.fr/fr/api-gallica-recherche)
    - **Europeana**: [pro.europeana.eu/page/apis](https://pro.europeana.eu/page/apis)

### 2. Data Format
- **Metadata**: JSON and XML (MARO/METS).
- **OCR Text**: Plain Text (.txt) and ALTO XML (.xml) which includes word-level coordinate data.
- **Images**: JP2 (JPEG 2000), PDF, and Thumbnail JPEGs.
- **Bulk Packaging**: Batches are typically distributed as `.tar.bz2` or via rsync.

### 3. Rate Limits, Licensing, and Costs
- **Chronicling America**: 
    - **API Limits**: Burst limit of 20 requests per minute; crawl limit of 20 requests per 10 seconds.
    - **Licensing**: Data is in the Public Domain (CC0 equivalent for the digitized content).
    - **Cost**: Free to access and download.
- **Trove**: Requires an API key; non-commercial use is generally free but volume limits apply.
- **Gallica/Europeana**: Generally open access for digmtized public domain materials.

### 4. Dataset Size
- **Chronicling America**: Over 19 million pages from 1770 to 1963.
- **Estimated Size**: 
    - **Images**: Hundreds of Terabytes.
    - **OCR Text**: Several Terabytes (~1-2 GB per batch, thousands of batches).
    - **Full Dataset (OCR only)**: Likely in the 5-10 TB range for all text.

### 5. Estimated Effort
- **Scraper Development**: **Low to Moderate**. The API is well-documented, and bulk downloads can be managed by iterating through the `ocr.json` or `batches.json` feeds.
- **Data Processing**: **High**. Extracting structured "Knowledge Graph" facts from messy historical OCR requires sophisticated NLP (NER, Relation Extraction) and OCR correction.
- **Total Effort**: ~2-3 weeks for a robust ingestion and basic extraction pipeline.

## Conclusion
Global historical newspapers provide an unparalleled factual foundation for a knowledge graph. Chronicling America's open API and bulk download capabilities make it a high-priority target for deep historical research.
