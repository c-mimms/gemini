---
title: "Global Aircraft Registration & Fleet Data"
date: 2026-03-13
category: "Technology & Infrastructure"
tags: ["aviation", "aircraft", "fleet", "registration", "transport"]
---

# Research Report: Global Aircraft Registration and Fleet Data

**Date:** 2026-03-13
**Researcher:** Gemini CLI
**Topic:** Global Aircraft Registration and Fleet Data

---

## 1. Brainstorming: Novel Dataset Ideas

The following dataset types were brainstormed for potential inclusion in the local knowledge graph:

1.  **Global Aircraft Registration and Fleet Data**: Comprehensive tracking of individual aircraft, including manufacturer details, model, ownership history, and registration status across different national registries (e.g., FAA, CAA).
2.  **Traditional Ethnobotanical Knowledge (TEK)**: Structured data on the historical and cultural uses of plants for medicinal, ritual, and dietary purposes, connecting botanical species to human culture.
3.  **Global Standard Time and Frequency Services**: A technical dataset covering the history of time zones, leap seconds, atomic clock locations, and the evolution of international time standards.
4.  **Historical Cartographic Metadata**: A database of historical maps, including metadata on engravers, publication dates, geographic coverage, and map projections used throughout history.
5.  **Global Sports Statistics and Records**: Granular historical data on athletes, competitive events, and world records, focusing on multi-national events like the Olympic Games.

**Selected Idea:** Global Aircraft Registration and Fleet Data.

---

## 2. Research Findings: Global Aircraft Registration and Fleet Data

### Overview
Aircraft registration data provides a unique identifier (tail number/registration) for every civil aircraft, linked to its manufacturer, serial number, model, owner, and engine type. This data is critical for mapping the global aviation ecosystem.

### Data Sources & Availability

| Source | Geographic Scope | URL | Access Method |
| :--- | :--- | :--- | :--- |
| **FAA (United States)** | USA | [FAA Releasable Database](https://www.faa.gov/licenses_certificates/aircraft_certification/aircraft_registry/releasable_aircraft_download) | Bulk ZIP (CSV/TXT) |
| **UK CAA (United Kingdom)** | UK | [G-INFO Database](https://www.caa.co.uk/aircraft-register/g-info/g-info-data-downloads/) | Bulk CSV/Excel |
| **Transport Canada** | Canada | [CCARCS Download](https://wwwapps.tc.gc.ca/Saf-Sec-Sur/2/CCARCS-RIACC/ddl.aspx) | Bulk CSV |
| **CASA (Australia)** | Australia | [Australian Aircraft Register](https://www.casa.gov.au/search-centre/aircraft-register) | Bulk CSV/CSV |
| **OpenSky Network** | Global (Aggregated) | [OpenSky Metadata](https://opensky-network.org/datasets/metadata/) | Bulk CSV |
| **ICAO** | Global (Types/Codes) | [ICAO API Data Service](https://www.icao.int/safety/iapi/Pages/default.aspx) | API (REST) |

### Data Format
- **Bulk Downloads:** Primarily Comma-Delimited TXT or CSV files inside ZIP archives.
- **API Access:** JSON (OpenSky, AirLabs, Aviation Edge).
- **Structure:** Tables usually include `Master` (Aircraft/Owner), `Engine`, `Reference` (Make/Model codes), and `Deregistered`.

### Licensing, Rate Limits, and Costs
- **Government Data (FAA, CAA, TC):** Generally public domain or released under open government licenses. Free of charge for bulk download.
- **OpenSky Network:** Free for non-commercial research purposes. Large CSVs are available without strict rate limits for bulk use.
- **Commercial APIs (AirLabs, Aviation Edge):** Freemium models. Free tiers typically limit the number of calls (e.g., 1,000/month) or the depth of data.

### Dataset Size
- **FAA Registry:** ~60MB zipped, expanding to ~250MB of raw text.
- **OpenSky Aggregated Database:** ~100MB - 300MB CSV.
- **Total Estimated Storage:** A normalized global database of civil aircraft would likely occupy **1GB - 5GB** in a local relational or graph database, depending on the level of historical detail (e.g., past owners).

### Estimated Effort for Scraper/Integration
- **Complexity:** Moderate.
- **Reasoning:** While downloading the files is trivial, each national registry uses different schemas, codes for manufacturers/models, and date formats. Normalizing this into a single "Aircraft" entity for a knowledge graph requires mapping these disparate schemas.
- **Implementation Time:** 2-3 days for a robust ingestion pipeline that handles the top 5 registries (USA, UK, Canada, Australia, and OpenSky).

---

## 3. Conclusion & Next Steps
The **Global Aircraft Registration and Fleet Data** is an excellent candidate for the knowledge graph. It provides a factual, stable backbone that can be linked to other datasets like "Airport Locations," "Flight Routes," and "Manufacturing History."

**Next Recommended Step:** Implement a parser for the FAA Releasable Database as a "base" layer, then layer in OpenSky metadata to fill in global gaps.
