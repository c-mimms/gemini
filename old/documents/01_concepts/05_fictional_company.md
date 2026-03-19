# Project 5: The Evolving Fictional Company / Codebase

## Concept
A simulation of a tech startup or open-source project over several years. The site generated isn't just articles, but a mixture of "Internal Slack/Email leaks", "Git Commit summaries", "Post-Mortems", and "API Documentation" that evolves as the company pivots, grows, and eventually fails or IPOs.

## How it's deeper than the Museum Task
Instead of prose, the agent is generating interconnected multi-format corporate artifacts. An outage report references a commit that references an arrogant email from the CEO.

## Context Management Strategy: "Architecture as State" 
The context is managed primarily by treating the project like actual software:
1. **The Architecture Map:** A highly compressed representation of the company's "Product" (e.g., a diagram or YAML file of microservices).
2. **Issue Tracker as Prompt Queue:** The system maintains a backlog of "Issues" (e.g., "Database scaling problem", "CEO demands pivot to AI"). The agent picks an issue.
3. **State Mutation:** To resolve the issue, the agent generates a set of artifacts (an email chain, a technical spec). Crucially, it must also output a structured `diff` or update to the Architecture Map. 
4. **Context Window:** The agent only sees the current Architecture Map (which guarantees technical consistency), the specific Issue it is tackling, and a short list of "Key Personnel" traits. It never needs to see older emails, it just needs to know the DB used to be Postgres and is now MongoDB based on the Architecture map.
