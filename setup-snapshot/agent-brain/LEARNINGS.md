# Observed lessons

## 2026-10-16 — Installation needs a storage preflight

Observed: installing Agentic Scientist failed with `ENOSPC`; `/home` had about 8 MB free. Removed only the pip download cache after approval, reclaiming about 748 MB. Installed environments and project files were preserved.

Structural response: the workflow health report measures free disk and records it before future large setup or experiment runs. A successful package installation does not prove there is enough space for datasets, build images, or experiment artifacts.

## 2026-10-16 — Cross-harness skills need real tool mapping

Observed: upstream pstack names Cursor's Task tool, Grok/Claude model slugs, transcript paths, and `/loop`. Copying it verbatim would leave misleading or unusable instructions.

Response: preserved the pinned original, added a Codex adapter, converted metadata, and validated all 57 installed skill entrypoints. Runtime behavior still requires a representative task; schema validation alone does not prove workflow quality.
# 2026-10-16: observed corrections during setup

- Sakana's dry run prints completed phases and checkpoint paths, but direct path inspection confirmed no run directory existed. Preserve the preview log as configuration evidence; do not infer artifacts or completed experiments from success-looking output.
- Empryo's receipt function passed its own three tests but returned TypeError for two malformed outcome types. Added a boundary type check and regression inputs; all 22 independent caller checks then passed. Evidence: `/home/park/Projects/agentic-workflow/evidence/empryo-independent-after.json`.
- Five pstack subprocess checks failed inside the active sandbox and passed when their test files were rerun outside it. The fix was to verify the execution environment, not weaken upstream assertions. Evidence: `evidence/pstack-runtime.json` in the workflow workspace.
- Rootless Docker maps host Park to container UID 0. The research runner's explicit host UID needed a narrowly scoped adapter. A private mount round-trip proved host file ownership with network disabled and capabilities dropped. Evidence: `evidence/scientist-rootless.json`.
- Project pointers can become stale during disk cleanup. Rechecking the index found ethical-distillation unavailable; its card now records that observation instead of inventing current project state.
