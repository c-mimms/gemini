# Research Report: Global Seismicity Data (Earthquakes)

## Date: 2026-03-07
## Topic: Global Seismicity Data (Earthquakes)

---

## 1. Brainstorming: Novel Dataset Ideas
The following dataset types were considered for their potential value in a local knowledge graph:
1.  **Global Seismicity Data (Earthquakes)**: Comprehensive records of seismic events, magnitudes, locations, and depths.
2.  **Global Airport and Navigation Infrastructure**: Detailed data on airports, runways, frequencies, and navigation aids worldwide.
3.  **Historical Global Agricultural Production**: Long-term data on crop yields, livestock, and land use (e.g., FAOSTAT).
4.  **International Patent Metadata**: Information on inventions, inventors, and technology classifications to track human innovation.
5.  **UN Treaty Collection**: The full text and signatory status of international treaties and conventions.

**Selected Idea for Research**: Global Seismicity Data (Earthquakes)

---

## 2. Research Findings: USGS Earthquake Catalog

### **Where can this data be obtained?**
The primary source is the **U.S. Geological Survey (USGS) Earthquake Catalog**.
- **Search Tool**: [earthquake.usgs.gov/earthquakes/search/](https://earthquake.usgs.gov/earthquakes/search/)
- **API**: [earthquake.usgs.gov/fdsnws/event/1/](https://earthquake.usgs.gov/fdsnws/event/1/) (FDSN Web Services)
- **Bulk Downloads**: Possible via the search interface or programmatic API calls.

### **What is the format of the data?**
The catalog supports several structured formats:
- **CSV**: Best for tabular analysis and database ingestion.
- **GeoJSON**: Ideal for geographic applications and web mapping.
- **QuakeML (XML)**: A specialized standard for seismological data interchange.
- **KML**: For visualization in Google Earth.

### **Are there any rate limits, licensing restrictions, or costs?**
- **Licensing**: **Public Domain**. Most USGS data is free from copyright and can be used, modified, and distributed without permission. Attribution is requested but not legally required.
- **Costs**: Free of charge.
- **Rate Limits**: The web search interface limits results to **20,000 events** per request. For larger datasets, users must paginate by date range or magnitude threshold via the API.

### **How large is the dataset approximately?**
- **Individual Query**: A CSV file of 20,000 events is approximately **2–5 MB**.
- **Total Catalog**: The complete historical record (from 1900 to present) containing millions of events (including micro-earthquakes) would likely reach **several Gigabytes (GB)** in CSV format, though the "significant" earthquake subset is much smaller.

### **Estimated Effort to Scrape/Download**
- **Effort**: **Low**.
- **Method**: A simple Python script can utilize the USGS API to request data in yearly or monthly chunks to bypass the 20,000-event limit. The data is already well-structured (CSV or GeoJSON), requiring minimal cleaning before ingestion into a knowledge graph or database.

---

## 3. Conclusion
The USGS Earthquake Catalog is an exceptional candidate for the local knowledge graph. It provides high-resolution, factual, and spatio-temporal data that is essential for understanding planetary dynamics and historical events. Its public domain status and structured API make it one of the most accessible scientific datasets available.
