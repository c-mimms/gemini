# Project 2: Alternate Tech Tree Simulator

## Concept
A chronologically advancing simulation of technological progression. The agent generates product launch press releases, retrospective reviews, or standard "Wikipedia-style" pages for an alternate timeline of computing (e.g., "What if analog computing remained dominant?"). The site updates "year by year".

## How it's deeper than the Museum Task
The Museum Task picks random objects from history. This project simulates a causal, forward-moving timeline. A breakthrough in "vacuum tube miniaturization" in year 3 must logically lead to "portable analog calculators" in year 4. 

## Context Management Strategy: The "Active Tech Tree" State
To maintain consistency without polluting context:
1. **The Technology Tree Data Structure:** We maintain a JSON file representing a tech tree. It tracks nodes like "Discovered", "Theorized", "Commercialized", and "Obsolete".
2. **Current Year Horizon:** The agent is only ever aware of the "Current Year" and a summarized list of "Currently Active Technologies" and "Recent Breakthroughs". 
3. **Pruning Context:** We drop older technologies from the prompt once they become obsolete or ubiquitous, replacing them with broad overarching assumptions ("It is known that cheap analog chips are everywhere").
4. **Action Space:** The agent isn't just generating text; it's selecting a "move" based on the current state (e.g., "Combine Tech A and Tech B to create an invention", "Iterate on Tech C", or "Introduce a market failure"). The output updates the JSON state for the next run.
