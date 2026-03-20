# Research Report: Global Telecommunication Standards & Protocol Specifications (3GPP/ITU)

## Brainstormed Ideas
1.  **Global Telecommunication Standards and Protocol Specifications (3GPP/ITU)**: Deep technical knowledge about how the global mobile and internet networks function at a protocol level. (Selected)
2.  **Historical Global Newspaper Archives (Metadata and OCR text)**: Factual historical events, social trends, and localized history from the 18th to 20th centuries.
3.  **Global Building Energy Benchmarking and Performance Data**: Detailed technical data on urban infrastructure efficiency, construction materials, and climate impact.
4.  **International Space Station (ISS) Telemetry and Live Experiment Data**: Real-time and historical engineering data from space-based research.
5.  **Global Standards for Weights, Measures, and Physical Constants (NIST/BIPM)**: The fundamental "source of truth" for all physical measurements, constants, and calibration standards.

---

## Selected Idea: Global Telecommunication Standards (3GPP & ITU-T)
This research focuses on the technical specifications that define modern cellular networks (3G, 4G, 5G, and emerging 6G) and global telecommunication protocols. This data is critical for a knowledge graph that aims to understand the technical architecture of the modern world.

### 1. Data Sources (URLs, APIs, Bulk Download Links)
#### **3GPP (3rd Generation Partnership Project)**
*   **FTP Server (Primary):** `ftp://ftp.3gpp.org/`
    *   **Latest Versions:** `ftp://ftp.3gpp.org/specs/latest/` (Organized by Release)
    *   **Archive:** `ftp://ftp.3gpp.org/specs/archive/` (Organized by Series)
*   **3GPP Forge (OpenAPI/YAML):** [https://forge.3gpp.org/rep/all/5G_APIs](https://forge.3gpp.org/rep/all/5G_APIs) (Official GitLab for 5G Core APIs).
*   **Community Mirror (GitHub):** [https://github.com/jdegre/5GC_APIs](https://github.com/jdegre/5GC_APIs)

#### **ITU (International Telecommunication Union - ITU-T)**
*   **Official Portal:** [https://www.itu.int/itu-t/recommendations/](https://www.itu.int/itu-t/recommendations/)
*   **ITU-R P. Series (Atmospheric/Propagation):** Often implemented in community tools like `ITU-Rpy` on GitHub.

### 2. Data Format
*   **3GPP Specs:** Primarily **ZIP archives** containing **Microsoft Word (.doc/.docx)** files. Some PDF mirrors exist via ETSI.
*   **3GPP APIs:** **OpenAPI 3.0 (YAML)** files.
*   **ITU-T Recommendations:** **PDF** is the standard for free public downloads.
*   **Metadata:** 3GPP provides an **Excel-based Status List** on their portal containing links to all specifications.

### 3. Rate Limits, Licensing, and Costs
*   **3GPP:**
    *   **Access:** Publicly accessible via FTP without authentication.
    *   **Licensing:** Generally open for individual/technical use, but redistribution of the documents themselves is subject to 3GPP's organizational policies (ETSI, ATIS, etc.).
    *   **Costs:** Free.
*   **ITU-T:**
    *   **Individual PDF Access:** Free for the vast majority (90%+) of recommendations.
    *   **Bulk/Commercial:** ITU charges for annual bulk subscriptions and commercial redistribution licenses.
    *   **Joint Standards:** Standards developed jointly with ISO/IEC are usually **paid** (available via ITU Electronic Bookshop).

### 4. Estimated Dataset Size
*   **3GPP Archive:** Several **hundred GBs** for the full historical archive (all releases, all series). A single release (e.g., Rel-18) is typically in the **10-20 GB** range.
*   **ITU-T PDF Collection:** Estimated **50-100 GB** for the complete set of in-force recommendations.
*   **OpenAPI Specs:** Very small (MBs).

### 5. Estimated Effort for Scraper/Download Script
*   **3GPP FTP Scraper:** **Medium Effort**. Existing CLI tools like `download_3gpp` (Python) significantly reduce the work. A custom script using `wget --mirror` or a Python `ftplib` wrapper would be straightforward. The main challenge is parsing the Word (.doc) content into machine-readable text for a knowledge graph.
*   **ITU-T Scraper:** **Medium/High Effort**. Since there is no official FTP/API for bulk PDF downloads, a scraper using `BeautifulSoup` or `Playwright` would be needed to navigate the series-based web structure.
*   **OpenAPI Downloader:** **Low Effort**. Simple `git clone` from 3GPP Forge.

### 6. Value for Knowledge Graph
High. These standards provide the exact schemas, state machines, and protocol definitions that power the global internet. They contain definitions for everything from cryptographic handshakes to the physics of radio wave propagation.
