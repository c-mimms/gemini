---
title: "Particle Physics Data (Particle Data Group)"
date: 2026-03-12
category: "Physics & Chemistry"
tags: ["particle-physics", "pdg", "high-energy", "cern", "subatomic"]
---

# Knowledge Graph Data Research: Particle Physics (Particle Data Group)

**Date:** 2026-03-12
**Topic:** Particle Physics Data (Standard Model)
**Researcher:** Gemini CLI Research Agent

---

## 1. Brainstorming: Novel Dataset Ideas

The following dataset types were brainstormed as potential high-value sources for the local knowledge graph:

1.  **Particle Physics Data (Particle Data Group)**: Properties of subatomic particles (mass, charge, decay modes).
2.  **Global Dam and Reservoir Information (GRanD)**: Geographic and technical data on worldwide dams.
3.  **Human Pathogen Genomic Data (NCBI)**: Genetic sequences and disease associations for pathogens.
4.  **Global Subsurface Boring/Well Logs**: Geological data from subsurface drilling.
5.  **International Postal and Address Formats**: Structured rules for global addressing systems.

**Selected Idea for Research:** Particle Physics Data (Particle Data Group)

---

## 2. Selected Idea Research: Particle Data Group (PDG)

### Description
The Particle Data Group (PDG) is an international collaboration that reviews and summarizes the properties of elementary particles and resonances. Their primary publication, the *Review of Particle Physics*, is the definitive source for particle data.

### Data Sources & Retrieval
*   **Official Website:** [pdg.lbl.gov](https://pdg.lbl.gov)
*   **API Documentation:** [pdgapi.lbl.gov/doc](https://pdgapi.lbl.gov/doc)
*   **GitHub Repository:** [github.com/particledatagroup/api](https://github.com/particledatagroup/api)
*   **Method 1 (Python API):** The `pdg` Python package allows for direct programmatic access and includes a local database.
*   **Method 2 (SQLite):** PDG provides downloadable `.sqlite` files containing the full relational database of particle properties.
*   **Method 3 (REST API):** A RESTful interface for fetching specific data points in JSON format (used by pdgLive).

### Data Format
*   **Primary:** SQLite (.sqlite) for the full local database.
*   **Secondary:** JSON via REST API.
*   **Legacy:** Machine-readable ASCII files (fixed-width formats) for masses and Monte Carlo IDs.

### Licensing, Costs & Restrictions
*   **License:** Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0).
*   **Cost:** Free for research and educational use.
*   **Restrictions:** Non-commercial use only. Derivatives are technically restricted, though internal use for a private knowledge graph is generally acceptable under research norms. Attribution is required in any published work.
*   **Rate Limits:** The REST API is rate-limited; the SQLite/Python API approach is preferred for bulk local storage.

### Estimated Dataset Size
*   **Approximate Size:** The SQLite database is relatively small (typically < 100 MB), making it ideal for local storage. The full documentation and PDF reviews are larger but not required for the raw data graph.

### Estimated Implementation Effort
*   **Effort Level:** Low to Moderate.
*   **Scraper/Download Script:** A simple script using `pip install pdg` can iterate through the database and export it to a graph-friendly format (e.g., RDF, Cypher, or a custom JSON schema). Alternatively, the SQLite file can be downloaded directly and parsed.

---

## 3. Conclusion
The PDG dataset is a "gold standard" source of factual, highly structured scientific knowledge. Its availability in SQLite format makes it an excellent candidate for immediate integration into a local knowledge graph.
