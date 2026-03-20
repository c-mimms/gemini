# Research Report: Global Music Metadata (MusicBrainz)

**Date:** 2026-03-14
**Topic:** Global Music Metadata (MusicBrainz)

## 1. Brainstormed Ideas
- **Global Music Metadata (MusicBrainz)**: A comprehensive, community-driven database of music metadata including artists, releases, recordings, labels, and works, all linked via persistent identifiers (MBIDs). (SELECTED)
- **Global Historical Natural Disasters (EM-DAT)**: A database containing data on the occurrence and effects of over 22,000 mass disasters worldwide from 1900 to the present day.
- **Global Soil Properties and Geospatial Earth Science (SoilGrids)**: High-resolution global maps of soil properties (pH, organic carbon, texture, etc.) at multiple depths, providing essential environmental context.
- **Global Intellectual Property - Trademarks (WIPO Global Brand Database)**: Records of millions of trademarks, brand names, and logos from dozens of national and international collections, complementing patent research.
- **Global Political and Election Results (ElectionGuide / OpenElections)**: Detailed historical data on national and sub-national elections worldwide, including candidate votes, turnout, and political party affiliations.

## 2. Selected Idea: Global Music Metadata (MusicBrainz)
MusicBrainz is a community-maintained open source encyclopedia of music information. For a knowledge graph, it provides a massive relational structure connecting people (artists), creative works (songs/compositions), and physical/digital products (releases/albums). Its use of MusicBrainz Identifiers (MBIDs) makes it the "de facto" linking layer for the music industry, with deep connections to Wikidata, Discogs, and Spotify.

## 3. Research Findings

### A. Data Sources & URLs
- **Main Download Page:** [MusicBrainz Database Download](https://musicbrainz.org/doc/MusicBrainz_Database/Download)
- **Bulk Datasets (MetaBrainz):** [MetaBrainz Datasets](https://metabrainz.org/datasets)
- **API Documentation:** [MusicBrainz API](https://musicbrainz.org/doc/MusicBrainz_API)

### B. Data Format
- **PostgreSQL Dumps:** The primary distribution format. These are `.tar.bz2` or `.xz` files containing private PostgreSQL dump formats meant for use with `pg_restore` or specific MetaBrainz scripts.
- **JSON Dumps:** A document-oriented format where each entity (Artist, Release, etc.) is a JSON object per line, ideal for NoSQL or document-based ingestion.
- **Canonical Dumps:** Simplified CSV files (`zstd` compressed) designed for machine learning, mapping various versions of recordings to a single "canonical" ID.

### C. Licensing, Costs, and Rate Limits
- **Core Data:** Licensed under **CC0 (Public Domain)**. This includes all core entities like artists, releases, recordings, and labels.
- **Supplementary Data:** Certain tags and ratings are under **CC BY-NC-SA 3.0**.
- **API Rate Limit:** 1 request per second.
- **Costs:** Entirely free for local download and use. Commercial users of the live data feed (for real-time updates) are encouraged to support the MetaBrainz Foundation.

### D. Dataset Size
- **Compressed Core Dump:** Approximately **2 GB to 4 GB** (`mbdump.tar.bz2`).
- **Uncompressed / Full DB Import:** A complete PostgreSQL instance (including all tables and edit history) can consume **100 GB to 300 GB+** of disk space.
- **Minimal Metadata Import:** A subset containing only core relations (no edit history) is significantly smaller (~20-40 GB uncompressed).

### E. Estimated Effort
- **Downloader:** **Low.** Direct download links are available for all dumps.
- **Ingestion/Parsing:** **Moderate to High.** 
    - Setting up the PostgreSQL schema manually is complex.
    - **Recommended:** Use the official `musicbrainz-docker` setup to spin up a pre-configured database environment.
    - Ingesting the JSON dumps is simpler for a custom knowledge graph but loses the native relational constraints of the SQL dump.
    - Mapping MBIDs to other services (Wikidata, Spotify) is highly automated as these links are stored as "URL" entities within the database.

## 4. Conclusion
MusicBrainz is a foundational dataset for any knowledge graph that seeks to understand cultural history and creative relationships. Its strict schema and persistent identifiers make it exceptionally high-quality. The availability of JSON dumps makes it more accessible than in the past, though the full PostgreSQL instance remains the gold standard for complex relationship traversal.
