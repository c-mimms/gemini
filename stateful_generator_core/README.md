# Stateful Generator Core

This folder contains a minimal, configurable engine for long-running, iterative agentic simulations. It uses a write-once node graph with mutable metadata and typed edges for provenance and refinement.

## What’s Implemented
- Write-once nodes with mutable metadata.
- Typed edges (`derived_from`, `refines`, `cites`, `summarizes`).
- Agent definitions with scoped permissions and output specs.
- Validators for schema and format constraints.
- Configs for four task domains (museum, trump fact checks, data research, georgia mining).

## Directory Structure
- `core/`: Engine code (`idea_engine.py`, `graph_store.py`, `config.py`).
- `configs/`: Example engine configurations.
- `cli/`: Demo tooling.
- `tests/`: Unit tests for the core engine.

## Quick Demo
```
python3 /Users/chris/code/gemini/stateful_generator_core/cli/demo_runs.py
```

## Tests
```
python3 -m unittest /Users/chris/code/gemini/stateful_generator_core/tests/test_idea_engine.py
```
