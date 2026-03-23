---
title: "Radio Frequency Spectrum Allocations (ITU)"
date: 2026-03-08
category: "Technology & Infrastructure"
tags: ["radio", "spectrum", "telecommunications", "itu", "frequency"]
---

# Knowledge Graph Research: Radio Frequency Spectrum Allocations

**Date:** 2026-03-08
**Topic:** Radio Frequency Spectrum Allocations (Global & National)
**Researcher:** Gemini CLI

---

## 1. Brainstormed Ideas
Below are 3-5 novel dataset types evaluated for inclusion in the local knowledge graph:

1.  **Global Biological Soil Crust Database (Biocrust)**: Deep ecological data on arid land crusts which are vital for carbon/nitrogen cycles. Sources: USGS, regional biological surveys.
2.  **Radio Frequency Spectrum Allocations (FCC/Ofcom/ITU)**: Technical and geographic data on how the electromagnetic spectrum is licensed and used globally. (Selected for this research).
3.  **Ancient Near East Archaeological Sites (CDLI/Pleiades)**: Precise coordinates and metadata for thousands of archaeological sites in the Fertile Crescent. Sources: Cuneiform Digital Library Initiative, Pleiades Gazeteer.
4.  **Global Port and Terminal Operations (WFP/IMO)**: Data on maritime logistics, including berth depths, crane capacities, and historical traffic. Sources: WFP Geonode, IMO GISIS.
5.  **National Inventory of Dams (US/Global)**: Structural and risk-related data for thousands of dams. Sources: US Army Corps of Engineers (NID), Global Reservoir and Dam Database (GRanD).

---

## 2. Selected Idea: Radio Frequency Spectrum Allocations
This dataset provides a comprehensive map of the "invisible infrastructure" of the modern world. It is highly structured, factual, and geographically grounded.

### Where can this data be obtained?
- **USA (FCC ULS):** The Federal Communications Commission provides full database dumps of the Universal Licensing System via FTP: `ftp://wireless.fcc.gov/pub/uls/complete/`.
- **UK (Ofcom WTR):** Ofcom provides the Wireless Telegraphy Register as a direct CSV download: `https://static.ofcom.org.uk/static/radiolicensing/html/register/WTR.csv`.
- **European/ITU Region 1 (EFIS):** The ECO Frequency Information System (EFIS) provides a portal to export European spectrum allocations to CSV or XML: `https://www.efis.dk/`.
- **Global (ITU Article 5):** The International Table of Frequency Allocations is officially available via the ITU RR5FATViewer software (paid), but the FCC maintains a version for all three ITU regions in their Online Table: `https://www.fcc.gov/oet/spectrum/table/fcctable.pdf`.

### What is the format of the data?
- **FCC:** Complex pipe-delimited `.dat` files bundled in `.zip` archives. Each service (Amateur, Cellular, etc.) has its own file.
- **Ofcom:** Single large CSV file containing all licenses.
- **EFIS/ITU:** CSV, XML, or Relational Database (MDB/SQLITE) formats depending on the export tool used.

### Rate limits, licensing, and costs?
- **FCC/Ofcom:** Open data, no cost, and generally no strict rate limits for bulk downloads via FTP/HTTPS.
- **ITU:** Official machine-readable databases are typically paid products (approx. 300-500 CHF). However, regional proxies like EFIS or the FCC's international table extracts are free to use.
- **Licensing:** Most national data follows the respective country's open government license (e.g., US Public Domain or UK OGL).

### Approximate size of the dataset?
- **FCC ULS:** Total size is roughly 10-20 GB when uncompressed. Individual service files (like Amateur Radio) are ~500 MB to 1 GB.
- **Ofcom WTR:** ~100-200 MB CSV.
- **Global Allocation Tables:** Generally small (under 50 MB) as they represent rules rather than individual licenses.

### Estimated effort to write a scraper or download script?
- **Effort: Medium.**
- **Details:** 
    - A script to download the files is trivial (`wget` or `curl`). 
    - The complexity lies in **parsing**. The FCC ULS uses a relational schema where one license might span multiple `.dat` files (e.g., `EN.dat` for names, `LO.dat` for locations, `FR.dat` for frequencies).
    - Mapping these to a Knowledge Graph (RDF or Property Graph) would require a custom ETL pipeline to join these tables on unique identifiers like `unique_system_identifier`.

---

## 3. Implementation Strategy
To integrate this into the local knowledge graph:
1.  **Phase 1:** Download the FCC "Service Definitions" and the `l_amat.zip` (Amateur Radio) as a pilot.
2.  **Phase 2:** Parse the pipe-delimited files into a staging SQLite database.
3.  **Phase 3:** Extract triples/nodes representing `Entity -> License -> Frequency -> Location`.
4.  **Phase 4:** Link to geographic entities (City/State) already in the knowledge graph.
