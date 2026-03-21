# Research Report: Global Amateur Radio (Ham Radio) Infrastructure

**Date:** 2026-03-21
**Topic:** Global Amateur Radio Infrastructure (Repeaters, Beacons, and Licensees)
**Researcher:** Gemini CLI

## 1. Brainstorming: Novel Dataset Ideas
The following dataset types were brainstormed as potential additions to the local knowledge graph:

1.  **Global Renewable Energy Potential**: High-resolution GIS datasets for solar irradiance, wind speed, and geothermal potential (e.g., Global Solar Atlas, Global Wind Atlas).
2.  **Global Amateur Radio (Ham Radio) Infrastructure**: Databases of repeaters, beacons, and licensed operators (callsigns) worldwide. (**Selected**)
3.  **Global Library Holdings & Metadata**: Bibliographic records of physical and digital items held by libraries worldwide, beyond the scope of Open Library (e.g., OCLC WorldCat-style open data).
4.  **Global Trademarks & Intellectual Property**: Databases of registered trademarks, logos, and brand ownership (beyond patent data).
5.  **Global Botanical Garden Collections & Herbarium Records**: Structured data on plant specimens held in botanical gardens and herbaria (e.g., BGCI's PlantSearch).

---

## 2. Selected Idea: Global Amateur Radio Infrastructure
Amateur radio (Ham radio) represents a vast, decentralized global communication network. This research focuses on two primary data types: **Licensees (Operators)** and **Infrastructure (Repeaters and Beacons)**.

### Where can this data be obtained?

#### Licensee / Operator Databases (Official Regulatory Data)
*   **United States (FCC ULS):** The Federal Communications Commission provides weekly bulk downloads of the Universal Licensing System (ULS) database.
    *   **URL:** [FCC ULS Database Downloads](https://www.fcc.gov/wireless/data/uls-database-downloads)
    *   **Direct FTP:** `ftp://wirelessftp.fcc.gov/pub/uls/complete/l_amat.zip`
*   **Canada (ISED):** Innovation, Science and Economic Development Canada provides daily updates.
    *   **URL:** [ISED Amateur Radio Downloads](https://sms-sgs.ic.gc.ca/amateur/download/index)
*   **Australia (ACMA):** The Australian Communications and Media Authority provides bulk CSV data and a Web API.
    *   **URL:** [ACMA Radiocomms Licence Data](https://www.acma.gov.au/radiocomms-licence-data)
*   **United Kingdom (Ofcom):** Periodic Freedom of Information (FoI) snapshots (e.g., March 2025 release).
    *   **URL:** [Ofcom FoI Responses](https://www.ofcom.org.uk/about-ofcom/foi-responses)

#### Infrastructure Databases (Repeaters and Beacons)
*   **Amateur Repeater Directory (ARD):** A community-maintained, open-source alternative to proprietary lists.
    *   **URL:** [GitHub - ARD-RepeaterList](https://github.com/Amateur-Repeater-Directory/ARD-RepeaterList)
*   **RadioID.net:** Primary source for digital radio (DMR/NXDN) repeaters.
    *   **URL:** [RadioID.net Database Dumps](https://www.radioid.net/static/rptrs.json)
*   **HearHam.live:** Provides a free JSON API for global repeaters.
    *   **URL:** [HearHam.live API](https://hearham.live/)
*   **IZ8WNH.it:** Global interactive map with CSV export functionality.
    *   **URL:** [IZ8WNH.it Map](https://www.iz8wnh.it/map/)

### What is the format of the data?
*   **FCC (US):** Pipe-delimited (`|`) text files (`.dat`) inside ZIP archives.
*   **Canada/Australia:** CSV or delimited text files inside ZIP archives.
*   **Infrastructure (ARD/RadioID/HearHam):** JSON and CSV.
*   **UK:** XLSX or CSV.

### Licensing, Rate Limits, and Costs
*   **Costs:** All listed sources are **free of charge**.
*   **Licensing:** Regulatory data (FCC, ISED, ACMA) is public domain or under government open licenses. Community data (ARD) is typically Creative Commons.
*   **Restrictions:** Proprietary databases like **RepeaterBook** and **QRZ.com** strictly forbid bulk scraping or republication and should be avoided for local knowledge graph ingestion unless using their specific (often paid) APIs.
*   **Rate Limits:** Bulk download links have no significant rate limits. APIs (RadioID, HearHam) may have standard limits, but bulk JSON dumps are preferred for local storage.

### Estimated Size
*   **FCC ULS (Amateur):** ~500 MB (zipped), >2 GB (unzipped).
*   **Canada/Australia Licensees:** <100 MB each.
*   **Global Repeater Databases:** <50 MB for JSON/CSV dumps.
*   **Total Estimate:** Approximately 3-5 GB for a comprehensive global dataset.

### Estimated Effort for Scraping/Ingestion
*   **Level: Moderate**
*   **Tasks:**
    1.  **Download Automation:** Simple `wget` or `curl` scripts for bulk ZIP files.
    2.  **Parsing:** Writing parsers for the FCC's pipe-delimited `.dat` format (specifically the `EN.dat`, `HD.dat`, and `AM.dat` files).
    3.  **Normalization:** Mapping different country formats (FCC vs. ISED vs. ACMA) into a unified schema for the knowledge graph.
    4.  **Geocoding:** Converting provided addresses or Maidenhead grid squares into Lat/Lon for GIS visualization.

---

## 3. Conclusion
The Global Amateur Radio Infrastructure dataset is a high-value target for a knowledge graph. It provides a structured, factual map of global communication capabilities and a verified list of operators. The data is largely available in bulk formats, making it ideal for local storage without the need for complex scraping of HTML pages.
