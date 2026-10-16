---
name: game-repair-benchmark
description: "Qualify real historical game-code bug repairs and build reproducible behavioral evaluations with chronological splits and isolated grading. Use for Godot-first per-game adaptation benchmarks and later engine transfer checks."
---

# Historical game repair benchmark

Follow the project's source approvals. Screening a repository does not adopt its code, assets, dependencies, or data. Record each relevant license separately and inspect engine/version requirements, usable history, issue provenance, and reproducibility before proposing it.

For an admitted candidate, identify immutable buggy and fixed revisions; inspect whether the fix combines unrelated changes. Prefer the real contemporaneous bug report. If reconstructing a task description from a fix, label it, avoid prescribing the solution, and retain that provenance for selection-bias analysis.

Run the same independent behavioral check on both revisions under the pinned environment. It must detect the failure before the fix and intended behavior after it; require relevant previously working behaviors to remain working. Parsing/compiling is an intermediate check. If the failure is not reliably reproduced, mark the task unqualified rather than weakening the check until it passes.

Preserve commands, exit status, raw output, engine version/import behavior, seeds and resource hashes. For UI/physics/resource bugs, use observable engine state or recordings where needed; headless success may not cover rendered or timing behavior. [Godot CLI documentation](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html) must match the chosen engine version.

Split history before producing training examples. Record cutoff, related/duplicate fixes, validation tasks, final tasks, and exclusions. Track selected and rejected candidates with reasons. Future snapshots, git objects, reference patches, answer-derived prose, and final tests must not be available in training, retrieval, teacher generation, or inference context.

Maintain two views: an allowed buggy snapshot for candidate generation and a private evaluator containing grading artifacts. Export only permitted files; inspect file lists and mounts. A full clone with branches hidden still contains future git objects. Keep final grading feedback out of iterative candidate development. If strong isolation is not yet implemented, label the boundary as unverified and do not claim a blind evaluation.

Score behavior and regressions, not similarity to the reference diff. Keep patch application, build success, behavior resolution, regressions, and infrastructure errors as distinct outcomes. Record denominators and rerun policy before comparison.

A second engine requires its own approved source and qualified tasks. Shared harness code does not prove behavioral transfer. Output a concrete task record and admission decision; use [experiment review](../ml-experiment-review/SKILL.md) for the broader result assessment. [SWE-bench evaluation](https://www.swebench.com/SWE-bench/guides/evaluation/) is a reference for harness design, not automatic validation of a game benchmark.
