# Core Architecture: Architecture as State

## 1. The State Graph
Instead of fuzzy LLM summaries, the "World State" is a series of strictly typed JSON/YAML files:
- **`entities.json`**: Core actors, services, or elements (e.g. `Server X`, `Employee Y`).
- **`events.json`**: An immutable, chronological ledger of all history.
- **`relationships.json`**: Directed graphs connecting the entities.

## 2. The Simulation Loop ("The Tick")
Each system operates in discrete steps, or "Ticks":

1. **Trigger Generation:** A script/Director randomly generates or pulls the next event (e.g., "Critical Server Outage" or "Daily ArXiv Pull").
2. **Context Assembly:** The system pulls *only* the relevant subset of the State Graph affecting the trigger.
3. **Agent Swarm Execution:** Specialized LLMs process the trigger and generate the documents/output.
4. **State Patching:** The swarm generates a strict `JSON Patch` to mutate the State Graph in response to their outputs. Validation scripts catch hallucinations (e.g., mutating an ID that doesn't exist) and reject/re-prompt.

## 3. Storage and Static Generation
Separation of concerns: The State Graph is the headless CMS. A Static Site Generator (SSG) or application layer consumes the JSON and the generated Markdown to present the universe dynamically to users.
