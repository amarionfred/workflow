---
name: grounded-art
description: Establish and review consistent realistic materials, lighting, environmental wear, and voxel silhouettes for a Roblox horror scene.
---

Build a material and lighting reference scene before dressing an entire map. Use an exterior, a window-lit room, and a flashlight-lit corridor from the actual game. Lock comparison cameras and record graphics settings.

Define the visual contract: voxel architecture scale, allowed small prop geometry, character proportions, texture density, and the intended level of camera distortion. Scan detail is useful only when it agrees with that contract. Judge silhouettes at normal play distance before texture resolution.

Use plausible albedo and material response across all three scenes. Separate color from roughness, metalness, normal, and emissive behavior; check current Roblox support. Normal maps do not change silhouettes. Avoid fixing one lighting condition with painted highlights in the base color. Dirt follows causes: leaks below openings, contact wear on handles, dust in sheltered recesses, debris near damage. Do not distribute grunge uniformly.

Set motivated light sources and a readable focal hierarchy. Test clues and enemy silhouettes with post effects disabled, at lower graphics quality, and while moving. Compare the cost of each added light or transparent layer. High-detail foliage and many unique materials need measured budgets.

For every external asset, retain origin, license, local filename, intended use, modifications, and import identifier. A reference video's resource pack is not permission to redistribute its textures.

Deliver a small approved palette, matching-view captures, cost measurements, and explicit exceptions to the style contract.

References: [Roblox PBR textures](https://create.roblox.com/docs/art/modeling/surface-appearance), [Guerrilla image-quality presentation](https://www.guerrilla-games.com/media/News/Files/GDC2014_Valient_Killzone_Graphics.pdf). Transfer the review method; renderer implementations differ.
