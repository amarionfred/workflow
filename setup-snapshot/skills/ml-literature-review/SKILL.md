---
name: ml-literature-review
description: "Find and critically read primary ML papers and official code, map prior work, and turn a specific claim into a feasible experiment. Use for literature reviews, novelty checks, and paper-to-code questions."
---

# ML literature review

Begin with the project's question and the decision the reading should inform. Search by mechanism and task, including earlier baselines and contrary findings. A lab name or citation count is not a selection criterion by itself.

Use [science-search](../science-search/SKILL.md) for ScienceMadeReadable semantic and keyword discovery, related papers, and citation walks. Supplement it with primary sources for recent or missing work; verify methods and results in the paper or official code.

For each material paper, record the exact title, authors, version/date, primary URL, official code URL/revision if found, and reading depth: abstract only, selected sections, full methods, or inspected implementation. Do not equate an abstract read with a methods review. Verify bibliographic details before emitting a citation.

Extract the proposed mechanism, supervision, data boundaries, objective, baseline, budget, metric, experimental unit, uncertainty, and limitations. Read the appendix and relevant implementation when the claim depends on a detail missing from the main text. Identify which numerical result belongs to which setting; do not transfer headline results to the current project.

For a novelty check, compare the closest methods on the actual claimed difference: architecture, objective, data recipe, retrieval policy, evaluation setting, or system integration. Search for the same mechanism under different terminology. A missing search result is not proof of novelty.

End with a short claim/evidence/gap table and the smallest comparison that could distinguish the hypothesis from a simpler explanation. Separate the authors' claims, your inference, and what the project has measured. Mark unavailable details instead of inventing them.

Reading does not adopt a model, dataset, teacher, or experiment. Bring a concrete recommendation to the project's existing decision gate, including license/access and full resource needs. A reduced-scale demonstration must be labeled as such.

For public DeepMind methods use [the reproduction skill](../deepmind-paper-reproduction/SKILL.md). For experimental controls and inference use [experiment review](../ml-experiment-review/SKILL.md).
