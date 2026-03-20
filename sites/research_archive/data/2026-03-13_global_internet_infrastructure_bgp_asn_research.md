# Research Report: Global Internet Infrastructure (BGP, ASN, and Interconnection)

**Date**: 2026-03-13
**Topic**: Global Internet Infrastructure (BGP, Autonomous Systems, and IP WHOIS)
**Researcher**: Gemini CLI

---

## 1. Brainstormed Ideas
For this research cycle, I focused on high-value, technical, and structured datasets that define the backbone of modern civilization.
1.  **Global Internet Infrastructure (BGP & Autonomous Systems)**: The structural "map" of the internet, including network interconnections and IP ownership.
2.  **Biological Pathways and Molecular Interactions (Reactome/KEGG)**: A deep graph of biological processes and protein interactions.
3.  **Global Standards and Reference Materials (NIST/ISO)**: Scientific definitions and measurement standards for physics and engineering.
4.  **International Philatelic and Postal History**: Structured data on the evolution of global postal routing and geopolitical history.
5.  **Global Dam and Reservoir Information (GRanD)**: Technical data on large-scale hydrological infrastructure.

---

## 2. Selected Idea: Global Internet Infrastructure
The selected focus is the global map of Autonomous Systems (AS) and the Border Gateway Protocol (BGP) routing tables. This data is the "topology" of the digital world, identifying who owns which parts of the internet and how they connect.

---

## 3. Detailed Research Findings

### Where can this data be obtained?
*   **BGP Routing Tables**:
    *   **Route Views Project (University of Oregon)**: Comprehensive archives of global BGP tables since 1997. URL: [http://archive.routeviews.org/](http://archive.routeviews.org/)
    *   **RIPE NCC RIS (Routing Information Service)**: Provides raw BGP data from globally distributed collectors. URL: [https://www.ripe.net/analyse/ris/ris-raw-data](https://www.ripe.net/analyse/ris/ris-raw-data)
*   **AS Relationships & Organizations**:
    *   **CAIDA (Center for Applied Internet Data Analysis)**: Provides inferred relationships (provider-customer, peer-to-peer) and maps ASNs to organizations. URL: [https://www.caida.org/catalog/datasets/as-relationships/](https://www.caida.org/catalog/datasets/as-relationships/)
*   **Peering Data**:
    *   **PeeringDB**: The industry-standard database for peering policies and data center interconnections. URL: [https://www.peeringdb.com/](https://www.peeringdb.com/)
*   **IP WHOIS**:
    *   **RIPE NCC FTP**: Provides daily database dumps (excluding personal data) for European/Middle Eastern IP space. URL: [https://ftp.ripe.net/ripe/dbase/](https://ftp.ripe.net/ripe/dbase/)

### What is the format of the data?
*   **BGP Data**: MRT (Multi-Threaded Routing Toolkit) format. This is a binary format designed for efficient storage of routing messages.
*   **PeeringDB**: JSON, SQL, and SQLite daily snapshots.
*   **CAIDA Datasets**: Plain text (tab-separated) and CSV.
*   **WHOIS**: Bulk text files or XML/JSON via specific RIR APIs.

### Rate limits, licensing, and costs?
*   **Route Views & RIPE RIS**: Entirely free and open for download. No strict rate limits, though bulk downloads should be staggered.
*   **CAIDA**: Free for research and non-commercial use with attribution. Commercial use may require a license.
*   **PeeringDB**: Open data; API is free but requires registration for high-volume access.
*   **WHOIS**: Varies by registry. RIPE NCC is the most open (public FTP). ARIN and APNIC require signed Acceptable Use Policies (AUP) for bulk access to prevent spam.

### How large is the dataset?
*   **BGP RIB Snapshots**: ~100MB to 500MB per collector per snapshot (compressed). A full global view from 10 collectors would be ~5GB compressed.
*   **CAIDA AS-Rel**: Very small (~5MB to 20MB).
*   **PeeringDB**: ~50MB to 100MB for a full snapshot.
*   **Total Local Requirement**: A high-quality "snapshot" of the internet's structure can be stored in under **10GB**.

### Estimated effort to write a scraper/downloader?
*   **PeeringDB**: **Low**. They have a well-documented REST API and provide daily SQLite dumps.
*   **CAIDA**: **Low**. Simple file downloads via HTTP/FTP.
*   **BGP (MRT)**: **Medium**. Requires utilizing specialized libraries like `PyMRT`, `bgpstream`, or `mrtparse` to convert binary data into a knowledge-graph-friendly format (like JSON or RDF).
*   **Overall Effort**: ~2-4 days to build a robust pipeline that fetches, parses, and links these datasets.

---

## 4. Value for Knowledge Graph
Integrating this data allows the knowledge graph to answer complex queries such as:
*   "Which organizations control the primary internet gateways in Brazil?"
*   "How has the number of interconnections between US and Chinese ISPs changed over time?"
*   "Which Autonomous Systems are the most critical for global routing stability?"
*   "Map the physical data centers used by a specific tech company's network."
