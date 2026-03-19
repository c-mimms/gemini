# Project 4: The Daily Procedural (Living Newspaper)

## Concept
An algorithmic local newspaper for a simulated fictional town. Each run generates a daily edition containing a front-page story, local politics, weird classifieds, and a weather report. Over time, recurring characters (the mayor, local business owners, eccentric townspeople) develop lives and interact.

## How it's deeper than the Museum Task
It requires simulating multiple independent actors and ongoing background events. A pothole reported on Monday might become a sinkhole by Thursday, and a major political scandal by next month.

## Context Management Strategy: "Story Arcs" and "Character Cards"
We avoid feeding previous newspaper text back into the system. Instead we use discrete state tracking:
1. **Active Story Arcs:** A JSON file maintains a list of 5-10 "Active Arcs". An arc has a title, characters involved, current tension level (1-10), and a 2-sentence summary of the latest development.
2. **Selection & Advancement:** When generating a daily paper, the main script randomly selects 2-3 Active Arcs to progress. It feeds only those specific arc summaries to the agent, instructing it to write articles advancing those plots, and maybe resolve one if tension is high.
3. **Character Roster:** A database of active townspeople. If an agent wants to quote someone, it queries the roster for an appropriate persona, ensuring the "Mayor" always sounds like the Mayor. Output extraction scripts update Character states (e.g., changing their job or status) based on the generated article.
