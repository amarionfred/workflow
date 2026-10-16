---
name: ml-experiment-review
description: "Design and assess controlled ML experiments with leakage checks, paired outcomes, uncertainty, resource accounting, and claim review. Use before substantive runs and when interpreting positive, negative, failed, or incomplete results."
---

# ML experiment design and review

Recover the registered question and design before reading the headline score. Define the estimand in plain language: what difference, in which population, under which budget. Distinguish a hardware/tool check from a model-performance experiment.

## Before execution

Record the hypothesis, counter-evidence, experimental unit, sampling/admission criteria, splits, baseline, treatment, primary metric, failure accounting, seed/replication plan, tuning budget, stopping rule, and raw artifact locations. Freeze final evaluation after validation development. Repeated testing on the final set changes the claim; record exploratory follow-ups explicitly.

Ensure training, retrieval, teacher generation, developer feedback, and candidate inference obey the same information boundary. A grader may know the reference answer; a purportedly blind generator may not. Separate processes on shared storage are insufficient evidence of isolation. Inspect the actual mounted/exported files and history.

## After execution

Report raw numerator/denominator and per-item outcomes before aggregates. For matched tasks, report paired wins/losses/ties and regressions. Identify the independent unit: tasks from the same project and repeated seeds on the same task are not automatically independent samples. Use uncertainty methods appropriate to the design, preserving pairing and clustering. With very few projects/seeds, describe interval instability and limited generalization rather than presenting artificial precision.

Keep model failures and infrastructure failures visible. Preserve the original attempt when rerunning a verified infrastructure failure under the declared policy. Do not replace missing measurements with zeros or favorable estimates.

Record total resource use: data preparation and verification, teacher generation, training/tuning including failed runs, evaluation/inference, storage, and human effort. Distinguish elapsed time from device time; unlike GPU hours are not equivalent work. Report gross provider cost, credits consumed, and cash charged separately.

For Game Model Research, complete every factor in the project's `01 Research/Result Assessment.md`: training beyond matched retrieval; data effectiveness; change/retention; projects/engines; total resources; implications for method/architecture. Use Measured, Inconclusive, Not measured, or Not applicable with a reason. A setup check has no adaptation measurement.

Review the strongest competing explanation and the narrowest defensible claim. Static later-task evaluation does not measure forgetting after sequential updates. More repaired bugs do not prove a mechanism, a new architecture, or cross-domain generality.

Deliver claim → evidence → uncertainty → limitation → next discriminating comparison. Read [review cases](references/review-cases.md) for subtle confounds. The [statistical-precipice paper](https://arxiv.org/abs/2108.13264) and [rliable](https://github.com/google-research/rliable) are methodological references; do not transplant an RL aggregate or interval procedure without checking its applicability.
