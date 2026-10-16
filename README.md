# Amarion's agent workflow

Private repository: [amarionfred/workflow](https://github.com/amarionfred/workflow). See [repository contents and restoration](docs/repository.md) for the captured setup, pinned upstream sources, and exclusions.

Start with [the practical guide](docs/working-together.md). The system combines Codex, Lauren Tan's public pstack methods, a small Markdown knowledge base, Empryo, and a research runner. Its value comes from clear outcomes and observable checks; installing more tools does not establish better results.

- [What changed and how to undo it](docs/changes-and-operations.md)
- [Primary sources and Lauren's workflow](docs/sources.md)
- [Every installed pstack skill](docs/pstack-inventory.md)
- [Current verification and remaining limits](STATUS.md)
- [Knowledge map snapshot](setup-snapshot/agent-brain/AGENTS.md) (live copy: `/home/park/Documents/agent-brain/AGENTS.md`)

Choose a project in Empryo, or run `agent-desk /absolute/project/path`. Your existing Codex retains `/record`. Start a new Codex session to pick up the new plugin catalog and full-access defaults.

Useful local commands:

```sh
agent-workflow health
agent-workflow report
agent-scientist doctor
agent-scientist preview
```

The first two commands only inspect local state and receipts. The research preview prints the configured commands; it does not perform research or create a completed experiment. Check STATUS.md before treating any installation or preview as a successful end-to-end run.
