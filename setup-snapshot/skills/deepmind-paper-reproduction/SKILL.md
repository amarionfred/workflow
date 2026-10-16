---
name: deepmind-paper-reproduction
description: "Critically investigate and reproduce a scoped mechanism from public Google DeepMind research using the paper, released code, and explicit fidelity checks. Use for DeepMind-related papers, RL/planning methods, recurrent models, and compute-scaling analysis."
---

# Public DeepMind paper reproduction

This skill provides a public-source workflow, not affiliation, private access, or demonstrated equivalence to a research lab. Start with the exact question or named paper. Use the [publications index](https://deepmind.google/research/publications/), the paper, and its author-linked implementation. Do not choose a model simply because DeepMind released it.

Read the methods relevant to the claim, appendices, experiment configuration, and implementation. Record provenance and reading depth. Separate what is actually released from a blog description; if weights, data, evaluator, or training details are unavailable, bound the reproduction accordingly.

Create a fidelity table: paper setting; available artifact; local setting; deviation; likely consequence. Choose one claim/mechanism and a feasible falsification check. A small demonstration is not reproduction of frontier-scale performance. Preserve the project's model, source, experiment, and spending gates.

## Choose the relevant branch

- **Architecture/memory:** inspect equations, state reset, causal computation, training versus incremental inference, precision, and sequence-length behavior. [Griffin](https://arxiv.org/abs/2402.19427) and [RecurrentGemma](https://github.com/google-deepmind/recurrentgemma) provide a public example; use the architecture skill for controls.
- **Reinforcement learning/planning:** identify observation/action space, reward and termination semantics, discount, replay/off-policy corrections, exploration, actor/learner versions, environment seeds, and test-time search budget. Check environment interaction cost and reward hacking separately from training loss. Inspect [Acme](https://github.com/google-deepmind/acme) or [dm_control](https://github.com/google-deepmind/dm_control) only when the paper uses them; their availability does not justify adding RL to another study.
- **Compute scaling:** distinguish training from scratch, continued pretraining, adaptation, and inference cost. Read the [Chinchilla paper](https://arxiv.org/abs/2203.15556) before using its setting. Do not apply a pretraining tokens-per-parameter heuristic as an established LoRA recipe or extrapolate far beyond measured scales without qualification.
- **World models/embodied agents:** separate predicting observations, choosing actions, planning, reward prediction, and downstream control. Check open-loop versus closed-loop evaluation, real versus simulated data, temporal leakage, environment resets, and distribution shift. Locate the specific primary paper before proposing a method; a convincing generated video is not control performance.

State what our project can learn from the result, what cannot transfer, and which controls would be needed. A game-playing result does not establish game-code repair ability. Broader reading can inform a proposal without expanding the current month's experiments.
