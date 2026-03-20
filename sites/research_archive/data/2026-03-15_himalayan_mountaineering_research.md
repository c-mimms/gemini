# Research Report: Himalayan Mountaineering Expeditions (The Himalayan Database)

**Date**: 2026-03-15  
**Topic**: Himalayan Mountaineering Expeditions  
**Researcher**: Gemini CLI  

---

## 1. Brainstormed Ideas
Below are 5 novel dataset types researched and evaluated for their potential inclusion in a local knowledge graph:

1.  **Himalayan Mountaineering Expeditions (The Himalayan Database)**: A comprehensive record of all expeditions to the Nepal Himalaya since 1905. Extremely factual and deeply structured.
2.  **Historical Encrypted Manuscripts (The DECODE Database)**: A collection of thousands of historical ciphers, keys, and transcriptions. Excellent for linguistic and cryptographic knowledge.
3.  **Global Wind Turbine Locations (USWTDB & Global)**: Spatial datasets containing precise coordinates, turbine models, and capacities for wind energy infrastructure.
4.  **Maritime Lighthouse Heritage (World List of Lights)**: Technical and historical data on lighthouses worldwide, including focal plane height, light patterns, and construction dates.
5.  **Digital Bibliography & Library Project (DBLP)**: A massive, high-quality bibliography of computer science publications, including authors, affiliations, and citation networks.

**Selected Idea**: **Himalayan Mountaineering Expeditions (The Himalayan Database)**

---

## 2. Research Findings: The Himalayan Database

### Overview
The Himalayan Database is a digital record of all expeditions that have climbed in the Nepal Himalaya. The database is based on the expedition archives of Elizabeth Hawley, a journalist who spent decades interviewing teams in Kathmandu. It covers peaks, expeditions, members, and references for over a century of climbing history.

### Data Source
- **Official Website**: [himalayandatabase.com](https://www.himalayandatabase.com)
- **Download URL**: [himalayandatabase.com/downloads.html](https://www.himalayandatabase.com/downloads.html)
- **API**: No official REST API exists. Community-maintained Python wrappers (e.g., `himalayandatabase-python`) exist on GitHub to parse the raw files.

### Data Format
- **Native Format**: Microsoft Visual FoxPro 9 (.DBF files).
- **Structure**: The data is partitioned into several core tables:
    - `PEAKS`: Metadata for ~480 peaks (height, location, climbing status).
    - `EXPED`: Details for ~11,000+ expeditions (dates, routes, success/failure, oxygen use).
    - `MEMBERS`: Biographical and event data for ~85,000+ climbers and high-altitude workers.
    - `REFER`: Literature and media references for the expeditions.
- **Alternative Formats**: CSV versions are occasionally hosted on platforms like Kaggle or Maven Analytics, but the DBF files are the authoritative source.

### Licensing & Restrictions
- **License**: Limited, non-exclusive, non-transferable, and perpetual license.
- **Cost**: Free for personal and research use.
- **Restrictions**: Redistribution of the raw database files or their contents to third parties is prohibited. Users may make one backup copy. Commercial use requires explicit permission.

### Dataset Size
- **Download**: ~43.1 MB (ZIP archive).
- **Extracted**: Approximately 100-150 MB when converted to a modern format like SQLite.
- **Scale**: Small enough for local storage on any device, but dense enough to provide high relational value for a knowledge graph.

### Estimated Effort to Scrape/Download
- **Download**: Trivial (Single ZIP download).
- **Ingestion/Conversion**: Moderate. Converting legacy Visual FoxPro (.DBF) files requires specific libraries (e.g., `dbfread` in Python). Mapping the relational structure into a knowledge graph (e.g., connecting `MEMBERS` to `EXPED` via team IDs) is straightforward due to the clean schema.
- **Total Effort**: ~2-4 hours to build a fully automated pipeline from raw ZIP to a local Graph/Relational database.

---

## 3. Evaluation for Knowledge Graph
This dataset is a "gold mine" for a local knowledge graph. It provides:
- **Unique Identifiers**: Peaks and members have stable IDs.
- **Factual Ground Truth**: Verified records of first ascents, deaths, and routes.
- **Relational Depth**: Rich connections between people, geography (peaks), time, and outcomes.
- **Local Portability**: The small footprint makes it an ideal candidate for offline query engines.
