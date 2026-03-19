# Configurable Idea + Research + Output Engine — Design Document

## Summary
This document defines a configurable, long‑running engine that generates ideas, conducts research, and produces publishable outputs. The architecture is graph‑first, with write‑once content nodes, mutable metadata, and typed edges for provenance and refinement. “Shape” (pyramid, hourglass, flat, etc.) emerges from configuration rather than fixed stages.

## Goals
- Support multiple configurations of the same core engine.
- Allow unconstrained idea generation or focused research‑to‑output pipelines.
- Enable web research at any layer, per agent permissions.
- Provide traceable facts and optional citation enforcement.
- Keep outputs flexible, including HTML, datasets, and reports.
- Preserve immutability of content while allowing refinement via new nodes.

## Non‑Goals
- Enforce a single schema across all configurations.
- Require web research on every run.
- Force a rigid stage pipeline in all runs.

## Core Concepts
- Node: Immutable content plus mutable metadata.
- Edge: Typed link between nodes, used for provenance and refinement.
- Run: A single agent execution that reads scoped nodes and writes new nodes.
- Config: Defines node types, agent roles, permissions, and validators.
- Shape: Emergent distribution of runs across node types.

## Node Model
Required fields:
- `id`
- `type`
- `content` (immutable)
- `metadata` (mutable map)
- `created_at`
- `created_by`

Refinement is implemented by creating a new node and linking it to the original.

## Edge Model
Required fields:
- `from_id`
- `to_id`
- `type`
- `metadata`

Common edge types:
- `derived_from`
- `refines`
- `cites`
- `summarizes`
- `contradicts` (optional, per config)

## Agent Model
Agents are defined by:
- `id`
- `role`
- `permissions` (web_search, read_types, write_types)
- `input_policy` (max_nodes)
- `output_policy` (outputs, link_to_inputs, cite_inputs)

Permissions are enforced per configuration, not globally.

## Validation
Validators are configurable per configuration:
- Schema validation for node types.
- Format validation for output structure.
- Optional citation coverage.

Default requirement:
- Schema validation enabled.

## Shape and Run Distribution
Shape is not a fixed pipeline. It emerges from:
- Run scheduling and agent weights.
- Read/write constraints per agent.
- Validation rules and gating.

Examples:
- Pyramid shape: many idea‑generators, strict promotion criteria.
- Hourglass shape: wide exploration, narrow curation, wide output.
- Flat shape: direct idea → output or list‑only configurations.

## Web Research
Web research is allowed per agent role. The engine must:
- Allow research at any layer.
- Support “offline” operation for tests.
- Preserve sources as first‑class nodes when research is enabled.

## Configuration Examples
Two full standalone replacements exist:
- Mimms Museum Engine
- Georgia Mining Research Engine

Each is a self‑contained folder with its own state, data, prompts, and output directory.

## Mimms Museum Engine (Replacement)
Focus:
- Reproduces existing museum pipeline behavior end‑to‑end.
- Uses format selection, topic selection, research, facts, outline, and HTML output.
- Optional publish step.

Key configuration choices:
- Node types: `FormatChoice`, `Topic`, `Source`, `Fact`, `Outline`, `Article`
- Output enforcement: HTML wrapper, metadata header, citations to facts.
- Web research permitted only for researcher role.

## Georgia Mining Research Engine (Improved)
Focus:
- Research‑first output with heavy data profiling and traceability.
- Prioritizes dataset‑derived facts and explicit profiling.

Key configuration choices:
- Node types: `FormatChoice`, `ResearchQuestion`, `Dataset`, `Profile`, `Fact`, `Synthesis`, `Article`
- Profiling step computes row/column counts and numeric summaries.
- Article generation includes tables and stat callouts derived from profiles.

## Replacement Strategy
Each engine is standalone to allow:
- Side‑by‑side comparison with the existing pipelines.
- Safe experimentation without impacting production outputs.
- Clear migration path.

## Milestones
1. Stabilize core node/edge model and validators.
2. Expand configuration schema to support richer policies.
3. Add strict validators for output constraints and citation coverage.
4. Build adapters for additional domains beyond museum/mining.

## Open Questions
- Define a universal “fact ledger” format or keep per‑config.
- Decide how to express scoring and ranking in metadata.
- Determine how much of promotion is explicit vs implicit.
