#!/usr/bin/env bash
# Prepare an Ubuntu WSL installation and build Lithos in the Linux user account.
set -eo pipefail

case "${1-}" in
  --help|-h) printf '%s\n' 'Usage: bash scripts/install-wsl.sh [--dry-run]'; exit 0 ;;
  --dry-run)
    [ "$#" -eq 1 ] || { echo 'Usage: bash scripts/install-wsl.sh [--dry-run]' >&2; exit 2; }
    printf '%s\n' 'Lithos Windows setup plan:' '  Install missing Ubuntu tools with apt (may ask for your password).' '  Install nvm if needed, use Linux Node.js 24, then build and install this checkout.' '  nvm may add its setup to your shell profile. No changes made in this preview.'
    exit 0 ;;
  '') [ "$#" -eq 0 ] || { echo 'Usage: bash scripts/install-wsl.sh [--dry-run]' >&2; exit 2; } ;;
  *) echo 'Usage: bash scripts/install-wsl.sh [--dry-run]' >&2; exit 2 ;;
esac

if [ -z "${WSL_DISTRO_NAME:-}" ] && ! grep -qi microsoft /proc/sys/kernel/osrelease; then
  echo 'Run this inside Ubuntu on Windows (WSL), not in Windows PowerShell.' >&2
  exit 1
fi
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
[ -f "$root/scripts/install.sh" ] || { echo 'Run this from a complete Lithos checkout.' >&2; exit 1; }

missing=false
for tool in git curl tmux make g++ python3; do
  command -v "$tool" >/dev/null 2>&1 || missing=true
done
if [ "$missing" = true ]; then
  command -v apt-get >/dev/null 2>&1 || { echo 'This helper needs Ubuntu or another apt-based WSL distribution.' >&2; exit 1; }
  if [ "$(id -u)" -eq 0 ]; then
    apt-get update
    apt-get install -y ca-certificates curl git tmux build-essential python3
  else
    command -v sudo >/dev/null 2>&1 || { echo 'Install sudo or the required tools, then retry.' >&2; exit 1; }
    sudo apt-get update
    sudo apt-get install -y ca-certificates curl git tmux build-essential python3
  fi
fi

# A Linux Node under nvm avoids accidentally using a Windows node.exe and lets
# npm install into the Linux user's home without changing the system prefix.
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
if [ ! -s "$NVM_DIR/nvm.sh" ]; then
  curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.8/install.sh | bash
fi
[ -s "$NVM_DIR/nvm.sh" ] || { echo 'nvm did not install; check the output above and retry.' >&2; exit 1; }
# nvm uses shell functions and does not support nounset.
. "$NVM_DIR/nvm.sh"
nvm install 24
nvm use 24
[ "$(node -p 'process.platform')" = linux ] || { echo 'Node.js must run inside Linux, not as Windows node.exe.' >&2; exit 1; }
case "$(node --version)" in v24.*) ;; *) echo 'Node.js 24 could not be selected.' >&2; exit 1 ;; esac
command -v npm >/dev/null 2>&1 || { echo 'npm is missing from the selected Linux Node installation.' >&2; exit 1; }

# The nvm distribution already includes its matching headers. Use them for
# native npm modules instead of downloading the same headers a second time.
node_root=$(CDPATH= cd -- "$(dirname -- "$(command -v node)")/.." && pwd)
if [ -z "${npm_config_nodedir:-}" ] && [ -z "${npm_package_config_node_gyp_nodedir:-}" ] && [ -f "$node_root/include/node/node.h" ]; then
  export npm_package_config_node_gyp_nodedir="$node_root"
fi

sh "$root/scripts/install.sh"
printf '%s\n' 'Lithos is installed in WSL.' 'In your Ubuntu terminal, load nvm and run nvm use 24 before using lithos.' 'Continue with the Windows steps in docs/reference/lithos-getting-started.md.'
