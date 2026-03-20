# 2026-03-15 IAEA PRIS (Power Reactor Information System) Research

## 1. Brainstormed Dataset Ideas
1.  **Global Nuclear Reactor Operational History (IAEA PRIS)**: Detailed lifecycle data, performance metrics, and technical specifications for every nuclear power reactor globally. (Selected)
2.  **Global Botanical Garden Collections (BGCI PlantSearch)**: A comprehensive database of plant species maintained in botanical gardens and arboreta worldwide.
3.  **Global Archaeological Radiocarbon Dating Databases (e.g., CARD)**: Aggregated radiocarbon (C14) dating results from archaeological sites.
4.  **International Tree-Ring Data Bank (ITRDB)**: High-resolution paleoclimate and dating data derived from tree-ring samples globally.
5.  **Global Antarctic Research Stations and Logistics (COMNAP)**: Data on the locations, capacities, populations, and research focuses of all Antarctic stations.

---

## 2. Selected Dataset: Global Nuclear Reactor Operational History (IAEA PRIS)

### Description
The Power Reactor Information System (PRIS), maintained by the International Atomic Energy Agency (IAEA), is the most comprehensive global database on nuclear power reactors. It contains detailed data on nuclear power plants worldwide, including their status, technical specifications, and performance history since 1970.

### Research Findings

#### Where can this data be obtained?
- **Public Portal**: [https://pris.iaea.org/PRIS/Home.aspx](https://pris.iaea.org/PRIS/Home.aspx)
- **Open Data Platform**: [https://data.iaea.org](https://data.iaea.org)
- **API Access**: The IAEA Data Platform utilizes the **CKAN API**.
  - Base API URL: `https://data.iaea.org/api/3/action/`
  - Key Actions: `package_search?q=PRIS`, `package_show?id={id}`, `datastore_search?resource_id={id}`

#### What is the format of the data?
- **API Formats**: JSON, XML.
- **Bulk Download Formats**: CSV, XLS (Excel), and PDF reports.
- **Interactive Reports**: The "PRIS Analytics" tool provides customizable data visualizations.

#### Are there any rate limits, licensing restrictions, or costs?
- **Cost**: The data is provided **free of charge**.
- **Licensing**: Governed by the **IAEA Terms of Use**.
  - **Attribution**: Users must give appropriate acknowledgement of the IAEA as the source.
  - **Reproduction**: Data can be used, reproduced, and disseminated for research and commercial products, provided it doesn't imply IAEA endorsement.
- **Restrictions**: Some "Registered Access" (NUCLEUS account required) data for specific performance categories (PRISTA) may have more restrictive internal-use-only terms. However, general reactor specifications and operational status are open.

#### How large is the dataset approximately?
- The dataset covers approximately **440 operational reactors**, **60 under construction**, and **200+ permanently shut down** reactors.
- Including historical monthly and annual performance data, the total structured data size is estimated to be between **100 MB and 500 MB** (CSV/JSON).

#### Estimated Effort to Write a Scraper/Download Script
- **Effort: Low to Medium.**
- Since the data is hosted on a CKAN-based platform, a Python script using the `requests` library can easily fetch the metadata and resource files.
- Parsing the detailed technical specifications might require some logic to map different reactor types (PWR, BWR, PHWR, etc.), but the structure is very consistent.

---

## 3. Potential for Knowledge Graph
This dataset is highly valuable for a local knowledge graph because it provides:
- **Spatio-temporal data**: Coordinates of plants and historical operational timelines.
- **Technical Relationships**: Connections between reactor types, cooling systems, and manufacturers (Westinghouse, Rosatom, Framatome, etc.).
- **Economic/Energy Context**: Electricity generation figures that can be linked to global energy trends.
