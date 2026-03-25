# Recurring Task: Knowledge Graph Data Research & Brainstorming

## Goal
The goal of this task is to brainstorm, research, and evaluate new data sources to scrape and save locally. This data will eventually be used to build a completely local knowledge graph capable of answering any question. 

## Context
You are an autonomous research agent. You are looking for novel, structured or semi-structured datasets that provide deep, factual knowledge. 
Some examples of dataset types to research:
- Government data
- Historical weather data
- GIS datasets of mining claims
- Stock prices
- Books (full text)
- Wikis

## Workflow

1.  **Deduplicate Ideas**:
    -   Check the existing research logs in `/Users/chris/code/gemini/sites/research_archive/data/` (if the directory does not exist, you may create it).
    -   Read through the titles/contents of previously researched ideas to ensure you do not research the same dataset type multiple times.

2.  **Brainstorm**:
    -   Think of 3-5 novel dataset types that have not been researched yet. Focus on high-value, factual, and locally storable data.
    -   Select the single most promising idea from your brainstormed list to pursue for this task run.

3.  **Research the Selected Idea**:
    -   Use your web search and browser tools to investigate the selected dataset.
    -   Find answers to the following questions:
        -   Where can this data be obtained? (Find specific URLs, APIs, or bulk download links).
        -   What is the format of the data? (JSON, CSV, Shapefile, PDF, etc.)
        -   Are there any rate limits, licensing restrictions, or costs associated with scraping/downloading it?
        -   How large is the dataset approximately? (MB/GB/TB)
        -   What would be the estimated effort to write a scraper or download script for this data?

4.  **Produce Research Document**:
    -   Write a structured markdown report detailing your findings. 
    -   The report should include the brainstormed list, the selected idea, and all the research findings from Step 3.
    -   Save this report locally at `/Users/chris/code/gemini/sites/research_archive/data/YYYY-MM-DD_[topic_name]_research.md` (replace the date and topic appropriately).
    
5.  **Publish Site**
    -   Run `python3 /Users/chris/code/gemini/sites/research_archive/build.py --source /Users/chris/code/gemini/sites/research_archive/data/ --s3-bucket s3://gemini-designs-portfolio-2026-v2/research/` to build and publish the site.

6.  **Log Completion**:
    -   Print a message confirming the task has completed and the research document has been saved.
