# Research Report: Global Volcanism Program (GVP) Dataset

## Brainstormed Ideas
1.  **Global Historical Conflict/Battle Dataset**: Detailed records of historical battles, including dates, locations (GIS), participants, and outcomes (e.g., Correlates of War).
2.  **Global Volcanism Program (GVP) Dataset**: Comprehensive records of Holocene volcanoes and eruptions, including geographical coordinates, eruption dates, and VEI (Volcanic Explosivity Index).
3.  **Marine Traffic/Shipwreck Records**: GIS data on shipwrecks globally, providing historical and geographical insights into maritime trade routes and disasters.
4.  **Global Cultural Heritage Sites**: Databases of national monuments, protected buildings, and archaeological sites from various national registries (beyond UNESCO).
5.  **Historical Patent Data**: Full text and metadata for patents dating back to the 19th century, reflecting the evolution of technology and human invention.

## Selected Idea: Global Volcanism Program (GVP) Dataset
The Global Volcanism Program (GVP) at the Smithsonian Institution maintains a comprehensive database of Holocene volcanoes and their eruptive history. This dataset is highly structured and provides precise spatial and temporal data, making it ideal for a knowledge graph.

### Research Findings

#### 1. Where can this data be obtained?
The data can be obtained from several official and community-maintained sources:
*   **Official Website**: [Smithsonian Global Volcanism Program](https://volcano.si.edu/)
*   **E3 Application**: [Eruptions, Earthquakes, & Emissions (E3) Web App](https://volcano.si.axismaps.io/) - Provides a "Download Data" feature.
*   **GitHub (TidyTuesday)**: The R for Data Science community maintains a cleaned version in CSV format: [rfordatascience/tidytuesday (2020-05-12)](https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-05-12).
*   **Kaggle**: [Volcano Eruptions in the Holocene Period](https://www.kaggle.com/datasets/smithsonian/volcano-eruptions).

#### 2. What is the format of the data?
*   **CSV**: Available via TidyTuesday and the E3 App.
*   **GeoJSON**: Available via the E3 App.
*   **Excel/XML**: Available through the official GVP search export tools.
*   **WFS (Web Feature Service)**: Available for programmatic GIS queries.

#### 3. Licensing, Rate Limits, and Costs
*   **Licensing**: The data is generally **freely accessible** for research, education, and personal use. Attribution is strictly required. 
*   **Commercial Use**: Commercial or disseminated use is granted on a case-by-case basis and may involve a fee.
*   **Rate Limits**: No explicit rate limits are stated for bulk downloads from the website or GitHub.
*   **Cost**: Free for non-commercial research.

#### 4. Dataset Size
*   **Volume**: Approximately 1,500 Holocene volcanoes and over 11,000 eruptions.
*   **File Size**: Very small (estimated < 50MB in CSV format), making it extremely efficient for local storage and knowledge graph integration.

#### 5. Estimated Effort to Scrape/Download
*   **Effort**: **Low**. 
*   The data can be downloaded directly as CSV files from the TidyTuesday repository or the E3 App. A simple Python script using `pandas` or `requests` could automate the retrieval and parsing of these files in under an hour.

### Conclusion
The GVP dataset is a high-value, low-effort addition to the local knowledge graph. Its structured nature (coordinates, dates, magnitudes) allows for complex spatial and temporal queries regarding geological history.
