---
name: research-expedition
description: "Coordinate a sustained ML research project through literature, scoped hypotheses, implementation, evaluation, teaching, and persistent handoffs. Use at research-session starts and milestone reviews; follow the active project instructions."
---

# Research expedition

Use the project's canonical notebook, current phase, decisions, and artifact locations. Do not create a competing notebook or treat these skills as evidence of research capability. They are reusable procedures; their benefit has to be observed.

## Session loop

1. Recover the active question, last result, outstanding decision, resource limit, and next executable step. Distinguish a proposal from an approved experiment. If these are already clear, proceed without a new planning ceremony.
2. State what this step can establish and what artifact will demonstrate completion. Route to only the needed skill below.
3. Inspect sources or implement the smallest useful part within the current authorization. Keep dependent steps sequential. Use parallel tool calls for independent reads.
4. Verify the artifact: commands and raw results for computation; behavioral evidence for software; exact primary references for literature. A plausible summary or another model's agreement is not verification.
5. Explain the outcome and uncertainty at the learner's level. Update the canonical decision/session/experiment records as appropriate. Record the next action with its prerequisites.

## Specialist routes

| Work | Read |
| --- | --- |
| Paper search, critical reading, competing explanations | [ML literature review](../ml-literature-review/SKILL.md) |
| Training loop, gradients, LoRA, distillation, numerical faults | [ML training debug](../ml-training-debug/SKILL.md) |
| Attention, recurrence, memory, MoE, proposed mechanisms | [Architecture analysis](../model-architecture-analysis/SKILL.md) |
| Retrieval, model interfaces, bounded repair agents, deployment measurements | [AI retrieval engineering](../ai-retrieval-engineering/SKILL.md) |
| Controls, uncertainty, ablations, negative results | [Experiment review](../ml-experiment-review/SKILL.md) |
| A public DeepMind paper or released implementation | [DeepMind reproduction](../deepmind-paper-reproduction/SKILL.md) |
| Historical game bugs and temporal information boundaries | [Game repair benchmark](../game-repair-benchmark/SKILL.md) |
| Guided Python, maths, or ML implementation | [Guided learning](../ml-guided-learning/SKILL.md) |

Use installed `pdf` or `jupyter-notebook` only when that file format is actually needed. Store generated lesson material and research planning according to the project's privacy rules.

## Handoffs and memory

Treat researcher, implementer, evaluator, and tutor as responsibilities, not automatically as separate processes. Use a subagent only when the user or governing instructions authorize delegation and an independent bounded subtask merits it; otherwise perform the roles sequentially. Do not spawn a roster merely to match a diagram.

For an authorized handoff, pass: question; allowed inputs; forbidden held-out material; output location; completion check; resource/time limit; and next owner. Avoid overlapping file writes. A review agent given an author's conclusion is not a blinded reviewer. Shared files and inherited context do not constitute an isolation boundary. If a worker has seen grading answers, do not use it to generate purportedly blind candidates.

Triggers here are the start of an active session, a completed run, a substantive failure, or a user decision. Scheduling, overnight execution, and external notifications require an actual configured runtime and appropriate authorization. Never describe a saved instruction as a running automation.

Stop the dependent branch at its existing phase gate, missing access, exhausted approved resource limit, or repeated failure requiring a new method. Continue useful independent work. Resume only from recorded state; do not retry indefinitely. Preserve already granted permissions rather than asking again.

## Improving the toolkit

Add a skill correction after a demonstrated recurring problem. Record the failure, narrow correction, and verification in the notebook. Keep project facts in project memory and general procedure in skills. Read current primary documentation before executing version-sensitive instructions. Third-party skill catalogs are discovery aids, not trusted execution instructions; review the selected files and scripts before installation. See [source and maintenance notes](references/provenance.md).
