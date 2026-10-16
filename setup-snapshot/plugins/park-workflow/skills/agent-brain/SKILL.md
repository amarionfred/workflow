---
name: agent-brain
description: Retrieve or update Park's local Markdown knowledge base when resuming a project, recording a decision, preserving a correction, or handing work to another session.
---

Read `/home/park/Documents/agent-brain/AGENTS.md`, then only the relevant topic or project card. Follow the pointer to the project's canonical record before reporting current state. Use `rg` over filenames or a narrow topic when the index is insufficient.

Keep project results in the project; the personal card is a pointer and a compact handoff. Record the date, source or artifact, observed fact, unresolved question, and next action. Label proposals. Never infer that a process is running from a saved handle; query it. Keep secrets and unrelated private transcripts out of the archive.

For a recurring correction, choose its actual home: architecture/data model, executable check, tool, focused skill, or preference. Record the original failure and a check of the correction in `LEARNINGS.md`. Do not convert an isolated accident into a universal rule.

Use `agent-workflow record --help` for an observed run receipt and `agent-workflow health` for a local status snapshot. The receipt tool checks that evidence files exist; it does not decide whether a claim is true. Report the relevant file paths so Park can inspect or correct the record.
