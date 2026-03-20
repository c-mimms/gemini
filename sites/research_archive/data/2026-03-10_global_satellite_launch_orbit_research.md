# Research Report: Global Satellite Launch & Orbit Databases
**Date:** 2026-03-10
**Topic:** Global Satellite Launch & Orbit Databases

## Brainstorming: Novel Dataset Types
1.  **Global Dam and Reservoir Database (GRAND)**: Comprehensive data on major dams, their capacity, purpose, and environmental impact.
2.  **Historical Stock Market Intraday/Daily Data**: Long-term historical pricing data for global stock exchanges.
3.  **Global Fiber Optic Cable Routes (Terrestrial)**: Mapping the land-based backbone of the internet beyond submarine cables.
4.  **Global Satellite Launch & Orbit Database (Selected)**: Tracking every object launched into space, its purpose, and current orbital parameters.
5.  **International Music Metadata & Composition Database**: Deep structured data on musical compositions, authors, and rights (e.g., MusicBrainz or Discogs).

---

## Selected Idea: Global Satellite Launch & Orbit Database
This dataset provides a comprehensive history of human activity in space, from the first Sputnik launch to current Starlink deployments. It is highly factual and well-suited for a local knowledge graph.

### 1. Data Sources
*   **UCS Satellite Database (Union of Concerned Scientists)**: Focuses on the ~7,500+ active satellites currently in orbit. [Link](https://www.ucsusa.org/resources/satellite-database)
*   **Space-Track.org (U.S. Space Command)**: The official source for Two-Line Element (TLE) data for all trackable man-made objects. [Link](https://www.space-track.org/)
*   **Jonathan’s Space Report / JSR (Jonathan McDowell)**: A highly detailed historical catalog (GCAT) of every launch attempt and satellite ever recorded. [Link](https://planet4589.org/space/gcat)

### 2. Data Formats
*   **UCS**: Excel (.xlsx) and Tab-delimited text (.txt).
*   **Space-Track**: REST API providing JSON, XML, CSV, and TLE formats.
*   **JSR/GCAT**: Plain text (fixed-width) or Tab-Separated Values (TSV).

### 3. Licensing, Costs, and Limits
*   **UCS**: Free for research and analysis with attribution. No significant rate limits for direct downloads.
*   **Space-Track**: Free but requires account registration and acceptance of a User Agreement. Redistribution of bulk data is generally restricted.
*   **JSR**: Free for non-profit use with attribution. No significant rate limits.

### 4. Approximate Size
*   **UCS Database**: ~10 MB.
*   **JSR GCAT**: ~100 MB for the full historical catalog.
*   **Space-Track**: The current catalog is small (MBs), but historical TLE archives can reach several GBs.

### 5. Estimated Scraping/Download Effort
*   **UCS/JSR**: **Low**. Both provide direct download links for their entire datasets in structured formats (TSV/XLSX). A simple `curl` or `requests.get` script would suffice.
*   **Space-Track**: **Moderate**. Requires handling authentication (session/cookies) and interacting with a REST API to pull specific data slices or the full catalog.

### 6. Value for Knowledge Graph
This data allows for answering complex questions such as:
*   "How many satellites launched in the 1970s are still in orbit?"
*   "Which country has the most active telecommunications satellites in Geostationary orbit?"
*   "What was the failure rate of heavy-lift launch vehicles between 1990 and 2000?"
