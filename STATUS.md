# Workflow setup: current evidence

Updated 2026-10-16. Setup is implemented and verified to the scope below. Start with README.md and the practical guide; the runtime checks are complete.

| Requirement | Observed state and evidence |
| --- | --- |
| Nine links | All mapped in `docs/sources.md`; text/articles recovered. Kai clip sampled visually every 12 seconds; no complete-transcript claim. |
| Lauren's workflow | 41 primary posts collected, three long articles read, public pstack pinned. See `docs/lauren-post-index.md` and `research/lauren-primary-corpus.json`. Further talks are listed as unwatched. |
| Public pstack skills | 54 core + 3 Benny installed; 23 playbooks retained. Schemas pass, fresh discovery finds 57 with zero errors. See `evidence/pstack-validation.json`, `evidence/codex-discovery.json`, and provenance. |
| Helper runtime | Bun 1.4.3 plus locked dependencies. 68 distinct tests covered; five sandbox subprocess failures passed on the targeted rerun outside it. Typecheck and installed-cache CLI pass. See `evidence/pstack-runtime.json`. |
| Roles, loops, trust | Task/role/receipt templates, context retrieval, real model task, independent verification, structural correction, and reviewed receipt. See `docs/working-together.md` and `evidence/empryo-*.json`. |
| Felix's framework | Primary essay applied to concrete game and research briefs in the guide. |
| Markdown brain | Preferences, lessons, decisions, source card, nine project cards, templates, receipts and reports. Eight project pointers resolve; removed ethical-distillation marked unavailable. See `evidence/workflow-checks.json`. |
| Empryo | 3.9.4-beta, doctor 9/9; Koda theme, launcher, desktop entry, Super+A. ChatGPT subscription task completed. Three agent-written tests passed; independent checks found two wrong exception types; correction made, all 22 checks pass. See `evidence/empryo-model-run.json` and before/after evidence. |
| Useful additions | Three personal workflow skills installed/discovered. Existing research, Roblox, Science/Blender and Orator tools retained. No new MCP account needed. |
| Automation | Daily health and Monday receipt-review user timers active/waiting and manually exercised with success. Reports are local and deterministic; no model calls. See brain `runs/` and `setup-snapshot/` units. |
| Teaching | Practical guide, project examples, full change map, commands, limits, rollback, and 57-skill inventory written. Start at README.md. |
| Full access | Fresh process verifies `danger-full-access`, approvals `never`, Astra/xhigh retained. Current session still has enforced restrictions. See `evidence/codex-discovery.json`. |
| Scientist | Pinned CLI and image built; doctor reports 21 passed, 7 optional warnings, 0 failures. The unchanged CPU baseline passed both natively and through Sakana's actual container preparation/evaluation path. Rootless private-file check passed. Inspector built and localhost health API responded; temporary server stopped. Autoillustrate 0.4.8, Headless 0.6.1, container Codex and TeX versions pass. Real SVG and PNG exports pass; PNG visually inspected. See `evidence/scientist-task-runtime.json` and `evidence/scientist-image.json`. |

Both image builds and all setup verification processes have finished. The preserved upstream image ID starts with `19a9463c0bf3`; the active image starts with `3f46633bab5e`. The local layer updates exactly two Headless dependencies; command checks pass and its production npm audit reports zero findings. Full IDs and the 7,140,778,579-byte image size are recorded in image evidence. No verification containers remain running.

The first direct renderer check timed out before Draw.io started because its virtual-display launcher was running as container PID 1. Retrying with Docker `--init` passed both exports while retaining network isolation and dropped capabilities. The failed attempt and final logs are preserved under `evidence/scientist-renderer/`.

The temporary inspector test server on `127.0.0.1:8765` was stopped after verification; its backend reported clean application shutdown. Launch on demand with `agent-scientist inspect start --no-build`.

Scientist evidence: `evidence/scientist-provenance.json`, `evidence/scientist-preview.log`, `evidence/circpack-baseline/`, `evidence/scientist-rootless.json`, `evidence/scientist-task-runtime.json`, and `evidence/scientist-image.json`. Preview prints completed labels and proposed checkpoint paths, but direct inspection confirmed no run directory was created. Both actual baseline evaluations scored 0.9597642169962064 with 26 circles; container preparation and validation took 97.822 seconds and made zero model calls. No optimized discovery, paper reproduction, six-phase AI campaign, full Autoillustrate model workflow, external paper review, or generated paper is claimed. GPU work and optional external API services require their own working runtime/credentials and a scoped research brief.

Pinned sources: pstack `99743e9c151c8537cbbf1f98bb38f34ef3368453`; Scientist `2b8aa39285c35aaca3b0e06dd121061ef8a2d854`. Upstream tracked files are unchanged. Nonsecret launchers, theme, adapter instructions, and units are preserved in `setup-snapshot/`.

Repository capture, 2026-10-16: the private GitHub repository is [amarionfred/workflow](https://github.com/amarionfred/workflow). The expanded snapshot preserves all three personal plugins, retained research/utility skills, the Markdown knowledge base, selected nonsecret configuration, launchers, and units; 326 snapshot files have source paths and SHA-256 hashes. The two upstream checkouts are pinned as submodules. The 22 receipt-processing checks passed again during capture. See [repository contents and restoration](docs/repository.md). This capture does not add a new end-to-end runtime or second-machine restore claim.
