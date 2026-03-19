# Research Report: Linguistic and Etymological Knowledge Base

**Date:** 2026-03-05
**Topic:** Linguistic and Etymological Knowledge Base (Unified WordNet & Wiktionary)

## 1. Brainstormed Ideas
- **Global Biological and Environmental Data (GBIF/IUCN)**: Detailed species distributions, conservation status, and ecological roles.
- **Universal Patents Data (USPTO/EPO)**: Structured information on inventions, technological advancements, and industrial classifications.
- **Linguistic and Etymological Databases (Wiktionary/WordNet)**: Hierarchical relationships between words, their historical origins, and semantic mappings. (SELECTED)
- **Astronomical Catalogs (SIMBAD/NED)**: Detailed properties and positions of celestial objects (stars, galaxies, exoplanets).
- **Global Legislative and Regulatory Data (OpenStates/EUR-Lex)**: Full-text laws, bills, and regulatory changes across different jurisdictions.

## 2. Selected Idea: Linguistic and Etymological Knowledge Base
Building a local knowledge graph of human language, including definitions, synonyms, hypernyms (is-a relationships), and etymological roots (origins of words). This provides a foundational "semantic layer" for any general-purpose knowledge graph.

## 3. Research Findings

### A. Data Sources & URLs
1.  **Wiktionary (Structured):** 
    - **Source:** [Kaikki.org](https://kaikki.org/dictionary/rawdata.html) (Highly recommended over raw Wikimedia dumps).
    - **Alternate Source:** [dumps.wikimedia.org](https://dumps.wikimedia.org/enwiktionary/)
2.  **WordNet:**
    - **Open English WordNet (Active):** [GitHub Releases](https://github.com/globalwordnet/english-wordnet/releases)
    - **Princeton WordNet (Legacy):** [Princeton WordNet Download](https://wordnet.princeton.edu/download/current-version)
3.  **Etymological Wordnet (etymwn):**
    - **Source:** [Gerard de Melo's Research Page](http://gerard.demelo.org/etymwn/) or [Archive.org](https://archive.org/details/etymwn-20130208)

### B. Data Format
- **Wiktionary (Kaikki):** JSONL (JSON Lines), one object per word/sense.
- **Wiktionary (Official):** XML (Wikitext format, requires heavy parsing).
- **Open English WordNet:** XML (LMF), JSON-LD, RDF.
- **Princeton WordNet:** Custom positional text files or Prolog.
- **Etymological Wordnet:** TSV (Tab-Separated Values) with three columns: `Word1`, `Relation`, `Word2`.

### C. Licensing, Costs, and Rate Limits
- **Wiktionary:** CC BY-SA 4.0 and GFDL. Free for use (including commercial) with attribution and share-alike requirements.
- **Open English WordNet:** CC-BY 4.0. Free with attribution.
- **Princeton WordNet:** Custom BSD-style license. Highly permissive.
- **Etymological Wordnet:** CC BY-SA.
- **Rate Limits:** Bulk downloads via dumps or GitHub releases have no operational rate limits beyond standard server bandwidth.

### D. Dataset Size
- **Wiktionary (English):** ~2.3 GB compressed (JSONL.gz), ~20 GB uncompressed (JSONL).
- **WordNet:** Small, typically < 100 MB.
- **Etymological Wordnet:** Small, typically < 50 MB (TSV).

### E. Estimated Effort
- **Scraper/Downloader:** **Low.** The data is available as direct bulk download links. A simple `wget` or `curl` script can retrieve the files.
- **Ingestion/Parsing:** **Moderate.**
    - WordNet and Etymological Wordnet are straightforward to parse (TSV/XML).
    - Wiktionary (via Kaikki) is well-structured JSON, but the sheer volume (20GB) requires efficient stream processing to map into a knowledge graph.
    - Mapping these three datasets together (e.g., linking a Wiktionary entry to its WordNet synset) is the most complex part of the task.

## 4. Conclusion
The combination of Wiktionary (for breadth and modern slang/usage), WordNet (for formal semantic structure), and Etymological Wordnet (for historical lineage) creates a powerful local linguistic foundation. The availability of pre-parsed JSONL for Wiktionary significantly reduces the barrier to entry for this dataset.
