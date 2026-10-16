---
name: cinematics-editing
description: Plan, stage, implement, and edit in-engine story scenes and honest gameplay trailers for a Roblox horror project.
---

Write what the audience must understand or feel in each shot. Plan screen direction, eyelines, geography, subject emphasis, and the transition back to player control. Use a timed animatic before polished animation or lighting.

Maintain a shot list with scene/shot IDs, duration, camera transform, lens or FOV, subject action, dialogue cue, lighting state, sound cue, and entry/exit conditions. Keep blocking readable without depth of field. Use restrained camera movement with a reason, particularly in first-person scenes.

For interactive scenes, specify start conditions, player position correction, permitted look/input, interruption, skip, replay, and recovery after disconnection. Skipping must produce the same durable story state as watching. A cutscene camera must reliably release control afterward.

Review each shot in the target engine and graphics tier. Measure the cost of visible characters, lights, shadows, and effects together. Shot-specific adjustments must restore prior gameplay settings on all exit paths.

For editing, preserve source footage and edit decisions. Keep clean dialogue, ambience, effects, and music stems where available; check sync, subtitle timing, peaks, black frames, and export dimensions. FFmpeg can create proxies/contact sheets and deterministic exports; use Blender's sequencer or an available editor for iterative timing.

Separate gameplay capture from concept renders in promotional work. Do not advertise an offline render as live Roblox performance.

References: [Naughty Dog cinematic process](https://www.naughtydog.com/blog/cinematic_process_in_the_last_of_us_gamescom_2012), [real-time cinematic cost and lighting](https://www.naughtydog.com/blog/naughty_dog_at_siggraph_asia_2020).
