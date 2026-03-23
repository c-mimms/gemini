---
title: "Ancient Coinage & Numismatics"
date: 2026-03-09
category: "History & Culture"
tags: ["numismatics", "coins", "ancient-history", "archaeology", "economics"]
---

# Research Report: Ancient Coinage (Numismatics) Knowledge Base

## Date: 2026-03-09
## Topic: Ancient Coinage (Numismatics)

---

## 1. Brainstormed Ideas
- **Global Deep-Sea Hydrothermal Vent Database**: Specific locations, chemistry, and biology of vents.
- **World Traditional Music/Instruments Database**: Metadata on ethnic musical styles, instruments, and recordings (e.g., Smithsonian Folkways).
- **International Space Station (ISS) Experiments Database**: Detailed records of all experiments conducted on the ISS, results, and involved researchers.
- **Global Cryptocurrency/Blockchain Address Clusters**: Tagged data for known entities (exchanges, mixers, hackers) for forensic knowledge.
- **Ancient Coinage (Numismatics) Database**: (Selected) Roman, Greek, and other ancient coins with metadata on find spots, weight, and imagery.

---

## 2. Selected Idea: Ancient Coinage (Numismatics) Database
Ancient numismatics provides a highly structured and factual record of history, economics, and geography. Projects like **Nomisma.org** and **OCRE** (Online Coins of the Roman Empire) have pioneered the use of Linked Open Data (LOD) in the humanities, making this an ideal dataset for a local knowledge graph.

---

## 3. Research Findings

### Where can this data be obtained?
- **Nomisma.org**: The central hub for numismatic Linked Open Data. It provides identifiers for mints, rulers, denominations, and materials.
    - **GitHub**: [github.com/nomisma/data](https://github.com/nomisma/data) (Contains core RDF data).
    - **SPARQL Endpoint**: [http://nomisma.org/sparql](http://nomisma.org/sparql)
- **OCRE (Online Coins of the Roman Empire)**: A complete corpus of Roman Imperial coinage (from Augustus to Zeno).
    - **Datasets Page**: [numismatics.org/ocre/datasets](http://numismatics.org/ocre/datasets)
- **CRRO (Coinage of the Roman Republic Online)**: [numismatics.org/crro](http://numismatics.org/crro/)
- **PELLA (Coins of the Ptolemaic Empire)**: [numismatics.org/pella](http://numismatics.org/pella/)

### What is the format of the data?
- **RDF/XML & Turtle**: The primary formats for the full Linked Open Data graph.
- **JSON-LD**: Available for individual concept records via the REST API.
- **CSV**: Search results from OCRE/Nomisma can be exported directly as CSV.
- **GeoJSON/KML**: Available for geographic concepts like mints and find spots.

### Licensing, Rate Limits, and Costs
- **Licensing**: Most data provided by the American Numismatic Society (ANS) and Nomisma is released under **CC-BY** (Creative Commons Attribution) or **CC0** (Public Domain). Specific museum specimen data linked through these hubs may have varying licenses (e.g., CC-BY-NC).
- **Rate Limits**: No strict rate limits are advertised for the SPARQL endpoint or REST APIs, but bulk users are encouraged to use the nightly RDF dumps or GitHub repository to reduce server load.
- **Costs**: Free and open access.

### Approximate Dataset Size
- **Nomisma Core Concepts**: ~50-100 MB (compressed RDF).
- **OCRE Type Corpus**: ~43,000 coin types. An RDF dump is approximately 200-500 MB.
- **Linked Specimens**: Millions of individual coin records across 30+ international collections. A full crawl of specimen metadata could reach several GBs.

### Estimated Effort for Scraper/Download Script
- **Effort: Low to Moderate**
- **Strategy**: 
    1. Clone the `nomisma/data` GitHub repository for core concepts (mints, rulers, etc.).
    2. Download the OCRE/CRRO RDF dumps directly from their respective dataset pages.
    3. Use a SPARQL client (in Python or Node.js) to query the endpoint for specific cross-referenced data that might not be in the flat dumps.
    4. Mapping the RDF to a local Graph database (e.g., Neo4j or a simple triple store) is straightforward due to the clean ontology used by Nomisma.

---

## 4. Conclusion
The Ancient Coinage dataset is a "gold standard" for historical data. It links geography (mints), biography (emperors), and economics (denominations) into a cohesive graph. The availability of clean RDF dumps and a public SPARQL endpoint makes it one of the easiest high-value datasets to integrate into a local knowledge graph.
