---
name: voxel-transfer
description: Convert an existing Minecraft Java build into staged Roblox environment assets while preserving the source, block shapes, scale, and gameplay clearances.
---

Work from the project's source manifest and a separate snapshot. Do not substitute a historical reconstruction or silently regenerate the user's finished map.

Begin with one representative room, its doorway, a stair, glass, foliage, and an exterior wall. Record Minecraft version, block states, exporter version, coordinate transform, and scale. Export block geometry, not screenshots. A block-name-only reader is insufficient for stair orientation, slab halves, fences, and waterlogging. Keep the special-block fallback list visible.

Use Mineways or an inspected equivalent to establish a reference export; use Blender for cleanup and batch processing. Partition by playable spaces and visibility, not one giant island mesh. Separate static visible geometry, collision, doors, interactables, and distant scenery. Remove enclosed faces without deleting surfaces visible through doors or windows. Preserve consistent texture scale across partition seams.

Compare source and Studio from matching viewpoints. Verify normals, UVs, material assignment, door and stair clearance, floor contact, collision at seams, streaming arrival, and distant silhouettes. Measure actual instances, triangles, texture memory, and frame time before scaling up. Do not invent universal asset budgets before selecting target devices.

Minecraft resource packs, shaders, entities, settings menus, and redstone behavior do not become Roblox systems through mesh export. Rebuild interactions and UI deliberately.

Deliver a repeatable export command, transform manifest, source hashes, unsupported-block report, and before/after captures.

References: [Mineways export and scripting](https://erich.realtimerendering.com/minecraft/public/mineways/mineways.html), [Roblox performance design](https://create.roblox.com/docs/performance-optimization/design). Recheck importer limits when performing an actual import.
