# Getting started with Lithos

Lithos is a way to give a project to a team of AI assistants. Start with a small, clear request, such as “help me make a simple website.” You stay in charge of the goal and any decisions the assistants bring back.

## What you need

- macOS or Linux, with Node.js 22 or 24, Git, and tmux installed.
- Codex or Claude Code installed and signed in. One is enough.
- A folder for the project you want to work on.

The setup below uses a terminal. If you are unfamiliar with it, you can ask someone comfortable with the terminal to help.

## Build from this repository

Lithos is currently distributed as source code. In a terminal, run:

```sh
git clone https://github.com/amarionfred/workflow.git lithos
cd lithos
sh scripts/install.sh
```

Run `lithos --help` to check the installation. Then run `lithos setup --dry-run` to see what setup would change, followed by `lithos setup` if you are comfortable with those changes. Run `lithos start` to start Lithos, then `lithos terminal open saved:kernel --window` to open its view. Tell the operator what you would like to do and where your project is.

Setup can modify configuration and install optional tools. Starting a team can add guidance and settings to its project. Review the setup preview and permissions before continuing. The assistants can make mistakes, so review their work.

The installer also provides `rig` as a compatibility command; installing it can replace an existing command with that name. Existing installations and some older technical names remain supported for compatibility. The detailed [technical help](help.md) describes the inherited system and may use those older names.
