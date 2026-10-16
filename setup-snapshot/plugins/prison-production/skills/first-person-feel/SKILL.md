---
name: first-person-feel
description: Design and tune grounded first-person movement, camera, weapon presentation, and interaction feel in Roblox using observable tests.
---

Separate player intent, authoritative movement/combat state, camera presentation, and animation. A shaky view must not silently move the authoritative aim ray. Define how camera aim and muzzle obstruction interact, then make the feedback consistent.

Start with walking, turning, crouching, a doorway, a stair, and one interaction. Evaluate acceleration, stopping, eye height, wall clearance, camera clipping, and input response before recoil. Record the exact input sequence and resulting view so changes can be compared.

For bodycam influence, decompose the effect into bounded rotation lag, translation, gait response, lean, FOV, and impact impulses. Tune one component at a time. Use frame-rate-independent behavior and expose comfort options. Test low frame rates and mouse/controller input. Large random shake is not a substitute for weight.

For a first weapon, build a state table covering equip, ready, aim, fire, reload, interrupted reload, empty, and blocked muzzle. Specify when ammo changes and when the next action is allowed. Test interruption, death, and respawn cleanup. Keep client feedback responsive while validating gameplay outcomes on the server.

Reference real movement or the user's own safe demonstrations when animating. Begin with a small reliable motion set; stress variants are an optional expansion, not a starting requirement.

Deliver a tuning table, comparison clip, state diagram, and observed input/comfort problems.

Reference: [Bodycam animation developer diary](https://www.youtube.com/watch?v=6YUWQXv0MTk). Its custom Unreal rendering and physics are reference behavior, not Roblox features.
