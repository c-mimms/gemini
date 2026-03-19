# Research Report: Global Mythology, Folklore, and Sacred Texts Knowledge Base

**Date:** 2026-03-13
**Topic:** Global Mythology, Folklore, and Sacred Texts (The Cultural Knowledge Layer)

## 1. Brainstormed Ideas
- **Global Music Knowledge Base (MusicBrainz/AcoustID)**: A massive, structured graph of artists, releases, labels, and recordings across all genres and history.
- **International Standards and Physical Constants (NIST/CODATA/ISO)**: The fundamental "source of truth" for measurement, physical constants, and technical standards that underpin all science.
- **Global Mythology, Folklore, and Sacred Texts (Sacred-Texts/Gutenberg/Wikidata)**: A rich layer of human cultural heritage, linking deities, myths, rituals, and sacred texts across civilizations. (SELECTED)
- **Global Botanical Traits and Functional Diversity (TRY Database/WFO)**: Beyond distribution data, this focuses on the functional characteristics (height, leaf traits, seed mass) of plant life.
- **Global Historical Demographics and Population Data (Maddison Project/Gapminder)**: Longitudinal data on human population, GDP, and life expectancy spanning centuries to millennia.

## 2. Selected Idea: Global Mythology, Folklore, and Sacred Texts
While previous research has covered "Hard Science" and "Infrastructure," this task explores the "Soft Science" and "Cultural" pillar of the knowledge graph. Mythology and folklore provide a deep network of people (gods/heroes), places (underworlds/mountains), things (relics/symbols), and events (creation/battles) that are essential for a complete model of human knowledge.

## 3. Research Findings

### A. Data Sources & URLs
1.  **Internet Sacred Text Archive (Sacred-Texts.com):** 
    - The largest non-profit archive of religion, mythology, and folklore.
    - **URL:** [https://www.sacred-texts.com/](https://www.sacred-texts.com/)
2.  **Project Gutenberg (Mythology & Epics Subset):**
    - High-quality public domain texts like the *Iliad*, *Odyssey*, *Eddas*, and *The Golden Bough*.
    - **URL:** [https://www.gutenberg.org/](https://www.gutenberg.org/)
3.  **Specialized Classification Datasets (Folklore Structure):**
    - **Trilogy (Folklore Indices):** Tidy data for the Thompson Motif Index (TMI) and Aarne-Thompson-Uther (ATU) Tale Type Index.
    - **URL:** [GitHub - j-hagedorn/trilogy](https://github.com/j-hagedorn/trilogy)
4.  **Hugging Face (Pre-processed Text):**
    - **merve/folk-mythology-tales:** ~247,000 rows of folklore and mythology electronic texts.
    - **URL:** [Hugging Face Dataset](https://huggingface.co/datasets/merve/folk-mythology-tales)
5.  **Specialized APIs & Name Databases:**
    - **Greek Myth API:** Structured data on Greek/Roman deities and heroes ([Link](https://greekmythapi.com/)).
    - **Mythology Names Dataset:** Attributes of deities parsed from Godchecker ([Link](https://github.com/repushko/mythology_names_dataset)).
    - **Sefaria API:** Open-source library of Jewish texts with a robust API ([Link](https://www.sefaria.org/)).

### B. Data Format
- **Raw Texts:** HTML (Sacred-Texts), TXT/EPUB (Gutenberg).
- **Structural Data:** CSV/JSON (GitHub repositories, Hugging Face, APIs).
- **Indices:** Tidy data (CSV) for motif and tale type classification.

### C. Licensing, Costs, and Rate Limits
- **Sacred-Texts:** Most content is public domain (published before 1929). Bulk offline access (DVD/USB) costs ~$100, but individual file scraping is free and permitted for non-commercial use.
- **Project Gutenberg:** Public domain (USA). Highly permissive.
- **Sefaria/Open Source APIs:** Usually CC0 or CC-BY.
- **Rate Limits:** Standard web scrapers should respect `robots.txt` on Sacred-Texts and Gutenberg; bulk downloads are preferred via rsync or direct dataset links.

### D. Dataset Size
- **Sacred-Texts (Full):** ~1,700 books, likely 2-5 GB uncompressed (HTML/Text).
- **Hugging Face Dataset:** ~1 GB (JSON/Parquet).
- **Gutenberg Mythology Subset:** Several GBs of high-quality edited texts.
- **Indices (TMI/ATU):** Small (< 100 MB) but extremely high metadata value.

### E. Estimated Effort
- **Scraper/Downloader:** **Low to Moderate.** The Hugging Face dataset can be downloaded in seconds. A scraper for specific sections of Sacred-Texts is a 1-day task.
- **Ingestion/Parsing:** **Moderate.** Converting raw HTML/TXT into structured "story nodes" in a graph requires entity recognition for names and places.
- **Graph Construction:** **High.** The true value lies in linking a "Deity Node" (from Godchecker) to their "Story Nodes" (from Sacred-Texts) and classifying those stories with "Motif Nodes" (from TMI). This provides a multi-layered cultural graph.

## 4. Conclusion
Integrating Global Mythology and Folklore adds a "narrative layer" to the local knowledge graph. By combining the raw volume of the Hugging Face/Sacred-Texts datasets with the structural rigor of the Thompson Motif Index, we can build a system capable of answering complex cultural questions like "Which deities across different cultures are associated with smithing and have a limp?"
