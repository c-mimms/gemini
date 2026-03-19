# Project 8: The City of Glass

## Pillar
Fiction / Entertainment / Worldbuilding

## The Core Concept
A persistent, real-time procedural noir simulation set in a sprawling, generated cyberpunk metropolis. The output artifact is a daily serialized "Private Eye Case File," a gritty narrative newsletter detailing the protagonist's investigations. Under the hood, the system simulates a massive clockwork cast of criminal syndicates, corrupt politicians, and desperate citizens who form alliances, commit crimes, and leave behind evidence trails based on hidden, evolving agendas.

## Why it Needs Iterative State
A compelling, multi-month mystery requires strict narrative continuity and severe consequences for the protagonist. The system maintains the exact state of the city as a database: who currently controls the docks, who holds a grudge, and what evidence is currently sitting in a locker. If the Detective fails to save an informant on Day 5, that NPC is permanently marked as "deceased" in the state, altering the available clues and political balance of power for Day 30.

## The Engine of Conflict/Discovery
The friction is driven by an asymmetric knowledge gap. A "Sim-Master" agent quietly mutates the City State every cycle (e.g., executing a random gang hit, forging a blackmail document) based on NPC motivations, completely hiding this reality from the "Detective" agent. The Detective must then iteratively query the updated state (investigating "crime scenes" or interrogating NPCs) to deduce what happened. The constant, organic divergence between the city's hidden truth and the Detective's attempts to uncover it guarantees the narrative never stalls.
