---
title: "ClinVar Human Genomics Database"
date: 2026-03-12
category: "Life Sciences"
tags: ["genomics", "genetics", "clinvar", "disease", "medicine"]
---

# Research Report: Human Genomics & Health (ClinVar)

## Date
2026-03-12

## Brainstormed Ideas
Below are 5 novel dataset types evaluated for the local knowledge graph:
1.  **Human Genomics (ClinVar)**: A public archive of human genetic variations and their relationship to phenotypes and diseases. High-value, factual, and extremely structured.
2.  **Global Trade Statistics (UN Comtrade)**: Detailed data on imports/exports between countries for thousands of products. Valuable for economic and supply chain knowledge.
3.  **Ancient Literature & Primary Sources (Perseus Digital Library)**: Full text of Greek, Latin, and other ancient texts with linguistic annotations. Excellent for cultural and historical depth.
4.  **World Intellectual Property: Trademarks (WIPO/USPTO)**: Global database of registered trademarks and logos. Complements the existing research on patents.
5.  **Global Demographic Trends (World Bank Open Data)**: Thousands of indicators (GDP, population, health metrics) for all countries. Provides a statistical foundation for world knowledge.

**Selected Idea**: Human Genomics (ClinVar)

---

## Selected Idea: Human Genomics (ClinVar)

### 1. Overview
ClinVar is a freely accessible, public archive of reports of the relationships among human variations and phenotypes, hosted by the National Center for Biotechnology Information (NCBI). It aggregates data from clinical laboratories, research organizations, and expert panels to provide a centralized resource for understanding the clinical significance of genetic variants.

### 2. Where can this data be obtained?
The primary method for obtaining bulk data is through the **NCBI FTP server**:
- **FTP URL**: `ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/`
- **Specific Path for XML**: `xml/vcv/` (Variation-level records) or `xml/rcv/` (Record-level records).
- **Specific Path for VCF**: `vcf_GRCh37/` or `vcf_GRCh38/`.
- **API Access**: Can be queried via NCBI Entrez E-utilities (`esearch`, `esummary`, `efetch`).

### 3. Data Format
ClinVar data is provided in multiple formats to suit different needs:
- **XML**: The most comprehensive format, containing all submitted evidence, assertions, and metadata.
- **VCF (Variant Call Format)**: Standard format for simple variants (SNPs and small Indels), mapped to human genome assemblies (GRCh37/38).
- **Tab-delimited (TXT)**: Summary files (e.g., `variant_summary.txt.gz`) that provide high-level details for quick lookups.

### 4. Licensing, Rate Limits, and Costs
- **Licensing**: As a work of the United States Government, ClinVar data is in the **public domain**. It is free to use, redistribute, and modify without restriction.
- **Costs**: There is **no cost** to download or use the data.
- **Rate Limits**:
    - **FTP**: No strict rate limits, but users are encouraged to use automated tools responsibly.
    - **API**: 3 requests per second without an API key; 10 requests per second with a free NCBI API key.

### 5. Dataset Size
The dataset is substantial and grows weekly:
- **Compressed XML**: ~10–15 GB (e.g., `ClinVarVariationRelease_00-latest.xml.gz`).
- **Uncompressed XML**: Can exceed 100 GB.
- **VCF Files**: ~50–100 MB per genome assembly.
- **Summary TXT**: ~150–200 MB compressed.

### 6. Estimated Effort to Scrape/Download
- **Download**: **Low effort**. A simple `wget` or `rsync` script can mirror the FTP directories.
- **Parsing**: **Moderate effort**. While VCF and TXT files are easy to parse with standard tools, the XML files are deeply nested and require specialized streaming parsers (like `lxml` in Python) to handle the 100GB+ uncompressed volume efficiently.
- **Integration**: **Moderate effort**. Mapping variants to clinical conditions requires handling standardized vocabularies like MedGen and OMIM.
