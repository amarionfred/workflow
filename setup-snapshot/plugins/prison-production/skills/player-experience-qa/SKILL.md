---
name: player-experience-qa
description: Evaluate Roblox gameplay, UI, comfort, accessibility, performance, and narrative recovery with device-specific evidence and unbiased playtests.
---

Choose a hypothesis for each test: finding the first objective, understanding a clue, identifying a threat, completing a reload, recovering a save, or maintaining a frame-time target. Specify observable success and what evidence would falsify it.

Keep first-time playtests free of coaching. Note hesitation, wrong turns, repeated actions, and misunderstood feedback before asking for opinions. Separate an observed event from an inferred cause. Aggregate numbers must remain traceable to individual sessions.

Select the device/input tiers and quality settings explicitly. Record client and server frame time, spikes, memory growth, load/streaming delay, and session length on representative routes. A screenshot or Studio emulator is not evidence of actual low-end device performance. Profile a bottleneck before optimizing it, then repeat the affected measurement.

Review UI text size, contrast, focus order, controller navigation, touch targets, subtitle speaker identification, camera comfort, and hold/toggle settings. Diegetic menus still need to be readable and operable. Minecraft-built menu geometry does not replace Roblox input and settings logic.

Exercise death, restart, skip, disconnection, rejoin, missing assets, and an interrupted objective. For multiplayer, add latency and conflicting actions. Keep release blockers distinct from cosmetic polish.

Deliver a short finding log with build/device, steps, expected/actual outcome, capture, severity, and retest result. Don't claim automated visual quality from linting.

References: [Valve's playtesting approach](https://cdn.fastly.steamstatic.com/apps/valve/2009/GDC2009_ValvesApproachToPlaytesting.pdf), [Roblox performance design](https://create.roblox.com/docs/performance-optimization/design).
