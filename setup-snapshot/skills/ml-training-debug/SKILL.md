---
name: ml-training-debug
description: "Implement or diagnose ML training and adaptation, including tensor shapes, autograd, losses, optimization, LoRA, quantization, distillation, and checkpoint recovery. Use after model/data choices are approved, or for scoped teaching examples."
---

# ML training and debugging

First identify the approved upstream model/revision, tokenizer, data split, objective, trainable parameters, software versions, and resource budget. If choices are pending, inspect requirements and prepare options without choosing them by example code. Check installed-version documentation before changing training APIs.

## Make one update understandable

Trace one permitted example through tokenization/features, batch construction, forward pass, target alignment, loss reduction, backward pass, optimizer step, and checkpoint. Write the important tensor shapes, dtypes, devices, padding/attention masks, and effective number of supervised tokens. Check that truncation retains the answer and loss masking excludes padding and any unsupervised prompt tokens.

Verify finite loss/gradients and intended parameter changes. Inspect trainable counts, optimizer membership, gradient accumulation/scaling, clipping order, scheduler cadence, train/eval mode, and random-state handling. A tiny training-only overfit check diagnoses wiring; it never demonstrates held-out quality. Distinguish a disconnected graph from expected zero gradients under a particular initialization.

## Adaptation choices

LoRA changes the parameterization of updates; distillation changes the source or form of training targets. Report them as separate factors. Record target modules, rank, scaling, dropout, initialization, frozen parameters, precision/quantization, and tokenizer/template compatibility. Validate that adapter disabling recovers the declared baseline and that saving/loading preserves outputs within a stated numerical tolerance.

In logit distillation, check distribution direction, temperature, weighting, masking, and vocabulary alignment. In sequence distillation, record teacher/revision, decoding, rejection/verification process, and information available to the teacher. Do not use future fixes or held-out grading artifacts to generate targets.

## Diagnose with evidence

Use the [diagnostic reference](references/diagnostics.md) for symptoms and discriminating checks. Change one explanatory factor where feasible; log unsuccessful attempts. Loss reduction is an optimization observation, not proof of task improvement.

Before scaling, measure actual memory/time on the approved environment. Include base weights, optimizer state, gradients, activations, temporary buffers, and checkpoint storage. Parameter count alone is insufficient. Mixed precision, activation checkpointing, batching, quantization, or distributed execution require correctness checks; distribution is justified by a measured need, not library availability.

Save enough state to resume: model/adapter, optimizer, scheduler, precision scaler where used, RNG, data/sampler position, configuration, code and data identities. Do not claim bitwise reproducibility across platforms simply because a seed is fixed.

Deliver a reproducible command/config, raw logs, a diagnosed or unresolved cause, and the next minimal check. Interpret performance with [experiment review](../ml-experiment-review/SKILL.md).

Primary starting points: [PyTorch reproducibility](https://docs.pytorch.org/docs/stable/notes/randomness.html), [PEFT LoRA](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora). Resolve documentation to the installed version before execution.
