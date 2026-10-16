---
name: spatial-horror-audio
description: Design, implement, and evaluate spatial sound, dialogue intelligibility, surface Foley, and tension mixing in a Roblox horror level.
---

Map acoustics to actual spaces: open coast, yard, small room, large cell hall, stairwell, and adjoining doorway. Begin with a small palette of room responses and transitions; validate current Roblox audio APIs before choosing the implementation.

Separate ambience, navigational cues, threat cues, dialogue, player Foley, and impact sounds. For each cue record source location, attenuation, obstruction behavior, priority, repetition limits, and narrative meaning. Essential clues need a visual or journal fallback.

Compare the same source inside, outside, behind a wall, above, below, and through an open door. Test transitions while moving, overlapping sources, and the player's ability to locate the source. A louder sound is not automatically more convincing. Maintain dialogue intelligibility during action and preserve useful contrast between quiet and loud moments without requiring excessive listening volume.

Footsteps should respond to the relevant surface and movement state, with controlled variation and no obvious machine-gun repetition. Synchronize handling Foley to animation markers and ensure interruption stops obsolete sounds.

Treat bodycam microphone coloration as optional presentation. Wind, muffling, and handling noise must not erase cues or make every surface sound alike. Verify in stereo headphones and ordinary speakers, and with relevant accessibility settings.

Deliver a cue sheet, original/licensed source register, in-engine A/B capture, and listening notes. Captions and waveform measurements are not proof that the mix sounds good.

Reference: [Bodycam sound developer diary](https://www.youtube.com/watch?v=Oz66Ek1RYWU). Use its environmental distinctions as design references, not claims that Roblox has the same propagation system.
