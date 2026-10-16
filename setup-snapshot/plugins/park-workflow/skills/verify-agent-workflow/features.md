# User-visible feature map

| Feature | Entry | Expected behavior | Evidence |
| --- | --- | --- | --- |
| Choose workspace | Super+A or `agent-desk` | Existing project picker opens Empryo in the selected directory | Live picker and app window |
| Open a known workspace | `agent-desk /absolute/project` | Kitty window titled Empryo with Koda colors | Screenshot and process cwd |
| Discover skills | Codex skill picker / app-server skills/list | All 57 pstack skills are enabled and resolvable | `evidence/codex-discovery.json` |
| Work unattended | Start a fresh Codex session; set `/goal` | Config resolves to never/full-access; goal continues within runtime limits | Config/read plus the actual goal state |
| Recall project context | Agent brain index → project card | Card leads to an existing canonical project file | File/path check and real retrieval |
| Health snapshot | `agent-workflow health` | JSON and Markdown agree on observed disk/config/install state | `Documents/agent-brain/runs/health.*` |
| Record a run | `agent-workflow record ...` | Existing evidence required; receipts append without replacing history | Receipt behavior check |
| Scheduled report | `agent-workflow-health.timer` | Daily local report, including catch-up after login | Active timer, next run, service result |
| Preview research | `agent-scientist preview` | Six configured stages are printed, none executed | Captured preview output |
