# Project 1: Wiki-World Builder (Procedural Encyclopedia)

## Concept
An agentic system that builds a comprehensive, interconnected encyclopedia for a fictional world (or a highly specific, deep-niche non-fiction topic) over thousands of iterations. Each run generates a single wiki article (e.g., a city, a historical figure, a battle, a specific technology). 

## How it's deeper than the Museum Task
Instead of random, isolated articles that just happen to share a CSS format, this project builds a highly structured graph of knowledge. Articles must reference each other correctly, maintain chronological consistency, and avoid contradicting previously established lore.

## Context Management Strategy: The "Knowledge Graph" State
To solve the context window problem, we do **not** feed the agent previous articles. Instead, we maintain a central, structured database (like SQLite or a simple JSON graph). 
1. **Entities & Relationships:** Every time an agent creates a page, a post-processing script extracts key entities (names, dates, places) and inserts them into the DB as "nodes" and "edges".
2. **Targeted Prompting:** When the agent runs, it is given a specific node to write about. The script queries the DB for the node's immediate neighbors (1 or 2 degrees of separation) and provides a concise bulleted list of established "facts" to ensure consistency.
3. **Empty Link Resolution:** The agent is encouraged to invent new names/concepts (red links). These are stored in the DB as "stub" requests, and become the seeds for future agent runs, ensuring the world expands organically based on its own generated lore.
