# Research Report: International Space Station (ISS) Experiments and Results

**Date:** 2026-03-17
**Researcher:** Gemini CLI
**Topic:** ISS Scientific Experiments, Facilities, and Results

---

## 1. Brainstormed Ideas
For this research cycle, the following novel dataset types were considered:
1.  **International Space Station (ISS) Experiments and Results**: A structured database of scientific experiments conducted on the ISS, including metadata on research goals, principal investigators, and outcomes. (SELECTED)
2.  **Global Biological High-Containment Labs (BSL-3/4)**: Locations and details of high-security laboratories globally, including research focus and institutional affiliations.
3.  **Global Historical Newspaper Archives Metadata**: Structured records of digitized historical newspapers, including titles, dates, locations, and OCR quality indicators.
4.  **Global Radio Astronomy Observatories and Targets**: A comprehensive list of radio telescopes, their technical specifications, and historical observation targets.
5.  **Global Submarine Telecommunications Cable Landing Stations**: Precise geographical coordinates and technical details of undersea cable landing points.

---

## 2. Selected Idea: ISS Experiments and Results
The International Space Station serves as a unique microgravity laboratory. Over 3,000 experiments have been conducted by researchers from over 100 countries. This dataset provides a high-value, factual foundation for a knowledge graph focusing on space science, biology, physics, and international collaboration.

---

## 3. Detailed Research Findings

### Where can this data be obtained?
*   **Space Station Research Explorer (SSRE):** The primary NASA portal for all ISS research. It includes data from NASA, ESA, JAXA, CSA, and Roscosmos.
    *   **All Experiments Report:** [NASA SSRE Reports](https://www.nasa.gov/mission_pages/station/research/experiments/explorer/report.html?type=all_experiments)
*   **NASA Open Science Data Repository (OSDR):** Focuses on biological and physical sciences, integrating GeneLab and the Ames Life Sciences Data Archive (ALSDA).
    *   **API:** [OSDR Public API](https://osdr.nasa.gov/reference/osdr-public-api/)
*   **JAXA DARTS (Kibo):** Specific data for Japanese experiments on the Kibo module.
    *   **URL:** [JAXA DARTS](https://darts.isas.jaxa.jp/iss/kibo/)
*   **ESA Erasmus Experiment Archive (EEA):** Metadata for European experiments.
    *   **URL:** [ESA EEA](https://eea.spaceflight.esa.int/)

### What is the format of the data?
*   **Bulk Metadata:** CSV, Excel (via SSRE Reports).
*   **Programmatic:** JSON (via OSDR API and data.nasa.gov SODA API).
*   **Linked Data:** RDF (NASA provides tools like `linkedISA` to convert ISA-Tab experiment metadata into RDF for Knowledge Graph use).

### Are there any rate limits, licensing, or costs?
*   **Licensing:** Data produced by NASA is generally in the **Public Domain** (U.S. Government work). Partner data (ESA/JAXA) is usually free for educational/research use but may have specific attribution requirements.
*   **Costs:** Free.
*   **Rate Limits:** Standard NASA API limits apply (typically 1,000-5,000 requests per hour depending on the endpoint), but bulk CSV/JSON downloads bypass the need for high-frequency polling.

### How large is the dataset?
*   **Metadata:** The "All Experiments" metadata is small (~50-100 MB).
*   **Full Data:** If including raw "Omics" data, imagery, and telemetry, the dataset grows into the **Terabyte (TB)** range.
*   **Publications:** Metadata for ~4,000+ publications associated with ISS research is available as a separate ~20 MB CSV.

### Estimated effort to write a scraper or download script?
*   **Effort: Low to Medium.**
*   A simple Python script using `requests` can pull the entire "All Experiments" CSV in minutes. 
*   Mapping this to a Knowledge Graph (RDF/Triples) is the primary task. Using NASA's existing `linkedISA` mappings or DBpedia's ISS extracts would significantly accelerate the process.

---

## 4. Conclusion
The ISS Experiments dataset is a "gold mine" for a local knowledge graph. It connects space agencies, scientific disciplines (biology, combustion, physics), international researchers, and specific hardware modules. It is highly structured and professionally maintained, making it an ideal candidate for ingestion.

---
**Status:** Research Complete. Ready for Scraper Implementation.
