# Knowledge Graph Data Research: Maritime Shipwreck Databases

## Date: 2026-03-07
## Topic: Maritime Shipwreck Databases

---

## 1. Brainstormed Ideas
- **Global Historical Conflict/Battle Database**: Structured data on historical battles, wars, casualties, and participants (e.g., Conflict Data Program).
- **Maritime Shipwreck Database**: GIS data on known shipwrecks, their history, and locations. (SELECTED)
- **Global Genetic/Genomic Variation (Human or Crop)**: Structured data on genetic markers and their geographical distribution.
- **World Register of Marine Species (WoRMS)**: Comprehensive taxonomy and ecological data for marine life.
- **Global Patent Database (Bulk Data)**: USPTO or WIPO patent data for technological evolution mapping.

---

## 2. Selected Idea: Maritime Shipwreck Database
The research focused on locating open-access, structured maritime shipwreck data with global or regional coverage.

### Findings

#### Where can this data be obtained?
1.  **UKHO ADMIRALTY Marine Data Portal (Global)**:
    - Provides a dataset of over 94,000 wrecks and obstructions worldwide.
    - [Portal Link](https://data.admiralty.co.uk/portal/apps/sites/#/marine-data-portal/pages/wrecks-and-obstructions)
2.  **NOAA Wrecks and Obstructions (USA)**:
    - Focuses on U.S. maritime boundaries using the AWOIS (Automated Wreck and Obstruction Information System).
    - [ArcGIS Hub Link](https://hub.arcgis.com/datasets/noaa::wrecks-and-obstructions-in-awois/about)
3.  **EMODnet Human Activities (Europe)**:
    - Aggregates data from European national authorities.
    - [EMODnet Portal](https://emodnet.ec.europa.eu/en/human-activities)
4.  **OXREP Ancient Shipwrecks Database (Mediterranean)**:
    - Focuses on ancient wrecks up to AD 1500.
    - [OXREP Link](https://oxrep.classics.ox.ac.uk/databases/shipwrecks_database/)

#### Data Format
- **UKHO**: Shapefile, GeoJSON, KML, and CSV.
- **NOAA**: CSV, JSON, Shapefile, KML.
- **EMODnet**: CSV, Shapefile, GeoJSON, GML.
- **OXREP**: Searchable table (may require HTML scraping or table export tools).

#### Licensing and Restrictions
- **UKHO/EMODnet**: Open Government Licence (OGL) – Free for commercial and non-commercial use with attribution.
- **NOAA**: Public domain (U.S. Government data).
- **Cost**: Generally free for these open-data portals. Private databases like Wrecksite.eu require paid subscriptions for bulk access.

#### Approximate Size
- The UKHO global dataset contains ~94,000 records. A CSV version of this data is estimated to be between **20 MB and 50 MB**.
- Combined global datasets from multiple sources would likely remain under **500 MB** for structured text/GIS data (excluding high-resolution sonar imagery).

#### Estimated Effort
- **Effort Level**: Low to Medium.
- Most sources provide direct bulk download links for CSV or GeoJSON files.
- A Python script using `requests` to fetch the files and `pandas` or `geopandas` to normalize the data would take approximately **2-4 hours** to implement.
- Normalizing the different schemas (e.g., column names for depth, date sunk, vessel type) would be the primary task.

---

## 3. Conclusion
The Maritime Shipwreck Database is a highly viable source for the knowledge graph. It provides concrete factual data (name, date, location, depth) that can be easily integrated into a local GIS-capable database. The UKHO dataset is the strongest starting point for global coverage.
