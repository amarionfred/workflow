#!/bin/sh
# Build and install the checkout the person selected; no registry package is assumed.
set -eu

case "${1-}" in
  --help|-h) printf '%s\n' 'Usage: sh scripts/install.sh [--dry-run]'; exit 0 ;;
  --dry-run)
    [ "$#" -eq 1 ] || { echo 'Usage: sh scripts/install.sh [--dry-run]' >&2; exit 2; }
    printf '%s\n' 'Lithos install plan:' '  Install this checkout’s dependencies, build its package, and install it to the npm global prefix.' '  Afterward, review lithos setup --dry-run before running lithos setup.' 'Dry run: nothing changed.'
    exit 0 ;;
  '') [ "$#" -eq 0 ] || { echo 'Usage: sh scripts/install.sh [--dry-run]' >&2; exit 2; } ;;
  *) echo 'Usage: sh scripts/install.sh [--dry-run]' >&2; exit 2 ;;
esac

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
if [ ! -f "$root/package.json" ] || [ ! -f "$root/packages/cli/package.json" ]; then
  echo 'Run this script from a complete Lithos checkout. See the getting-started guide.' >&2
  exit 1
fi
for tool in node npm; do
  command -v "$tool" >/dev/null 2>&1 || { echo "Missing $tool: install Node.js 22 or 24 with npm." >&2; exit 127; }
done
version=$(node --version)
case "$version" in v22.*|v24.*) ;; *) echo "Lithos requires Node.js 22 or 24; found $version." >&2; exit 1 ;; esac
cd "$root"
npm ci
npm run build:package
npm install -g --install-links "$root/packages/cli"
modules=$(npm root -g)
checker="$modules/@lithos/cli/scripts/check-abi.mjs"
[ -f "$checker" ] || { echo "Installed Lithos compatibility checker not found: $checker" >&2; exit 1; }
node "$checker"
printf '%s\n' 'Lithos is installed. Run lithos setup --dry-run to review setup before you continue.'
