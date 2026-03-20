# Research Report: Global Standards & Technical Specifications Metadata

## Date: 2026-03-17
## Topic: Global Standards & Technical Specifications (ISO/IEC/IEEE/RFC)

### 1. Brainstormed Ideas
- **Global Historical Newspapers Archive Metadata**: Metadata of historical newspapers including titles, locations, dates, and publishers to provide historical context.
- **Global Biological Taxonomies & Phylogenetics**: Comprehensive taxonomic trees and phylogenetic relationships beyond basic species names.
- **Global Legislative Metadata**: Metadata on bills, laws, and legislative processes from various countries.
- **Global Standards & Technical Specifications (ISO/IEC/IEEE/RFC)**: Metadata on technical standards that define modern technology and industry. (SELECTED)
- **Global Postal Code and Administrative Boundary Hierarchy**: A complete mapping of postal codes to high-resolution administrative boundaries.

---

### 2. Selected Idea: Global Standards & Technical Specifications
Technical standards are the "blueprints" of the modern world. Having a local knowledge graph of these standards allows for deep analysis of technological evolution, cross-references between industries, and understanding the foundational rules that govern everything from internet protocols to safety symbols.

### 3. Research Findings

#### A. Data Sources & Access Points
- **IETF (RFCs)**:
    - **Official XML Index**: [rfc-index.xml](https://www.rfc-editor.org/rfc-index.xml) (~14MB). This is the gold standard for RFC metadata.
    - **Bulk Access**: Supported via rsync at `rsync.rfc-editor.org::rfcs-dist`.
    - **Individual Metadata**: Available via JSON at `https://www.rfc-editor.org/rfc/rfc[number].json`.
- **IEEE**:
    - **IEEE Xplore Metadata API**: Provides programmatic access to metadata for IEEE standards, journals, and conferences. Returns JSON or XML. Requires a free API key.
    - **URL**: [ieeexploreapi.ieee.org](https://ieeexploreapi.ieee.org/)
- **ISO (International Organization for Standardization)**:
    - **Online Browsing Platform (OBP)**: [iso.org/obp](https://www.iso.org/obp). Contains metadata for all standards (Scope, Terms, Definitions).
    - **Note**: No direct public bulk API; metadata is typically accessed via the OBP or through national member bodies.
- **IEC (International Electrotechnical Commission)**:
    - **IEC API Portal**: [api-portal.iec.ch](https://api-portal.iec.ch/). Provides OpenAPI/Swagger documentation for standards publications.
    - **Electropedia (IEV)**: [opendata-api.iec.ch](https://opendata-api.iec.ch/). Open Data API for over 20,000 electrotechnical terms and definitions.

#### B. Data Format
- **RFC**: XML (Main index), JSON (Individual), Plain Text (Full text).
- **IEEE**: JSON and XML via API.
- **ISO/IEC**: JSON, XML (via APIs), and potentially CSV/TXT for legacy indices.

#### C. Rate Limits & Licensing
- **RFC**: Generally open and free. No strict rate limits for the XML index.
- **IEEE**: API requires registration; usage is governed by API terms (usually generous for metadata, restricted for full text).
- **ISO/IEC**: Metadata is generally free to browse, but bulk datasets or full standards usually require purchase or specific licensing agreements. Scraping the OBP should be done respectfully.

#### D. Approximate Dataset Size
- **Metadata Only**: ~500 MB to 2 GB for a comprehensive collection of metadata (titles, abstracts, dates, relationships) for the major bodies.
- **Full Text**: Significantly larger (TB range) and generally behind paywalls.

#### E. Estimated Effort
- **Low (RFC)**: A simple Python script can parse the `rfc-index.xml` in a few hours.
- **Medium (IEEE/IEC)**: Requires API key management and handling paginated JSON responses. 1-2 days of development.
- **High (ISO)**: May require a sophisticated scraper for the Online Browsing Platform to extract structured metadata without a public bulk API. 3-5 days of development.

### 4. Conclusion
The RFC index is an immediate "quick win" for the knowledge graph. IEEE and IEC provide structured API access that is highly valuable. ISO remains the most challenging but contains some of the most critical high-level industrial standards. Integrating these would create a powerful map of global technical governance.
