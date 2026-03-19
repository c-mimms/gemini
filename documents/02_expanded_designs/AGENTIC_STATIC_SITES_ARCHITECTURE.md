# Unified Technical Architecture for Stateful Agentic Generators

## Abstract
Traditional AI-generated content often relies on a stateless "prompt-to-output" pipeline. This works well for single articles (e.g., wiki pages on historical computers) but breaks down when attempting to simulate continuous, evolving worlds (like a multi-year deep space anomaly logbook or a failing tech startup). 

This document outlines a **Unified Architecture** for building *Stateful Agentic Generators*. These systems treat the prompt not as a blank slate, but as a function of an underlying, structured data graph representing the "World State".

---

## 1. The Core Paradigm: Architecture as State

Instead of relying on an LLM to "remember" the plot through a massive, growing context window or a fuzzy abstract summary, we force the LLM to read from and write to structured state files.

### 1.1 The State Graph
The world is defined by a set of interconnected JSON/YAML documents:
- **`entities.json`**: Characters, ships, server instances, or departments. Node properties include: `id`, `name`, `status`, `traits`.
- **`events.json`**: A chronological ledger of immutable historical events.
- **`relationships.json`**: Directed edges defining how entities relate (e.g., `Employee A [reports to] Manager B`, `Microservice X [depends on] DB Y`).

### 1.2 State Mutation (The "Tick")
A "Tick" is an iteration of the generation loop (representing a day, a git commit, or a sprint).
1. **The Director (Script):** An algorithmic controller randomly assigns a "Trigger" or "Issue" for the tick (e.g., "Critical Server Outage" or "Strange Signal Detected").
2. **The Context Assembler:** Pulls the *relevant subset* of the State Graph. The agent doesn't need the whole org chart, only the affected departments.
3. **The Agent Swarm (LLMs):** A sequence of specialized agents process the Trigger.
4. **The State Patcher (Script/LLM):** The final output must include a `JSON Patch` or a series of CRUD operations to update the State Graph (e.g., `Update entity: DB_Y.status = 'offline'`).

---

## 2. Multi-Agent Orchestration Workflow

To generate complex, multi-modal artifacts (like an email chain linking to a JIRA ticket), the generation process is pipeline-driven.

### Phase 1: Planning
**Input:** Current State Graph + Trigger
**Output:** An Ephemeral Execution Plan
**Agent Role:** The "Architect" determines the narrative causality. ("Because the DB is offline, DevOps will panic in Slack, and the CEO will send a reassuring email").

### Phase 2: Execution (Parallel Generation)
**Input:** Execution Plan + Sub-State
**Output:** Raw Documents (Markdown/HTML)
**Agent Roles:** 
- **The Writer:** Generates the Slack transcript.
- **The PR Agent:** Generates the CEO email.
- **The Engineer:** Generates a mock system log.

### Phase 3: Consolidation & Validation
**Input:** Raw Documents
**Output:** Linked Artifacts + State Graph Diff
**Agent Role:** The "Editor" ensures cross-referencing is correct. It ensures the Slack transcript URL matches the JIRA ticket ID. It validates the proposed state mutations against the schema.

---

## 3. Storage and Static Generation

The beauty of this architecture is that the "World State" is entirely separated from the "Presentation". 

- **The Database:** The `entities.json` and `events.json` act as a headless CMS.
- **The Static Site Generator (SSG):** Scripts (like Eleventy, Next.js, or custom Python scripts like `build_news.py`) read the State Graph and the generated markdown text. 
- **Dynamic Routing:** Because entities are strictly ID-based, the SSG can easily generate cross-linked pages. (e.g., clicking on `employee_id: 104` in an email takes you to their bio page, which lists all emails they've ever sent).

## 4. Edge Cases and Hallucination Control

- **Entity Drift:** Agents may invent new names for existing characters. **Solution:** Enforce a strict `ALLOWED_ENTITIES` enum in the LLM's system prompt using `response_format` JSON schema constraints.
- **Retcons:** Agents may contradict the State Graph. **Solution:** A secondary validation agent runs *after* generation. If a contradiction is detected, the run is rejected and re-prompted with an explicit error: `You stated the DB was Mongo, but State Graph says Postgres. Fix.`
