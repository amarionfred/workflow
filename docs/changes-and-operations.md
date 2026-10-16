# Changes and operations

Installed and configured on 2026-10-16. See STATUS.md for current verification; this document explains the components and their boundaries.

| Component | Location and behavior |
| --- | --- |
| Codex defaults | `~/.codex/config.toml`: `approval_policy="never"`, `sandbox_mode="danger-full-access"`; existing `gpt-6-astra` and `xhigh` retained. A fresh ephemeral thread confirmed the actual full-access sandbox policy and no-approval setting without a model turn. The already-running session keeps its enforced permissions. |
| Personal instructions | `~/.codex/AGENTS.md`: retrieve relevant context, own authorized work through verification, teach when asked, correct recurring failures structurally. |
| pstack | `~/plugins/pstack`, installed through the personal marketplace. All 54 public core skills plus three Benny skills, 23 playbooks, reference material, scripts, and two agent templates preserved. Source revision and hashes are recorded. |
| Codex adaptation | `~/plugins/pstack/CODEX.md` translates Cursor tools, model routing, scheduling, skill invocation, and history access into actual Codex capabilities. Model roles inherit the parent; no fictional model diversity or cloud service is claimed. |
| Helper runtime | Bun 1.4.3 under `~/.local/opt/pstack-runtime`, exposed as `~/.local/bin/bun`. pstack's locked helper dependencies are included in the refreshed plugin cache. |
| Personal skills | `~/plugins/park-workflow`: `agent-brain`, `agentic-scientist`, `verify-agent-workflow`. These connect existing research/game tools to context and evidence. |
| Knowledge base | `~/Documents/agent-brain`: preferences, project pointers, author/source card, decisions, lessons, run receipts, and templates. Repositories retain canonical project state. A removed project is marked unavailable. |
| Empryo | Official signed 3.9.4-beta binary under `~/.empryo/bin`; ChatGPT subscription connected; `subscriptions/gpt-5.6-terra` used for the coding check. Its model list differs from Codex's; Astra was not advertised in the observed subscription list. |
| Desktop integration | `~/.empryo/themes/koda.json` matches the existing monochrome palette. `agent-desk` opens a project picker and Kitty; desktop entry and Hyprland Super+A binding installed. Compact diffs and turn notifications enabled. |
| Health routine | Daily around 08:00 UTC, systemd user timer runs `agent-workflow health`; writes brain `runs/health.md` and JSON. No model calls. |
| Review routine | Mondays around 08:15 UTC, systemd user timer runs `agent-workflow report`; aggregates reviewed receipts and surfaces correction evidence. No automatic model-written lessons or cross-project edits. |
| Scientist | Pinned upstream checkout and Python environment under `vendor/AI-Scientist-v3`. `agent-scientist` supplies the local temp directory and Codex defaults for doctor/preview. Runtime evidence is in STATUS.md. |
| Docker | Official rootless Docker under `~/.local/opt/docker-rootless`; `~/.local/bin/docker` points to its CLI. User `docker.service` and rootless context run containers without a root daemon. Images live under your home directory. |

The research wrapper prepends a dedicated Docker adapter, leaving the ordinary Docker command unchanged. Sakana passes the host UID/GID into its containers; rootless Docker requires container `0:0` to map back to that host account. The adapter checks that the daemon reports rootless operation before translating this exact user pair. It resolves the fixed rootless connection even when Sakana gives an installer a temporary home. A private bind-mount test passed with networking disabled, capabilities dropped, and the output still owned by Park. This verifies file ownership compatibility; full campaign behavior has a separate status.

The original built research image is retained as `agentic-scientist/agent-cli:upstream-2b8aa39285c3`. The active `:latest` tag adds the small local layer in `tools/scientist-image/Dockerfile`, which updates two known vulnerable Headless dependencies and verifies that only those two package versions changed. The upstream checkout stays unchanged. See [runtime notes](runtime-notes.md) for the scoped audit and [image evidence](../evidence/scientist-image.json) for exact image identities and rendering checks. The image identity records this build; floating upstream base images and installers mean the source revision alone cannot guarantee identical future rebuilds.

The run inspector is built and its localhost health endpoint was exercised. Start it with `agent-scientist inspect start --no-build`; it serves saved run artifacts at `http://127.0.0.1:8765`. Building the UI does not create experimental results.

