# Technical Architecture: State-Driven Generation

This document outlines the mechanics of the "Architecture as State" paradigm, allowing agents to maintain consistency across infinite iterations.

## 1. The State Graph (The Vault)
Instead of a flat folder of files, the system perceives the world as a graph of nodes and edges.
- **Nodes:** Entities (People, Places, Code Modules, Historical Events).
- **Edges:** Relationships (Located In, Developed By, Conflicts With).
- **Format:** Strongly typed JSON/YAML schemas (see `schemas/`).

## 2. The Interaction Loop (The Tick)
Every agent action follows these steps:
1.  **Context Query:** The "Sovereign Archivist" queries the State Graph for nodes within 2 degrees of the current task.
2.  **Constraint Generation:** These facts are converted into a "World Bible" for the current prompt.
3.  **Swarm Execution:**
    - **Architect:** Plans the change.
    - **Writer:** Generates the content.
    - **Critic:** Compares the output against the "World Bible" for hallucinations.
4.  **State Mutation:** On success, the graph is updated. Stubs (Empty Links) are generated for needed future content.

## 3. Conflict & Dissonance Engine
When an agent attempts a change that violates the current state:
- The system pauses.
- A "Debugging Agent" or "Inquisitor" is spawned to resolve the lore/logic break.
- The outcome either updates the established fact or rewrites the new content to comply.

## 4. Scaling Lore
By only feeding the agent local neighborhoods of the graph, we bypass context window limits. The world can be infinite while the prompt remains small.
