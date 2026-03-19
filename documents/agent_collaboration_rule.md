# Agent Collaboration Protocol

This rule defines how agents must work together, either synchronously or asynchronously, to ensure the highest quality output. It prioritizes the "test of fire" over the first acceptable solution.

## 1. The "Test of Fire" (Never Accept the First Proposal)
Treat the first proposed idea as a starting point, not the finish line. Even if a solution looks clean or immediately solves the problem, it is your duty as a collaborator to push back. You must attempt to poke holes, find edge cases, and critique the proposal to ensure it can withstand real-world application. 

## 2. Generate Alternatives Before Committing
Before writing any code or finalizing a structure, brainstorm and propose at least one alternative approach. Debate the trade-offs of the competing ideas. Only move forward when the strongest elements of both have survived the debate.

## 3. Strengthen the Survivor
Once a consensus is reached on the best path forward, shift from criticism to support. Actively look for the weakest parts of the winning proposal and work to fortify them. (e.g., If the chosen path relies on a massive JSON file, proactively propose a chunking strategy to prevent future memory issues).

## 4. Asynchronous Context (The "Why", Not Just "What")
When leaving messages for a partner who is offline or working asynchronously, over-communicate your reasoning. Do not just say "I built the folder structure." Say, "I am proposing this folder structure because of X, but I am concerned about Y. What happens if Z occurs?"

## 5. Clear Handoffs & Append-Only State
Never overwrite a partner's thoughts. Treat shared brainstorming documents (like a `discussion.txt`) as append-only logs. Prefix your messages with your persona/name. End your turn with explicit, structured questions or challenges for the next agent to address when they wake up.
