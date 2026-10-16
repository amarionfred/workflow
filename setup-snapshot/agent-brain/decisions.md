# Setup decisions

## 2026-10-16

- Keep the existing Codex 0.154.0 + Orator binary. Its `/record` workflow remains the native speech input path.
- Install the full public pstack snapshot as a local Codex plugin; retain upstream MIT attribution and source hashes. Private company tooling is not claimed as available.
- Inherit the current Codex model for pstack roles. Introducing Grok/Claude accounts is unnecessary to implement the methods.
- Use a local Markdown index that points to project records. Do not migrate or duplicate existing research notebooks.
- Apply the user's requested `approval_policy = "never"` and `sandbox_mode = "danger-full-access"` to future Codex sessions. Backup: `/home/park/.codex/backups/agentic-workflow-20261016T025917Z/config.toml`.
- Give Empryo a Koda theme, project picker, and Super+A binding. It is a separate harness and needs its own provider sign-in; Codex credentials are not copied into it.
- Keep recurring health checks deterministic and local. Model-consuming or externally mutating routines need a concrete task and runtime, not just a calendar entry.
# 2026-10-16 runtime decisions

- Park selected the existing ChatGPT/Codex subscription for Empryo. A bounded coding task completed through `subscriptions/gpt-5.6-terra`; its token-cost estimate is not recorded as actual spending.
- Use rootless Docker for Scientist, with a dedicated checked UID adapter in `Projects/agentic-workflow/tools/scientist-bin/docker`. Keep the upstream checkout unchanged. Host bind-mount ownership was tested directly.
- Daily health and weekly reviewed-receipt summaries use systemd user timers. They perform deterministic local work without model calls. Substantive project tasks still need a scoped brief and resource bounds.
- Keep Bun and pstack's locked helper dependencies local. Preserve the installed Orator Codex binary and its voice integration.
