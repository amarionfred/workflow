---
name: authored-mystery
description: Structure a character-led mystery around an existing map, including clue dependencies, dialogue state, branching discovery, and persistent progression.
---

Distinguish the sequence of truths from the sequence of rooms. Write the central mystery, protagonist's motive, opposing interpretations, and what each major revelation changes before scripting quests.

Create a clue graph with stable IDs. Each clue records location, prerequisites, information conveyed, alternate access, journal consequence, and recovery if missed. Essential understanding should not depend on one unmarked object or on hearing one interruptible line. Optional clues should enrich interpretation or choices rather than secretly block completion.

Keep authored beats compatible with exploration order. Track knowledge separately from physical inventory and mission completion. Dialogue conditions need speaker availability, priority, interruption/resume behavior, cooldown, and whether a line can repeat. Test returning after leaving mid-conversation.

For extraction, decide what persists after success, death, disconnection, and replay. Tie a run to a concrete new discovery or relationship change. Repeated exposition and indefinitely resetting character decisions undermine authored progression. Do not add a loot economy unless it serves the chosen experience.

Use a beat table: place, player action, uncertainty, reveal, emotional turn, and next choice. Revisit spaces only when access, danger, information, or interpretation meaningfully changes. Duration is an outcome of tested content, not a reason to add errands.

Deliver the dependency graph, one playable mystery sequence, dialogue conditions, and a save/recovery matrix. Mark unapproved plot inventions as proposals.

Reference: [Frictional's horror lessons](https://frictionalgames.com/2019-10-9-years-9-lessons-on-horror/), particularly context, player expectations, and the interaction of reward with fear.
