---
title: "Radioisotope & Nuclear Decay Data (NNDC)"
date: 2026-03-10
category: "Physics & Chemistry"
tags: ["nuclear-physics", "radioisotopes", "decay", "nndc", "radiation"]
---

# Research Report: Radioisotope and Nuclear Decay Data (NNDC)

## Date: 2026-03-10
## Topic: Radioisotope and Nuclear Decay Data

---

## 1. Brainstormed Ideas
Below are 3-5 novel dataset types evaluated for the local knowledge graph:
1.  **Global Biological Diversity Heritage Library (BHL)**: Full text and metadata of biodiversity literature spanning hundreds of years.
2.  **Global Historical Climatology Network - Monthly (GHCNm)**: Long-term temperature, precipitation, and pressure data (monthly aggregates).
3.  **Radioisotope and Nuclear Decay Data (NNDC)**: Factual data on isotopes, half-lives, decay modes, and cross-sections.
4.  **Global Oceanographic Observations (BODC/NOAA)**: Bathymetry, ocean temperature profiles, salinity, and current data.
5.  **Historical Stock Market Fundamentals (SEC EDGAR)**: Corporate filings and fundamental data from the last century.

**Selected Idea**: **Radioisotope and Nuclear Decay Data (NNDC)**. This dataset provides fundamental physical constants and properties for every known isotope, which is essential for a high-fidelity scientific knowledge graph.

---

## 2. Research Findings: Radioisotope and Nuclear Decay Data

### Where can this data be obtained?
The primary source for this data is the **National Nuclear Data Center (NNDC)** at Brookhaven National Laboratory and the **International Atomic Energy Agency (IAEA)**.

- **NNDC ENDF/ENSDF Downloads**: [NNDC Download Page](https://www.nndc.bnl.gov/endf/b8.0/download.html)
- **IAEA LiveChart API**: [LiveChart API Documentation](https://nds.iaea.org/relnsd/v1/data?)
    - Example: `https://nds.iaea.org/relnsd/v1/data?fields=ground_states&nuclides=all`
- **NuDat 3**: [NuDat Interactive Tool](https://www.nndc.bnl.gov/nudat3/) for filtered CSV exports.

### Data Format
- **Legacy Formats**: 
    - **ENDF-6**: A legacy fixed-width text format used for nuclear reaction data.
    - **ENSDF**: Fixed-width text format for structure and decay data.
- **Modern Formats**:
    - **CSV**: Available via the IAEA API and NuDat exports.
    - **GNDS (XML/JSON)**: The NNDC is transitioning to the Generalized Nuclear Data Structure (GNDS), which is more machine-readable.
    - **HDF5/JSON**: Available through community tools like `openmc-data-storage`.

### Licensing, Rate Limits, and Costs
- **Licensing**: NNDC data is produced by the US Government and is generally in the **public domain**. IAEA data is provided for research and peaceful purposes with no specified cost.
- **Rate Limits**: The IAEA API does not publish strict rate limits, but standard polite scraping practices (1-2 seconds between requests) are recommended.
- **Costs**: Free of charge.

### Dataset Size
- **ENDF/B-VIII.0**: Approximately **488 MB** (compressed).
- **ENSDF**: The complete database of nuclear structure and decay is estimated to be in the **low gigabytes (1-5 GB)** range when uncompressed.
- **IAEA API Extracts**: Summary CSVs for all nuclides (ground states) are relatively small (**< 10 MB**).

### Estimated Effort to Scrape/Download
- **Effort: Low to Medium**
    - **Low**: Fetching summary data (mass, half-life, decay modes) via the IAEA LiveChart API is extremely straightforward with a few Python requests.
    - **Medium**: Parsing the full ENSDF or ENDF-6 files requires handling legacy fixed-width formats. However, existing open-source libraries (e.g., `openmc`, `mcnp` tools, or specialized Python parsers) can significantly reduce this effort.

---

## 3. Conclusion
The NNDC/IAEA nuclear datasets are high-value, factual, and extremely well-structured. They are ideal for a local knowledge graph. The IAEA LiveChart API provides the fastest path to a "Nuclide Knowledge Base," while the full ENDF/ENSDF libraries provide the depth required for complex physics simulations or detailed decay chain analysis.
