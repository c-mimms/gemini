# Research Report: Global Tsunami Event and Runup Database

**Date:** 2026-03-24
**Topic:** Global Tsunami Event and Runup Database (NOAA NCEI)

## 1. Brainstormed Ideas
- **Global Tsunami Event and Runup Database**: Historical records of tsunami events and observation data (NOAA NCEI).
- **Global Chemical Weapons Conventions and Disarmament Data**: Data on stockpiles, destruction facilities, and inspections (OPCW data).
- **Global Active Fault Lines & Tectonic Plate Boundaries**: Detailed geophysical data on the structures that shape the Earth (GEM Global Active Faults).
- **Global Flight Tracking Infrastructure (ADSB)**: Metadata on the network of receivers and historical aircraft movement data (OpenSky Network).
- **Global Protected Species Trade Data (CITES)**: Records of international trade in endangered species.

**Selected Idea**: **Global Tsunami Event and Runup Database**. This dataset is critical for understanding seismic hazards, coastal vulnerability, and historical oceanographic events.

## 2. Research Findings

### Where can this data be obtained?
- **NOAA NCEI (National Centers for Environmental Information)**: The primary repository for historical tsunami data.
- **API Access**: The [NCEI Hazard API](https://www.ngdc.noaa.gov/hazel/hazards-service/api/v1/) provides programmatic access to events and runups.
- **Bulk Download**: Available via the [NCEI Tsunami Event Search](https://www.ngdc.noaa.gov/hazel/view/hazards/tsunami/event-search) portal.

### What is the format of the data?
- **API**: JSON is the default response format.
- **Bulk Download**: CSV, TSV, and XLS (Excel) formats are available through the search interface.

### Are there any rate limits, licensing restrictions, or costs?
- **Licensing**: Public domain (U.S. Federal Government data). Free to use, redistribute, and modify.
- **Costs**: None.
- **Limits**: Standard NOAA API rate limits apply, but the dataset size is small enough that a few requests can capture the entire history.

### How large is the dataset approximately?
- **Tsunami Events**: ~2,400 source events.
- **Tsunami Runups**: ~27,000 observation records.
- **Estimated Size**: Less than 10 MB for the entire uncompressed CSV dataset.

### What is the estimated effort to write a scraper or download script?
- **Effort: Low**. The NCEI Hazard API is well-documented (Swagger/OpenAPI). A Python script using the `requests` library could download both the events and runups in under an hour. The data is already highly structured, requiring minimal cleaning.
