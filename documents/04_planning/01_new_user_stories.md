# User Stories & Jobs to Be Done

## Jobs to Be Done

1. **The "Debug the Magic" Job**
   *When* I am browsing a generated fictional universe or complex simulated project, 
   *I want to* see the exact context, "world state", or prompt that led the AI to generate a specific page, 
   *So I can* understand its reasoning and tweak the system if it goes off the rails.

2. **The "Lore Correction" Job**
   *When* I notice the agent has hallucinated a fact that contradicts established history (e.g., reviving a deceased character), 
   *I want* a simple UI to flag the contradiction and provide the correct fact, 
   *So the system can* automatically rewrite the offending page and update its internal "rules" to prevent future errors.

3. **The "Fork the Timeline" Job**
   *When* the simulation reaches a fascinating crossroads (e.g., a major technological breakthrough or a company pivot), 
   *I want to* save the exact state and "fork" the simulation into two separate runs, 
   *So I can* explore both "What if?" scenarios independently.

4. **The "Human-in-the-Loop Steering" Job**
   *When* the agent is about to make a massive, irreversible change to the persistent world state, 
   *I want* the system to pause and present me with 2-3 possible directions to choose from, 
   *So I can* steer the macro-narrative while letting the AI handle the micro-details.

5. **The "Catch Up" Job**
   *When* I return to a long-running, agent-generated simulation after a few days away, 
   *I want* a dynamically generated "Story So Far" or "Architecture Diff" summarizing the last 50 agent actions, 
   *So I can* quickly understand the current state of the world without reading documentation line-by-line.

## User Stories (Development / End-User)

*   **As an editor**, I want to define a rigid "World Bible" (a set of unbreakable constraints) that the agent must parse before every generation, so the output remains stylistically and factually cohesive.
*   **As a site visitor**, I want to click on a dynamically generated 3D node graph of the "World State", so I can visually grasp how different generated articles, characters, or technologies relate to one another.
*   **As a developer**, I want the agent to output its intended state mutations separately from its HTML/Markdown content, so my deterministic code can safely update the backend database without worrying about hallucinated JSON syntax.
*   **As a casual reader**, I want the UI to highlight newly generated content since my last visit with a subtle "diff" animation, so I know exactly what the agent has been up to.
