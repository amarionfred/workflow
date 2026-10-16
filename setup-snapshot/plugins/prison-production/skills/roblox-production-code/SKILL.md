---
name: roblox-production-code
description: Implement maintainable Roblox game systems with explicit state ownership, validated client requests, persistence recovery, and reproducible Studio verification.
---

Read the project's current architecture and ownership rules before editing. Verify Studio identity and Edit/Client/Server context. Use the connected official MCP documentation and debugging capabilities when needed; a configured server is not proof of a live connection.

Keep camera and presentation on the client. The server owns consequential shared outcomes, such as damage, inventory, mission completion, and rewards. Validate request type, bounds, permissions, current state, and rate. Never accept a client's claimed hit or reward amount as truth. Evaluate network ownership when physical objects affect gameplay.

Use stable IDs and explicit transitions for mission, interaction, weapon, and dialogue states. Make cleanup cover completion, cancellation, death, respawn, and player departure. Avoid hidden cross-system dependencies on hierarchy names where a declared interface is clearer.

For saves, define schema version, migration, retry behavior, conflict/session handling, and idempotent reward grants before integrating progression. Verify failure paths in an isolated test environment rather than risking real player records.

Use typed Luau where it clarifies contracts. Formatter/linter output supplements runtime evidence. Choose dependencies for a concrete need, inspect their license and update history, and pin versions. Don't install overlapping frameworks just to expand the toolkit.

Deliver the behavior change, relevant automated or manual verification, known limitations, and a reproducible Studio test. Keep filesystem code and Studio assets under a documented synchronization rule.

References: [Roblox client/server security](https://create.roblox.com/docs/scripting/security/client-server-boundary), [official Studio MCP](https://create.roblox.com/docs/studio/mcp), [Rojo](https://rojo.space/docs/).
