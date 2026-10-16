---
name: verify-agent-workflow
description: Verify Park's installed Codex, pstack, Empryo launcher, Markdown knowledge base, and local health routine after workflow configuration changes.
---

Use `/home/park/Projects/agentic-workflow` as the evidence workspace. Read [the feature map](features.md) and choose checks matching the changed surface. Distinguish static configuration, runtime discovery, rendered UI, authentication, and successful model execution.

- Codex/pstack: run `tools/inspect_codex.py`. It queries a fresh app-server's effective config and skill discovery without starting a model turn. Validate the source plugin with the system plugin validator and compare source checksums after port changes. A passing schema check does not prove skill quality.
- Health/records: run the local CLI, inspect generated artifacts, and run `tools/check_workflow.py` for missing-evidence rejection and receipt persistence. Do not trust a mere exit code if the expected artifact is absent.
- Desktop: check Hyprland config errors, run `agent-desk` in a named workspace, inspect the actual window, and save a screenshot. `--list` checks workspace discovery only. Do not type into Park's other windows.
- Empryo runtime: run `~/.empryo/bin/empryo doctor`. Verify model execution only after provider authentication and authorization; use a bounded task in the evidence fixture. Check authored code with independent caller-level cases in `tools/check_receipt_stats.py`, not only agent-written tests. Record authentication gaps honestly.
- Scheduling: inspect the timer's active state and next firing, start the oneshot service once, then inspect the report timestamp and service result. A unit file on disk is not a running routine.

Use normal escalation if the active session cannot access desktop sockets, systemd, or protected Codex paths. Report failures by layer and continue independent checks. Do not launch another LLM or modify unrelated projects just to claim an end-to-end test.