No new MCP server was needed for these features. Existing Science, Blender/Roblox, research, and voice tools were retained. Useful integrations must earn their context, authentication, and maintenance cost through a task. The public Benny workflows are installed as procedures; company bots, Slack/Linear connections, and cloud-agent services are not reproduced just by copying their skills.

Pstack's installed names are namespaced, such as `$pstack:poteto-mode`, `$pstack:in-your-own-words`, `$pstack:teach`, `$pstack:correct`, and `$pstack:create-verification-skill`. Use the skill picker to confirm the displayed name. Its Cursor slash-command examples are not native Codex commands. Specialized workflows should be explicitly selected when relevant.

The original Orator Codex binary at `~/.local/share/orator/codex` and its `/record` integration were preserved. The aborted Rust-clean command was not relied on to reclaim space. After your cleanup, disk availability was rechecked before further installation. The only completed cache cleanup in this setup removed disposable package downloads.

Record a reviewed task like this, using real evidence:

```sh
agent-workflow record --task 'Fix reconnect state' --outcome accepted \
  --corrections 1 --evidence /absolute/path/to/test-output.txt \
  --lesson 'Reconnect must read server state before rendering.'
agent-workflow report
```

Do not record an API-equivalent subscription token estimate as actual spending. Supply `--seconds` and `--cost` only when measured. Receipt file existence is checked; whether the work deserves acceptance remains a review judgment. Counts from a few selected tasks are not a benchmark.

To inspect scheduling:

```sh
systemctl --user list-timers agent-workflow-health.timer agent-workflow-review.timer
systemctl --user status agent-workflow-health.service agent-workflow-review.service
```

User timers run while your user service manager is available. They are persistent and catch up when it returns. They do not guarantee activity while logged out, suspended, or powered off. Docker also runs as a user service. No remote always-on worker was provisioned.

For research, start with `agent-scientist doctor` and `agent-scientist preview`. The six upstream phases are drafting, investigation, ablations, final evaluation, post-hoc analysis, and paper. Preview prints “completed” phase labels and proposed checkpoint paths even though it executes no agents; checking those paths confirmed that it created no run directory. Its saved log is configuration evidence only. An actual campaign requires a scoped brief, controls, budgets, and the project's existing research rules. The optional external paper review and some image-generation paths need API credentials separate from your ChatGPT plan.

Recheck a changed surface with the smallest meaningful procedure in [the verification skill's feature map](/home/park/plugins/park-workflow/skills/verify-agent-workflow/features.md). The setup's Python receipt tests, app-server discovery, Empryo provider task, desktop observation, and timer execution test different layers. None substitutes for another.

To refresh pstack, inspect upstream changes first and update the pinned checkout intentionally. `tools/port_pstack.py` produces the local adaptation; preserve CODEX.md and provenance, validate every skill, use the system plugin cachebuster helper, reinstall with `codex plugin add pstack@personal`, and check fresh discovery. Do not silently update your workflow from an unreviewed latest branch.

Rollback is specific and reversible:

- Restore Codex settings from `~/.codex/backups/agentic-workflow-20261016T025917Z/config.toml`, or restore only approval/sandbox keys if other settings have since changed. Remove or edit the newly added global AGENTS.md separately.
- Use `codex plugin list` and the CLI's remove command to disable the two new plugins. The source directories and knowledge files can remain for reference.
- Empryo and Hyprland backups are under `~/.local/state/agentic-workflow/backups/20261016T030158Z`. Restore only this setup's changes if you have subsequently edited either config; reload Hyprland afterward.
- Disable local routines with `systemctl --user disable --now agent-workflow-health.timer agent-workflow-review.timer`.
- Stop the research container daemon with `systemctl --user disable --now docker.service`. Keep images until you decide whether to reuse them; deleting them forces downloads and rebuilds.
- Sign out of the ChatGPT plan from Empryo's `/login` interface if desired. Configuration backups do not contain copied authentication tokens.

Full-access mode was explicitly requested and verified for new Codex sessions. It removes a technical approval barrier; it does not expand the meaning of an instruction such as “prepare a draft” into permission to publish or send it. [Official approval documentation](https://learn.chatgpt.com/docs/agent-approvals-security).
