# Workflow repository

This repository preserves Park's workflow as configured on 2026-10-16. Its GitHub destination is the private repository `amarionfred/workflow`. The local workspace remains `/home/park/Projects/agentic-workflow` because launchers, skills, and knowledge pointers use that path.

| Location | Preserved content |
| --- | --- |
| `docs/`, `STATUS.md` | Operating guide, decisions, sources, verification results, and remaining limits |
| `tools/` | Configuration, pstack port, workflow reporting, runtime adapters, and executable checks |
| `research/`, `evidence/`, `verification/` | Source research, observed results, images, and verification fixtures |
| `setup-snapshot/plugins/` | Complete local pstack adaptation, Park Workflow plugin, and retained Prison Production skills, with their manifests and licenses |
| `setup-snapshot/skills/` | Retained personal research and utility skills, including supporting resources and licenses |
| `setup-snapshot/agent-brain/` | Knowledge index, preferences, lessons, project pointers, templates, and observed run receipts |
| `setup-snapshot/` | Launchers, theme, desktop entry, user service/timer units, instructions, marketplace, and selected nonsecret settings |
| `vendor/` | Unmodified public upstream repositories, pinned as Git submodules |

The knowledge snapshot contains pointers to other projects; their canonical research records and project files remain in those projects. `setup-snapshot/manifest.json` records the original path and SHA-256 of each copied or selected-settings file. The specialist research/game skills predate this setup and are included so their integration is preserved.

Clone with both pinned upstream sources:

```sh
git clone --recurse-submodules https://github.com/amarionfred/workflow.git
```

For an existing clone, use `git submodule update --init --recursive`. The pins are pstack's parent repository at `99743e9c151c8537cbbf1f98bb38f34ef3368453` and AI Scientist v3 at `2b8aa39285c35aaca3b0e06dd121061ef8a2d854`. Upstream licenses stay with those repositories; the pstack adaptation also retains its MIT license. This archive does not apply a new blanket license to third-party material.

Restoration is a reviewed setup operation. Place the workspace at its original path, or update absolute paths in the copied scripts, skills, units, and knowledge pointers. Restore plugin sources under `~/plugins`, personal skills under `~/.codex/skills`, and knowledge files under `~/Documents/agent-brain`. The marketplace snapshot belongs at `~/.agents/plugins/marketplace.json`; its paths also need adjustment on another account. Merge the selected Codex and Empryo settings into existing configuration, preserving provider and MCP settings. Restore launchers, the desktop entry, theme, and units to the source paths recorded in the manifest. The Super+A binding is documented in `tools/configure_empryo.py`.

Use the existing installation and verification procedures in [changes and operations](changes-and-operations.md) and the [verification skill](../setup-snapshot/plugins/park-workflow/skills/verify-agent-workflow/SKILL.md). Reinstall required runtimes and locked dependencies, then recheck the relevant behavior. No complete restore on a second machine is claimed. Preserve the existing Orator Codex binary when restoring on this machine.

Credentials, authentication files, provider session databases, private conversation logs, virtual environments, dependency downloads, binaries, and Docker images are excluded. Image identities and build inputs are recorded in the evidence; the image itself must be rebuilt. Authenticate through each provider's supported login flow.

To refresh the selected local snapshots from this machine:

```sh
python3 tools/snapshot_workflow.py
git diff --stat
git diff -- setup-snapshot
```

The snapshot tool copies files without changing installed sources. It does not delete archived files when a source is removed; review and remove stale entries deliberately. Review changes before committing, especially new knowledge receipts or settings. The existing runtime evidence is historical and does not assert that a process is still running.
