# Project 3: The Deep-Space / Anomaly Logbook

## Concept
A continuous, unfolding narrative told through the daily logs of a scientific research outpost or deep space mission studying a complex, slow-moving anomaly. Every run generates a new daily entry, mixing mundane operational details, scientific hypotheses, and strange events.

## How it's deeper than the Museum Task
This relies heavily on narrative continuity and mystery-building. The agent is actively trying to "solve" or "explore" something, creating a serial fiction experience rather than standalone informative articles. The tone must remain consistent, and hypotheses must evolve naturally.

## Context Management Strategy: RAG (Retrieval-Augmented Generation) & Summarization
Because tracking plot is harder than tracking isolated facts, we use a two-tiered memory system:
1. **The "Story Bible" Summary:** A strictly constrained, 500-word summary of the "Story So Far" that is systematically updated every 10 runs by a secondary summarizing agent. This acts as the unbreakable core lore for the prompt.
2. **Vector DB (RAG) for Specifics:** All past logs are embedded in a local vector database. Before the agent writes a new log, it decides what scientific test or narrative thread it wants to pursue today. It queries the vector DB (e.g., "What were previous results regarding the blue crystals?") and receives 2-3 highly relevant past entries to inject into its prompt. This allows it to reference an experiment from 200 runs ago perfectly, without keeping all 200 runs in context.
