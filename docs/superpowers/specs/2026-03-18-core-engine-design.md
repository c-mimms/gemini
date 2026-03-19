# Core Configurable Engine — Design Spec

## Summary
Design a configurable, long‑running engine that supports idea generation, research, and publishable outputs. The core provides scheduling, tool control, logging, and a minimal schema. Adapters define domain‑specific node types, prompts, validators, and output behavior. “Shape” (pyramid, hourglass, flat) emerges from configuration rather than fixed stages.

## Goals
- Single core engine, many configurations.
- Web research allowed at any layer, per agent permissions.
- Strong auditability: every run is logged with inputs, outputs, tool calls, and token usage.
- Output flexibility: HTML, datasets, reports, metadata, code artifacts.
- Immutable content by default, with opt‑out per configuration.

## Non‑Goals
- A single universal ontology for all domains.
- Mandatory research or citation rules in every config.
- A fixed pipeline stage model.

## Architecture Overview
### Core Engine
- Executes agent runs in parallel (optimistic by default).
- Enforces tool availability per agent role.
- Validates core schema and adapter schemas.
- Writes a per‑run log snapshot including resolved config.

### Adapter Package
- JSON config: node types, agent roles, prompts, validators, scheduling.
- Optional domain tools (e.g., dataset profiling, scraping).
- Output renderers for domain artifacts (e.g., HTML).

### Storage Wrapper
- Core provides a storage API and default layout.
- Adapters map artifacts into `/data` and define sub‑layout.
- Core enforces schema validation and logging.

## Storage + Logging
### Layout (core‑defined)
- `/data/` — adapter artifacts and datasets
- `/state/` — graph storage (nodes/edges)
- `/runs/` — per‑run logs (includes config snapshot)

### Run Log (core‑enforced)
Each run writes a structured log:
- Agent id + role
- Input node ids + excerpts
- Output node ids
- Tool calls (params, result sizes, errors)
- Token usage
- Timing and status
- Config snapshot used for the run

## Scheduling + Parallelism
### Default Scheduler (core)
- Weighted agent selection
- Optimistic concurrency by default
- Optional locking policies if a config requires them

### Parallel Run Behavior
- Most runs create new nodes (no conflicts).
- Metadata updates are permitted but must be logged.
- Adapters can enforce stricter rules when needed.

## Core Schema (Minimum)
### Node
- `id`
- `type`
- `content`
- `metadata`
- `created_at`
- `created_by`
- `content_mutable` (optional; defaults false)

### Edge
- `from_id`
- `to_id`
- `type`
- `metadata`
- `created_at`
- `created_by`

### RunLog
- `run_id`
- `agent_id`
- `inputs`
- `outputs`
- `tool_calls`
- `timing`
- `token_usage`
- `status`
- `config_snapshot`

## Config Model (JSON)
- `node_types`: domain node types and schema references
- `edge_types`: allowed edge types
- `agents`: roles with permissions and input/output policies
- `tools`: default tool library + per‑agent allowlists
- `validators`: schema, format, optional citation rules
- `scheduler`: weights, concurrency, optional locking policy

## Storage Wrapper (Details)
- All read/write access goes through a storage API.
- The API enforces:
  - Schema validation for node/edge creation.
  - Immutable content by default (unless `content_mutable`).
  - Run log creation with config snapshot for every execution.
- Adapters define their own sub‑layout inside `/data`.

## Tool System
### Default Tool Library
- Web search
- HTTP fetch
- File read/write
- Shell exec (opt‑in)
- Image download
- Optional browser automation (Playwright CLI)

### Tool Exposure Rules
- Core ships tool registry.
- Configs define per‑agent allowlists.
- Engine supports different LLM runners:
  - Runner with built‑in tools: adapter maps to them.
  - Naked API runner: core provides tool implementations.

### Tool Safety Defaults
- Shell exec and browser automation are opt‑in.
- Tool calls must be logged with params and outputs truncated or summarized for safe logs.

## Example Mappings (from current workflows)
### Museum
- Node types: `Topic`, `Source`, `Fact`, `Outline`, `Article`
- Format selection stored in run log + article metadata.
- Research agent has web tools; writer does not.
- Output validator enforces `<main class="museum-body">` + metadata header.
- Facts cite sources; article cites facts.

### Georgia Mining (research‑first)
- Node types: `ResearchQuestion`, `Dataset`, `Profile`, `Fact`, `Synthesis`, `Article`
- Format stored in run log + article metadata.
- Profiling step computes row/column and numeric summaries.
- Output includes tables + stat callouts derived from profiles.

### Media Scraper
- Node types: `Source`, `Playlist`, `MediaFile`, `Metadata`
- Scraper agent writes `MediaFile`, metadata agent writes tags.
- Tool use: HTTP fetch, shell exec, optional browser automation.

### Research Community
- Node types: `Hypothesis`, `Source`, `Experiment`, `Paper`, `Review`
- Agents generate, critique, review; best papers promoted via metadata.

## Open Questions
- Should scoring be standardized across configs or remain per‑adapter?
- Should promotion rules be explicit (edges) or implicit (metadata)?
