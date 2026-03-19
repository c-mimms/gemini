# User Stories & Jobs to Be Done

## Jobs to Be Done (JTBD)

**For the Creator/Developer:**
* **JTBD 1:** "When I want to build a deep, complex digital environment, I want to define the rules and seed the initial state, *so that* an agentic system can populate the rest of the world for me without requiring my manual input for every detail."
* **JTBD 2:** "When simulating a long-running process with LLMs, I need a reliable way to compress, store, and retrieve structured state, *so that* my agents don't hallucinate, contradict themselves, or blow out my API budget on massive context windows."
* **JTBD 3:** "When reviewing my agent's procedural outputs, I need a way to easily manually intervene, edit, or rollback a bad generation, *so that* a single hallucinated logic error doesn't corrupt the entire downstream simulation."
* **JTBD 4:** "When experimenting with generation quality, I need to easily swap out the underlying models or specific prompt templates for different node types, *so that* I can optimize for speed, cost, or reasoning depth depending on the specific task."

**For the End-User/Reader:**
* **JTBD 5:** "When exploring a procedurally generated world or story, I want to encounter elements that reference each other logically over time, *so that* the experience feels handcrafted, immersive, and earned."

---

## User Stories (Agile Breakdown)

### Epic 1: State Management & Memory
* **US 1.1 - Schema Definition:** As an Orchestrator, I need a centralized database schema to store "Entities" and their relationships, so that agents can reference established facts reliably.
* **US 1.2 - Targeted Context Injection:** As an AI Generator Node, I need to receive a structured "Context Payload" with only the immediate neighboring graph data, so that I have strict guardrails for my output.
* **US 1.3 - Entity Resolution Pipeline:** As the Data Ingestion script, I need an automated step to match newly generated entities against existing ones, so that the knowledge graph does not become fragmented with duplicates (e.g., merging "The Dark King" and "King Darion").
* **US 1.4 - Manual Override:** As a Admin, I want a UI or CLI command to forcefully edit a node or delete a generated edge in the database, so that I can fix canon-breaking mistakes.

### Epic 2: Generation Loops & The "Stub" Queue
* **US 2.1 - The Red Link Queue:** As the Task Queue, I need a mechanism to collect new, unwritten concepts requested by agents and prioritize them, so that the most heavily-referenced missing information is generated next.
* **US 2.2 - Output Validation via Secondary LLM:** As the Validation Layer, I want to run a fast, cheap model to explicitly check a new generation against its prompt constraints before committing it to the database, so that malformed JSON or logic errors are caught early.
* **US 2.3 - Archetype Templates:** As a Creator, I want to define different prompt architectures for different types of nodes (e.g., "Battle" vs "Person" vs "Item"), so that the outputs are structurally appropriate for the subject matter.

### Epic 3: User Interaction & Visualization
* **US 3.1 - The Graph Explorer:** As an End-User, I want to see a visual, interactive node-graph of the generated knowledge, so I can understand how everything connects macroscopically.
* **US 3.2 - External 'Bump' Events:** As a Developer, I want an API endpoint to inject an external event (e.g., "A meteorite hits the town") into the active state, so that the simulation must react and integrate unexpected external stimuli into the next generation loop.
