---
title: "USPTO Patent Bulk Data"
date: 2026-03-19
category: "Law & Governance"
tags: ["patents", "intellectual-property", "innovation", "uspto", "legal"]
---

# Knowledge Graph Data Research: USPTO Patent Bulk Data

## Date: 2026-03-19

## Brainstormed Ideas
1.  **US Patent and Trademark Office (USPTO) Data**: Bulk downloads of patent applications and granted patents. Rich technical/legal info, structured XML/JSON.
2.  **Global Power Plant Database**: Information on power plants globally (type, capacity, generation, location).
3.  **National Library of Medicine (NLM) MEDLINE/PubMed**: Academic abstracts and metadata for life sciences and biomedical information.
4.  **FAA Aircraft Registration and Accidents**: Detailed records of US-registered aircraft and historical accident reports.
5.  **OpenStreetMap (OSM) Planet Dumps**: High-fidelity geographic data including buildings, roads, points of interest.

## Selected Idea
**US Patent and Trademark Office (USPTO) Patent Bulk Data**
Selected for its high factual density, strong structure (XML/JSON), and immense value for building a technical knowledge graph.

## Research Findings

### 1. Where can this data be obtained?
- **USPTO Open Data Portal (ODP)**: [https://developer.uspto.gov/](https://developer.uspto.gov/) - For modern API-driven access and metadata retrieval.
- **Bulk Data Storage System (BDSS)**: [https://bulkdata.uspto.gov/](https://bulkdata.uspto.gov/) - For direct weekly bulk downloads of grants and applications.

### 2. What is the format of the data?
- **XML**: Historical data (1790-2001) and weekly bulk updates for grants and applications.
- **JSON**: Modern metadata and file wrapper data retrieved via the Open Data Portal API.

### 3. Rate limits, licensing, and costs?
- **Licensing**: Public domain data, no license fees.
- **Costs**: Free to download.
- **Rate Limits**:
    - **Bulk Downloads**: 20 downloads per year for the same file per API key (XML files have higher limits).
    - **IP Limit**: 5 files per 10 seconds per IP.
    - **Concurrency**: Burst limit of 1 (serial downloads recommended).
    - **Metadata API**: 5 million calls per week quota.
    - **Signed URLs**: Redirected download links are digitally signed and expire in **5 seconds**.

### 4. Approximate size of the dataset?
- **Weekly Patent Grants**: ~9 GB (compressed) per week.
- **Weekly Patent Applications**: ~11 GB (compressed) per week.
- Total historical size is in the multi-terabyte range.

### 5. Estimated effort to write a scraper/download script?
- **Effort**: Moderate.
- **Requirements**: 
    - Obtain an API key from the USPTO Developer Portal.
    - Handle OAuth2 or API key authentication.
    - Manage the 5-second expiration of signed download links (immediate download trigger).
    - Implement robust error handling and retry logic for large file transfers.
    - Serial download logic to stay within the burst limit.
    - Disk space management for multi-GB ZIP files.

## Conclusion
The USPTO Patent Bulk Data is a goldmine for a local knowledge graph. While the file sizes are large, the data is highly structured and well-documented. A python script using `requests` for API calls and `tqdm` for download progress would be an effective starting point.
