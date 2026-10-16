---
name: horror-encounters
description: Build and evaluate horror encounter pacing, readable AI behavior, and constrained replay variation in an existing Roblox level.
---

First draw the actual movement graph: entrances, loops, shortcuts, dead ends, vertical links, safe spaces, and long sightlines. A roof plan is insufficient. Walk representative routes with the final player dimensions and collision.

Describe each threat's player-readable rules: detection, warning, pursuit, search, disengagement, and counterplay. Separate sensing from omniscient world state. Log AI transitions with reasons and investigate stuck cases at doors and stairs.

Author legal encounter slots with approach routes, visibility exclusions, retreat options, and narrative conditions. Select among them within constraints. Never spawn a visible threat directly into a player's view merely because a timer elapsed. Avoid sealing every escape unless the scene intentionally teaches a different solution.

Track recent pressure through observable events and use it to space encounters. Keep time for anticipation, a peak, aftermath, and investigation. Test silence as a deliberate beat. Do not copy Left 4 Dead's numerical timings into a mystery game or conflate pacing adjustments with hidden difficulty changes.

Replay variation should change decisions: access, patrol paths, a scarce resource location, or an optional objective. Randomizing every clue weakens authored inference. Record the seed and state for reproducing failures.

Deliver route captures, an encounter sheet, AI state logs, and a playtest question that can disprove the intended effect.

Reference: [Valve, The AI Systems of Left 4 Dead](https://cdn.fastly.steamstatic.com/apps/valve/2009/ai_systems_of_l4d_mike_booth.pdf), especially sensed knowledge, authored candidate locations, and intensity pacing.
