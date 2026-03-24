# Research Report: Global Maritime Ports & Shipping Terminals

**Date:** 2026-03-23
**Topic:** Global Maritime Ports & Shipping Terminals (NGA World Port Index & UN/LOCODE)

## 1. Brainstormed Ideas
- **Global Maritime Ports & Shipping Terminals**: Comprehensive data on port locations, capabilities, and infrastructure (UN/LOCODE and NGA World Port Index).
- **Global Active Fault Lines & Tectonic Plate Boundaries**: Detailed geophysical data on the structures that shape the Earth (GEM Global Active Faults).
- **Global Flight Tracking Infrastructure (ADSB)**: Metadata on the network of receivers and historical aircraft movement data (OpenSky Network).
- **Global High-Voltage Power Substations**: Precise locations and technical specifications of the nodes in the global energy grid.
- **Global Trademark & Brand Registry**: Structured data on commercial identifiers and intellectual property (WIPO Global Brand Database).

**Selected Idea**: **Global Maritime Ports & Shipping Terminals**. This dataset is foundational for understanding global trade, logistics, and maritime geography.

## 2. Research Findings

### Where can this data be obtained?
- **NGA World Port Index (WPI)**: Maintained by the National Geospatial-Intelligence Agency (NGA). Bulk downloads and an API are available via the [NGA Maritime Safety Information (MSI) portal](https://msi.nga.mil/Publications/WPI).
- **UN/LOCODE**: Maintained by UNECE. Identifies over 103,000 locations globally. Available at the [UNECE website](https://unece.org/trade/cefact/unlocode-code-list-country-and-territory).

### What is the format of the data?
- **NGA WPI**: CSV, JSON, XML, Shapefile (SHP), File Geodatabase (GDB), and PDF.
- **UN/LOCODE**: MS Access (.mdb), CSV, TXT, and HTML.

### Are there any rate limits, licensing restrictions, or costs?
- **NGA WPI**: Public domain (U.S. Government). Free to download and use without restrictions.
- **UN/LOCODE**: Publicly available data provided by the United Nations for trade and transport. No cost associated with standard access.

### How large is the dataset approximately?
- **NGA WPI**: Small but dense; ~3,700 entries with extensive technical fields. Bulk size is ~1–5 MB.
- **UN/LOCODE**: Moderate; ~103,000 records. Bulk size is ~20–50 MB.

### What is the estimated effort to write a scraper or download script?
- **Effort: Low**. Both sources provide well-structured CSV files for bulk download. A Python script using `requests` for downloading and `pandas` for processing could ingest both datasets in a few hours of development time.
