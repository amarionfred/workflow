---
name: agentic-scientist
description: Configure, inspect, or run the installed Sakana AI Scientist v3 pipeline for a scoped research question, using controlled baselines, ablations, sealed evaluation, and traceable artifacts.
---

The pinned checkout is `/home/park/Projects/agentic-workflow/vendor/AI-Scientist-v3`. Read its `README.md` and the relevant pipeline documentation before version-sensitive commands. `agent-scientist doctor` checks the CPU circle-packing setup with Codex; `agent-scientist preview` prints the six-phase plan without launching agents. `agent-scientist run TASK [overrides]` defaults to Codex/Astra and no API env file; explicit overrides win. Other commands pass to upstream.

The wrapper uses a dedicated rootless-Docker adapter in the workflow project's `tools/scientist-bin/docker`. It maps the upstream explicit host UID/GID to container `0:0`, which maps back to Park on the host; it always selects the rootless context and removes endpoint overrides. Read the runtime verification evidence before claiming full pipeline compatibility. Do not point this adapter at a root daemon or relax upstream isolation to work around a failure.

Before a substantive experiment, read the project's AGENTS.md and canonical research record, then use the installed `ml-experiment-review` and `research-expedition` skills as appropriate. Recover the hypothesis, dataset split, metric, baseline, compute budget, and decision criterion. Existing approvals remain valid; installation alone is not approval for an unbounded research campaign.

Verify the intended runtime. The upstream default uses Docker and a pinned agent image. The original machine inspection found no Docker and very little home-disk space; check current state rather than treating that as permanent. A native fallback changes isolation and cannot support claims of a sealed evaluation unless the evaluator enforces it independently. Do not silently disable stages, isolation, or hard checks to make a run pass.

Keep candidate construction away from held-out answers. Bind each result to the code revision, configuration, seeds, raw outputs, and resource measurements. Compare baselines and ablations under matched conditions. A paper being generated or a reviewer agreeing is not evidence that a mechanism works. Treat failures and negative results as findings, and moderate claims to the actual evidence.

Resume the recorded run directory and verify live process/job handles before restarting. Distill validated conclusions into the project record; preserve raw evidence and failed hypotheses. Optional AutoIllustrate produces editable figures and needs its own runtime and model connection. Do not claim it is installed merely because its name appears in the paper stage.
