# Contributing to Lithos

Thanks for helping improve Lithos. For a bug, open an issue and describe what happened, what you expected, and how to reproduce it. Remove private information, credentials, and personal paths before sharing.

For a larger change, describe the idea in an issue first. Small fixes can go straight into a pull request. For a security issue, follow the [security policy](SECURITY.md).

## Development setup

You need Node.js 22 or 24, npm 10 or newer, Git, tmux, and rsync.

```sh
git clone https://github.com/amarionfred/workflow.git lithos
cd lithos
npm ci
npm run build
npm test
npm run lint
```

Use a separate test environment for work that starts services or assistants. See the [worktree guide](docs/reference/worktree-builds.md) and [setup reference](docs/reference/getting-started.md#before-you-start).

Describe what your change does and how you checked it in your pull request. Keep license notices and attribution when adapting existing work. Contributions use the [Apache-2.0 license](LICENSE).
