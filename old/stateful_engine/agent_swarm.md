# The Agent Swarm

Complex generations require specialized roles instead of a single prompt. The Swarm Pipeline ensures high-quality, heavily structured execution on each "Tick".

## Phases of Generation

### Phase 1: Planning
**Role:** The Architect
**Responsibility:** Receives the current Sub-State and Trigger. Determines the narrative or logical causality. Generates an Ephemeral Execution Plan specifying exactly what sub-documents or actions need to occur.

### Phase 2: Execution (Parallel)
**Role:** Swarm Specialists (The Writer, The Engineer, The Researcher, etc.)
**Responsibility:** Takes the Execution Plan and Sub-State to write raw content (e.g., "Slack Transcripts", "Code Diffs", "Wiki Entries"). Operates in parallel.

### Phase 3: Consolidation & Validation
**Role:** The Editor / The Patcher
**Responsibility:** Consolidates all raw documents. Checks for contradictions against the strict State Graph. Generates the final JSON diff to mutate the State Graph. If contradictions exist, flags an error for Phase 2 retry.
