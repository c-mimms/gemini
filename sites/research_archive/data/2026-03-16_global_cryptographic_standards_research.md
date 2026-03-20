# Research Report: Global Cryptographic Standards & Protocols (RFCs, NIST, IANA)

**Date**: 2026-03-16
**Topic**: Global Cryptographic Standards & Protocols
**Researcher**: Gemini CLI

---

## 1. Brainstormed Ideas
Below are 5 novel dataset types researched for the local knowledge graph:
1.  **Global Film History & Archive Metadata**: Comprehensive metadata of historical films, directors, and archives beyond commercial databases.
2.  **Global Public Transit Networks (GTFS Aggregations)**: Mapping stops, routes, and agencies worldwide for transit infrastructure knowledge.
3.  **Global Cryptographic Standards & Protocols (RFCs/NIST)**: Deep technical specifications for internet and security protocols that govern modern technology.
4.  **Global Telecommunications Tower Infrastructure (OpenCellID)**: Physical locations and technical details of mobile network infrastructure worldwide.
5.  **Global Historical Manuscripts & Papyrology Records**: Digital records of ancient texts, their provenance, and contents for cultural/historical depth.

**Selected Idea for this Research Run**: Global Cryptographic Standards & Protocols (RFCs/NIST/IANA)

---

## 2. Research Findings: Global Cryptographic Standards & Protocols

### Description
A comprehensive collection of technical standards, protocol specifications, and cryptographic algorithm registries that define how the internet and secure communications function. This includes IETF RFCs, IANA protocol parameters, and NIST FIPS/SP 800 standards.

### Where can this data be obtained?
*   **IETF RFCs (Request for Comments)**:
    *   **Official XML/Bulk**: `rsync -avz rsync.rfc-editor.org::rfcs-xml ./rfcs`
    *   **JSON Bibliographic Data**: [GitHub: ietf-tools/relaton-data-rfcs](https://github.com/ietf-tools/relaton-data-rfcs)
    *   **Metadata Export**: [IETF Datatracker](https://datatracker.ietf.org/doc/rfc/all/) (CSV export available).
*   **IANA (Internet Assigned Numbers Authority) Registries**:
    *   **Bulk Retrieval**: `rsync -avz rsync.iana.org::assignments/ ./iana-registries`
    *   **Individual XML/CSV**: Each registry at [iana.org/assignments](https://www.iana.org/assignments/) has XML/CSV download links.
*   **NIST Standards (FIPS and SP 800 Series)**:
    *   **OSCAL Content (JSON/YAML/XML)**: [GitHub: usnistgov/oscal-content](https://github.com/usnistgov/oscal-content) (Full control catalogs like SP 800-53).
    *   **CPRT (Cybersecurity and Privacy Reference Tool)**: [NIST CPRT Catalog](https://csrc.nist.gov/projects/cprt/catalog) (Flat JSON files for various standards).
    *   **Publication Metadata**: [CSRC Publications Search](https://csrc.nist.gov/publications/sp800) (CSV/XLSX export).
*   **Cryptographic Algorithms**:
    *   **SCANOSS Crypto Dataset (YAML)**: [GitHub: scanoss/crypto_algorithms_open_dataset](https://github.com/scanoss/crypto_algorithms_open_dataset).
    *   **CSOR (Computer Security Objects Register)**: [NIST CSOR](https://csrc.nist.gov/projects/computer-security-objects-register) (XML/CSV OID lists).

### What is the format of the data?
*   **XML**: Primary for IETF RFCs and IANA registries.
*   **JSON/YAML**: Available for NIST OSCAL/CPRT data and Relaton RFC metadata.
*   **CSV/XLSX**: Available for publication lists and protocol registries.
*   **PDF**: Full original documentation for NIST standards.

### Are there any rate limits, licensing restrictions, or costs?
*   **Cost**: Free. All data is provided as public service or under open standards licenses.
*   **Licensing**:
    *   **NIST**: US Government public domain.
    *   **IETF/IANA**: Generally open standards; some restrictions on derivative works of the RFC text itself, but metadata/registries are free to use.
    *   **SCANOSS**: CC-BY-4.0.
*   **Rate Limits**: None for rsync access. Standard web rate limits apply for GitHub/web downloads.

### How large is the dataset approximately?
*   **IETF RFCs (XML/JSON)**: ~500 MB - 1 GB (10,000+ files).
*   **IANA Registries**: < 100 MB.
*   **NIST Standards (OSCAL/CPRT)**: ~200 MB.
*   **Total Estimated**: 2 - 5 GB (if including full-text PDFs of NIST standards).

### Estimated effort to write a scraper or download script?
*   **Effort Level**: **Low-Medium**.
*   **Reasoning**: Bulk download is trivial via `rsync`. The primary effort lies in parsing the various XML and JSON schemas into a unified format for the knowledge graph. IANA and IETF XML formats are highly consistent, while NIST OSCAL is complex but well-documented.

---

## 3. Knowledge Graph Integration Potential
This dataset provides the "rules" of technology. Integrating it allows the knowledge graph to:
*   Identify which protocols are defined in specific RFCs.
*   Map cryptographic algorithms to their OIDs and security strengths.
*   Link NIST security controls (SP 800-53) to the protocols that implement them.
*   Answer deep technical questions about port numbers, TLS cipher suites, and encryption standards.
