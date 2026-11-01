# Lithos

Lithos helps a team of AI assistants work together on a project. You describe what you want, and the team can divide the work, keep track of progress, and bring decisions back to you.

You can use it to build software, explore an idea, or maintain a project. The team keeps its work and conversations organized so you can return to them later. You choose which assistants to use and what they are allowed to do.

Lithos runs on Mac, Linux, or Windows using WSL 2. It works with Codex and Claude Code; you need an account for at least one of them.

[Get started](docs/reference/lithos-getting-started.md) · [Technical reference](docs/reference/help.md) · [License](LICENSE)

## Harness engineering

Lithos coordinates ordinary coding-agent sessions through a local daemon. The harness makes team state, work ownership, context and recovery inputs explicit, so people and agents can inspect how work is organized.

| Mechanism | What it provides |
| --- | --- |
| Shared state | CLI, terminal UI and MCP clients use the same daemon, backed by SQLite. The [architecture map](ARCHITECTURE.md#the-request-path) connects those interfaces to services, storage and runtime adapters. |
| Durable work records | [Queue items](packages/daemon/src/domain/queue-repository.ts) store destinations, status, blockers and transition history. Assignments remain inspectable across turns, with recorded ownership and handoffs. |
| Stable seats and recovery | [Durable node IDs](docs/reference/seat-node-targeting.md) identify seats separately from their current sessions. [Stored snapshots](packages/daemon/src/domain/snapshot-repository.ts) supply explicit recovery inputs, including checks for unusable snapshots. |
| Inspectable context | [Startup layering](docs/reference/agent-startup-guide.md#context-loading-what-goes-where) separates reusable skills from role and project guidance. Team specifications declare which files and skills each agent receives. |
| Per-seat input controls | [Delivery modes](docs/reference/seat-delivery.md) can hold messages or protect unfinished input for a chosen seat. These controls are configurable and separate from the coding agent's runtime permissions. |
| Testable coordination | [Installed-package scenarios](packages/test-system/ci/README.md) exercise queue persistence through daemon restarts, with injected faults to check the assertions. [Live-model evaluations](packages/test-system/evals/README.md) are a separate check of context selection and use. |

The test documentation records the supported checks and their limits. Scripted infrastructure checks do not establish model quality or successful project delivery.

## See Lithos

These example screens use sample data.

**Your team:** See what each assistant is doing and who needs your attention.

![Lithos team view showing assistants and their status](assets/ui/screenshots/lithos/team.png)

**Team map:** See how the assistants work together.

![Lithos team map showing connected assistant roles](assets/ui/screenshots/lithos/team-map.png)

**Project progress:** Follow the work as it moves forward.

![Lithos project view showing work in progress](assets/ui/screenshots/lithos/project-progress.png)

Lithos is based on [OpenRig](https://github.com/mvschwarz/openrig), an open-source project by mvschwarz and its contributors. Their work and license are credited in [NOTICE](NOTICE).
