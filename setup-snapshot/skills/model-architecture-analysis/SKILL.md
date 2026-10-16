---
name: model-architecture-analysis
description: "Analyze or propose neural architectures through equations, tensor/state flow, complexity, measurable mechanisms, and controlled ablations. Use for attention, recurrent/state-space memory, MoE, representation analysis, and architecture-versus-training claims."
---

# Model architecture analysis

Classify the intervention before naming a contribution: computational architecture, trainable-parameter scheme, objective/data, retrieval, inference/search, or systems optimization. Adapting an existing architecture with LoRA is not by itself a new architecture.

Start from the approved baseline or a clearly labeled analytical example. Describe the information flow with shapes and a forward equation, identifying learned parameters, persistent state, external memory, and what changes between training and inference. Use [mechanism checks](references/mechanisms.md) for attention, recurrence, routing, and representation claims.

Ask what failure the mechanism predicts and what result would falsify that explanation. Compare a simpler control that addresses the same failure. Hold data, training tokens/updates, parameter or compute budget, tuning effort, context, tools, and inference attempts as comparable as the question permits. When multiple quantities cannot be matched, state which estimand each comparison addresses.

Report training versus inference compute separately. Distinguish parameter memory, KV/state memory, activation memory, prefill, decoding, batch size, and hardware utilization. Asymptotic complexity is not measured speed. A paper's throughput on another device does not predict ours without profiling.

Require code-level invariants appropriate to the mechanism: shapes, causal masking/no future-token access, state reset, padding behavior, gradient flow, and equivalent incremental versus full-sequence computation when expected. Begin with a minimal mathematical or local implementation check; do not initiate a new training study without its phase approval.

For interpretability, separate correlation, a probe's predictive performance, and a causal intervention. Check whether an ablation damages general computation or introduces out-of-distribution states before attributing a specific concept to a component.

Return a mechanism diagram/equation, predicted tradeoffs, closest prior work, controlled test, feasibility, and claim limits. A repair-score gain alone cannot establish the proposed internal mechanism or architectural novelty.

Public example for mechanism analysis, not a model recommendation: [Griffin](https://arxiv.org/abs/2402.19427) and its [RecurrentGemma implementation](https://github.com/google-deepmind/recurrentgemma). Read the actual methods before applying them.
