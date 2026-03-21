# Research Report: Meteorite Landings Database (Meteoritical Bulletin)

## 1. Brainstormed Ideas
1. **Global Seamount and Guyot Database**: A dataset containing undersea mountains, their coordinates, depth, and geological composition.
2. **Meteorite Landings Database (Meteoritical Bulletin Database)**: Locations, masses, discovery years, and classifications of known meteorite falls and finds globally.
3. **Lepidoptera Host Plant Database**: Specific ecological relationships mapping butterfly and moth species to their specific host plants worldwide.

## 2. Selected Idea
**Meteorite Landings Database (Meteoritical Bulletin Database)**
This dataset is chosen because it represents highly structured, globally distributed, and scientifically significant physical events (meteorite impacts and finds). The data provides a rich set of temporal, spatial, and compositional facts, making it an excellent addition to a local knowledge graph.

## 3. Research Findings

### Where can this data be obtained?
The primary authoritative source is the Meteoritical Society, but direct bulk access is best obtained through mirrored open data portals:
*   **NASA Open Data Portal**: Provides a clean dataset derived from the Meteoritical Society's records. It is available via the Meteorite Landings API (powered by Socrata) and direct download links.
*   **Natural History Museum (NHM) Data Portal**: Provides a digital version of the Catalogue of Meteorites.
*   **Data.gov**: Mirrors the NASA dataset.

### What is the format of the data?
The data is readily available in **CSV, JSON, XML, and RDF** formats.

### Are there any rate limits, licensing restrictions, or costs associated with scraping/downloading it?
*   **Licensing**: The data is provided as Open Data under U.S. Government works and public domain licenses.
*   **Costs**: Free of charge.
*   **Rate Limits**: Direct bulk downloads (CSV/JSON) do not face rate limits. Programmatic access via the Socrata API may have standard request throttling (e.g., limits per hour for unauthenticated users), but authentication with an app token can increase these limits. No complex scraping is required.

### How large is the dataset approximately?
The dataset contains over 45,000 to 70,000+ individual meteorite records. As structured text (CSV or JSON), the entire dataset is extremely lightweight, estimated to be between **10 MB and 20 MB**. It is highly efficient for local storage and ingestion.

### What would be the estimated effort to write a scraper or download script for this data?
**Very Low Effort.** 
Since the data is officially packaged as a bulk downloadable CSV or JSON file via REST APIs, there is no need for HTML parsing, handling pagination on web pages, or bypassing bot protections. A simple Python script using the `requests` library to fetch the Socrata dataset URL and save the response to disk would take just a few minutes to write.
