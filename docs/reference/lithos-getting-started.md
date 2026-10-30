# Getting started with Lithos

Lithos is a way to give a project to a team of AI assistants. Start with a small, clear request, such as “help me make a simple website.” You stay in charge of the goal and any decisions the assistants bring back.

## What you need

- macOS, Linux, or Windows. On Windows, use Ubuntu through WSL 2.
- On macOS or Linux: Node.js 22 or 24, Git, and tmux installed.
- Codex or Claude Code installed and signed in. One is enough.
- A folder for the project you want to work on.

The setup below uses a terminal. If you are unfamiliar with it, you can ask someone comfortable with the terminal to help.

## Windows

Lithos runs on Windows using Ubuntu in Windows Subsystem for Linux (WSL 2). A direct Windows installation is not supported.

1. Open PowerShell as an administrator and run `wsl --install -d Ubuntu`. Restart if Windows asks, then open Ubuntu and create your Linux username and password. If Ubuntu is already installed, open it instead; `wsl --list --verbose` in PowerShell shows whether it uses version 2. If it shows version 1, run `wsl --set-version Ubuntu 2` in PowerShell. See [Microsoft's WSL guide](https://learn.microsoft.com/en-us/windows/wsl/install) if you need help.
2. In the Ubuntu terminal, run these commands. Keep the checkout in your Linux home folder:

```sh
sudo apt-get update && sudo apt-get install -y git
git clone https://github.com/amarionfred/workflow.git "$HOME/lithos"
cd "$HOME/lithos"
bash scripts/install-wsl.sh --dry-run
bash scripts/install-wsl.sh
```

The installer adds any missing Ubuntu tools, installs nvm if needed, selects Linux Node.js 24, and builds Lithos. It may ask for your Linux password.

3. In your Ubuntu terminal, load Node and set up the assistant you want. This example uses Codex; replace `codex` with `claude` for Claude Code.

```sh
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
. "$NVM_DIR/nvm.sh"
nvm use 24
lithos setup --providers codex --no-herdr --dry-run
lithos setup --providers codex --no-herdr
```

If you are not signed in, run `codex login` (or `claude auth login`). In a new Ubuntu terminal, run `nvm use 24` before using Lithos if it is not already on your path.

4. Start Lithos and check that its operator has started:

```sh
lithos daemon start
lithos ps --nodes --rig kernel
```

When `operator-agent@kernel` is running, open it in the same terminal with `tmux attach -t operator-agent@kernel`. Tell the operator what you want to do and where your project is. Press **Ctrl+B**, release, then **D** to leave the view without stopping the team. Run `lithos tui` to see the dashboard.

This route uses WSL and has not yet been verified on a Windows computer. Keep your project files inside the Linux home folder when possible.

## macOS and Linux

### Build from this repository

Lithos is currently distributed as source code. In a terminal, run:

```sh
git clone https://github.com/amarionfred/workflow.git lithos
cd lithos
sh scripts/install.sh
```

Run `lithos --help` to check the installation. Then run `lithos setup --dry-run` to see what setup would change, followed by `lithos setup` if you are comfortable with those changes. Run `lithos start` to start Lithos, then `lithos terminal open saved:kernel --window` to open its view. Tell the operator what you would like to do and where your project is.

Setup can modify configuration and install optional tools. Starting a team can add guidance and settings to its project. Review the setup preview and permissions before continuing. The assistants can make mistakes, so review their work.

The installer also provides `rig` as a compatibility command; installing it can replace an existing command with that name. Existing installations and some older technical names remain supported for compatibility. The detailed [technical help](help.md) describes the inherited system and may use those older names.
