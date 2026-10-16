#!/usr/bin/env bash
# Empryo web installer — macOS & Linux.
#
#   curl -fsSL https://empryo.com/install.sh | bash
#   wget -qO-  https://empryo.com/install.sh | bash
#
# What it does:
#   1. Detects platform/arch (incl. Rosetta on Apple Silicon and pre-Haswell
#      x86_64 Linux CPUs → baseline build, with a one-shot baseline retry if
#      the standard build still dies on a signal).
#   2. Resolves the requested release (latest by default, EMPRYO_VERSION=x.y.z
#      to pin) from dl.empryo.com.
#   3. Downloads the platform tarball + SHA256SUMS.txt and verifies the
#      RSA-4096 signature and sha-256 checksum before anything executes.
#   4. Extracts to a temp dir and runs the bundled install.sh, which installs
#      to ~/.empryo/ and adds ~/.empryo/bin to PATH.
#
# Options (env vars — `curl | bash` can't take flags):
#   EMPRYO_VERSION=2.19.0   pin a version (default: latest)
#   EMPRYO_QUIET=1          non-interactive output (CI, scripts)
#   EMPRYO_ARCH=x64-baseline force a build variant (x64 | arm64 | x64-baseline);
#                           default: auto-detected from the CPU
#   EMPRYO_NO_VERIFY=1      skip checksum verification (NOT recommended;
#                           only for air-gapped mirrors without SHA256SUMS)
#   EMPRYO_THEME=crimson    installer accent (empryo | soul | coffee | water |
#                           crimson | undertow) — empryo.com sets this to match
#                           the theme you picked on the site
#   EMPRYO_PLAIN=1          text and newlines only — no colour, no mote, no
#                           cursor control (what a pipe, CI or the in-app
#                           updater gets automatically)
#   NO_COLOR=1              plain output
#
# This script is served as a static asset from empryo.com (synced into the
# webapp public/ at build time). Binaries are fetched from dl.empryo.com — a
# public Cloudflare R2 bucket — never from GitHub or npm.

# Re-exec under bash if invoked via sh/dash (dash lacks pipefail).
if [ -z "${BASH_VERSION:-}" ]; then
  exec bash "$0" "$@"
fi
set -euo pipefail

DL_BASE="https://dl.empryo.com"
VERSION="${EMPRYO_VERSION:-}"
QUIET="${EMPRYO_QUIET:-}"
NO_VERIFY="${EMPRYO_NO_VERIFY:-}"

# Pinned release-signing public key (RSA-4096). Every release's SHA256SUMS.txt
# carries a detached signature from the matching private key — a secret kept
# separate from the R2 upload credential. We verify that signature against
# this committed key before trusting any checksum, so compromising
# dl.empryo.com (or its write credential) alone cannot forge an install.
EMPRYO_SIGN_PUBKEY="-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAruhF8gaO+gJ3hzCb+foC
QOAeNMIbbfD7uV+EzessuD6TDB0TurY8EEi9T9DtOPuXGk9zNFgKo73IWWQmTYvx
eIjDIoz1BzUjBkFD0HLy1QPRPKGlnKnVz0j2cb9PEA3gCnlsEC55OPVp2hLuTq5L
Ak4g0AmJeyPmTwuX1MuR7ZI9ETDaQeMsGdI816DX7ySyR4RAYXzLfWFXIKBehVfu
+TcKZk7f8AjT4d1g9+9hMsC9YsezET06yQWeJidAs/xi/E/wT0EmKQ8Ps/y54g7o
7iAZM5B1oilAzS+XLUUHyk6BbX6PWgpgrhs2iIVwoE9aMTO10fDhzJn/86vz29PT
mzi9/SjI8D5ibFIMgeK2e34l4i4OWknbmbscfVRDbB+qwnIFXgguHg1vTmacSnag
HKdOAXDIZYzpDprrAXOmFItReAJ8MFZGKUfR/HuFaSVNQYL/nFja4TeHAX0hhTk3
y9uI96UJ4T708iu1EtT2W+gO+iKrCi3PVJgeORZ8kAS7ZEQHjT//ndd5UofyfE32
ayz/mBIwXm8VTNBB9uis+MX6NmwT+cjTJoOts0Iu7kix0a/wnypeMPsAOUeTENQd
lMvhnXyXtSEhjP8/jWXxavxcc+Km884+/+OSeJAsSXQ2ydzEGxXnoNAM/pW3D5xs
nYBZ3Y5B7tNTnm5Rw4+G7EUCAwEAAQ==
-----END PUBLIC KEY-----"

# ── Presentation ──────────────────────────────────────────────────────
# Three output modes, decided once, here:
#
#   rich   a real terminal — accent colour, the mote drawn in braille
#   plain  a pipe, a log, CI, or EMPRYO_PLAIN=1 — line-per-event, no colour,
#          no cursor movement, no carriage returns, no spinner
#   quiet  EMPRYO_QUIET=1 — the same as plain, minus the brand block
#
# Plain mode is not a courtesy, it is a contract. Empryo's own update flow
# spawns this script with its stdio piped into the TUI, and every escape byte
# that reaches that pipe is painted as garbage across an OpenTUI frame. So the
# rule is absolute: if stdout is not a terminal, nothing but text and newlines
# leaves this script. EMPRYO_PLAIN is exported further down so the bundled
# installer inside the tarball obeys the same contract.
USE_COLOR=""
if [[ -z "$QUIET" && -z "${NO_COLOR:-}" && -z "${EMPRYO_PLAIN:-}" && -t 1 && -n "${TERM:-}" && "${TERM:-}" != "dumb" ]]; then
  USE_COLOR=1
fi

# Braille needs a UTF-8 locale to survive the trip. A bare `ssh host 'curl … |
# bash'`, a Windows OpenSSH session and a scratch container often carry no
# locale at all — there the mark degrades to ASCII instead of mojibake.
UTF8=""
case "${LC_ALL:-${LC_CTYPE:-${LANG:-}}}" in
  *[Uu][Tt][Ff]*8* | *[Uu][Tt][Ff]8*) UTF8=1 ;;
esac
if [[ -n "$USE_COLOR" ]]; then
  # Accent + its dim companion, per theme. These are the proxySoul palettes
  # from the app itself (packages/base/src/theme/tokens.ts) — same names,
  # same hues, so the terminal matches the product you are about to run.
  case "${EMPRYO_THEME:-empryo}" in
    soul)    AC=$'\033[38;2;155;106;245m' AD=$'\033[38;2;120;68;240m' EY=$'\033[38;2;255;61;127m' ;; # proxySoul purple
    coffee)  AC=$'\033[38;2;232;138;26m' AD=$'\033[38;2;200;148;74m' EY=$'\033[38;2;240;112;58m' ;; # amber & burnt orange
    water)   AC=$'\033[38;2;30;180;224m' AD=$'\033[38;2;24;151;192m' EY=$'\033[38;2;26;184;164m' ;; # ocean blue & teal
    crimson) AC=$'\033[38;2;244;58;107m' AD=$'\033[38;2;180;62;98m' EY=$'\033[38;2;255;122;162m' ;; # plum-black crimson
    undertow) AC=$'\033[38;2;152;176;194m' AD=$'\033[38;2;122;146;164m' EY=$'\033[38;2;196;154;164m' ;; # monochrome night tide
    *)       AC=$'\033[38;2;61;255;57m' AD=$'\033[38;2;74;167;74m' EY=$'\033[38;2;54;238;51m' ;; # empryo terminal green
  esac
  G="$AC"                      # accent — glyphs, banner
  GD="$AD"                     # dim accent — quiet success
  A=$'\033[38;2;233;196;106m'  # amber — warnings
  R=$'\033[38;2;255;80;70m'    # red — failure
  W=$'\033[38;2;200;200;196m'  # body text
  D=$'\033[2m'                 # dim
  B=$'\033[1m'                 # bold
  X=$'\033[0m'
else
  G="" GD="" A="" R="" W="" D="" B="" X=""
fi

# ── The Mote block ───────────────────────────────────────────────────
# Empryo's terminal identity, the same as the app's boot splash: Mote on the
# left hatching as the install advances, the name, what is happening, a live
# bar with its percentage and the current step on the right. Rich mode only;
# a pipe, CI or the in-app updater gets one plain line per step instead.
MOTE=(
  '                '
  '                '
  '       {⢠⡾⠛⢿⡆}    '
  '       {⠈⠿⣶⠾⠃}    '
  '                '
  '                '
  '                '
  '                '
  '    ⢀⠔⠚⠉⠙⣒⡦     '
  '   ⢠⠁  {⢠⣿⠻⢿⣎}⡄   '
  '   ⢠   {⠘⠿⣶⡿⠃}⡆   '
  '   ⠘⣆      ⣠⠃   '
  '    ⠈⠓⠦⠤⠶⠒⠊⠁    '
  '                '
  '                '
  '    ⣠⠖⠛⠛⠛⣛⡶⣄    '
  '   ⣼⠁  {⢰⣿⠻⣿⣯}⣧   '
  '   ⣿   {⠘⢿⣶⡿⠋}⣿   '
  '   ⠸⣧      ⣰⠏   '
  '    ⠈⠻⠶⠶⢶⠶⠛⠉    '
  '                '
  '                '
  '    ⣠⠶⠛⠛⢛⣛⡶⣄    '
  '   ⣼⠁  {⢰⣿⠻⣿⣯}⣷   '
  '   ⣿   {⠘⢿⣶⡿⠏}⣿   '
  '   ⠹⣧      ⣰⡏   '
  '    ⠙⠻⠶⠶⢶⠶⠟⠋    '
  '                '
  '     ⡄ ⢀⡄  ⡀    '
  '   ⢢⣴⠞⠛⠛⢛⣛⡾⣦⡀   '
  '   ⣾⠁  {⢰⣿⠻⣿⣿}⣿⠁  '
  '  ⠘⣿   {⠘⢿⣶⡿⠏}⣿⠂  '
  '   ⢽⣧⡀     ⣰⡟   '
  '    ⠙⢿⢶⡶⢶⠶⠟⠋⠂   '
  '     ⠁  ⠈       '
  '     ⣄⣀⣀⣆ ⢀⡀    '
  '   ⢲⣴⠟⠛⠛⢛⣻⣿⣦⣄   '
  '  ⢀⣿⠁  {⢰⣿⠻⢿⣯}⣿⠉  '
  ' ⠈⠛⣿   {⠘⢿⣶⡿⠏}⣿⠳⠄ '
  '  ⢠⢿⣇      ⣰⡟   '
  '    ⠙⣷⣶⣶⢶⠶⠟⠋⠂   '
  '     ⠁  ⠘       '
  '     ⣄⣀⣠⣆⡀⢀⡀    '
  '   ⢲⣴⠟⠛⠛⢛⣻⣿⣶⣄   '
  '  ⢀⣿⠁  {⢰⣿⠻⢿⣯}⣿⡉  '
  ' ⠈⠛⣿   {⠘⢿⣶⡿⠏}⣿⠳⠄ '
  '  ⢠⢿⣇      ⣰⡟   '
  '    ⠙⣿⣶⣶⢶⠶⠟⠋⠂   '
  '     ⠁  ⠘       '
  '     ⣄⢀⣀⣆ ⢀⡀    '
  '   ⢲⣴⠟⠛⠛⢛⣻⣿⣦⡄   '
  '  ⢀⣿⠁  {⢰⣿⠻⢿⣯}⣿⡉  '
  ' ⠈⠻⣿   {⠘⢿⣶⡿⠏}⣿⠳⠄ '
  '  ⢠⢿⣇      ⣰⡟   '
  '    ⠙⣷⣶⣶⢶⠶⠟⠋⠂   '
  '     ⠁  ⠘       '
  '     ⣄⢀⣀⣆ ⢀⡀    '
  '   ⢲⣴⠿⠛⠛⢛⣻⣿⣦⡀   '
  '  ⢀⣿⠁  {⢰⣿⠻⢿⣯}⣿⡉  '
  ' ⠈⠻⣿   {⠘⢿⣶⣿⠏}⣿⠷⠄ '
  '  ⢠⢿⣇      ⣠⡟   '
  '    ⠙⢷⣦⣴⣶⡶⠾⠛⠆   '
  '     ⠉  ⠘       '
  '     ⣄⢀⣀⣆ ⢀⡀    '
  '   ⢲⣴⠟⠛⠛⢛⣛⡿⣦⡀   '
  '  ⢀⣿⠁  {⢰⣿⠻⢿⣯}⣿⡉  '
  ' ⠈⠻⣿   {⠘⢿⣶⡿⠏}⣿⠳⠄ '
  '  ⢠⢽⣇      ⣠⡟   '
  '    ⠙⢷⣶⣴⢶⠶⠞⠋⠆   '
  '     ⠁  ⠘       '
  '     ⣄⢀⣀⣆ ⢀⡀    '
  '   ⢲⣴⠟⠛⠛⢛⣛⡿⣦⡄   '
  '  ⢀⣿⠁  {⢰⢫⢠⢌⢫}⣿⡉  '
  ' ⠈⠻⣿   {⠘⢮⣁⡡⠏}⣿⠳⠄ '
  '  ⢠⢿⣇      ⣰⡟   '
  '    ⠙⢷⣶⣴⢶⠶⠟⠋⠂   '
  '     ⠁  ⠘       '
  '     ⣄⣀⣠⣆⡀⢀⡀    '
  '   ⢲⣴⠟⠛⠛⢛⣻⡿⣶⣄   '
  '  ⢀⣿⠁  {⢰⢁⢠⢌⢫}⣿⡉  '
  ' ⠈⠛⣿   {⠘⢄⣁⡡⠎}⣿⠳⠄ '
  '  ⢠⢿⣇      ⣰⡟   '
  '    ⠙⣿⣶⣶⢶⠶⠟⠋⠂   '
  '     ⠁  ⠘       '
)
MOTE_ROWS=7
MOTE_REST=9
PCT=0
FRAME=0
TICK=0
BLOCK=""
TITLE="Getting ready"
LABEL=""
NOTES=()
if [[ -n "$UTF8" ]]; then
  BAR_ON="━" BAR_OFF="─" GL_OK="✓" EYE_GLYPH="⊙"
else
  BAR_ON="=" BAR_OFF="-" GL_OK="+" EYE_GLYPH="o"
fi
if [[ -n "$USE_COLOR" ]]; then
  EYE="$EY"
  EYE_DIM="$AD"
else
  EYE="" EYE_DIM=""
fi

bar() {
  local fill=$(( $1 * 24 / 100 )) i out="$G"
  for ((i = 0; i < 24; i++)); do
    if ((i == fill)); then out+="$D"; fi
    if ((i < fill)); then out+="$BAR_ON"; else out+="$BAR_OFF"; fi
  done
  printf '%s%s  %s%3d%%%s' "$out" "$X" "$W" "$1" "$X"
}

block_draw() {
  [[ -n "$USE_COLOR" ]] || return 0
  local i row right eye="$EYE"
  if [[ -n "$BLOCK" ]]; then printf '\033[%dA' "$MOTE_ROWS"; fi
  BLOCK=1
  if (( TICK / 7 % 3 == 2 )); then eye="$EYE_DIM"; fi
  for ((i = 0; i < MOTE_ROWS; i++)); do
    if [[ -n "$UTF8" ]]; then
      row="${MOTE[$((FRAME * MOTE_ROWS + i))]}"
      row="${row//\{/$eye}"
      row="${row//\}/$G}"
    else
      row="                "
    fi
    case $i in
      1) right="${W}${B}Empry${X}${EYE}${EYE_GLYPH}${X}" ;;
      2) right="${D}${TITLE}${X}" ;;
      4) right="$(bar "$PCT")" ;;
      5) right="${D}${LABEL}${X}" ;;
      *) right="" ;;
    esac
    printf '\033[2K  %s%s%s   %s\n' "$G" "$row" "$X" "$right"
  done
}

hatch() {
  FRAME=$(( PCT * MOTE_REST / 100 ))
  TICK=$((TICK + 1))
  block_draw
}

# step <percent> <label> [pid] — the bar eases toward <percent> while the job
# runs, then lands on it. Plain mode prints the label once.
step() {
  local target="$1" pid="${3:-}" rc=0
  LABEL="$2"
  if [[ -z "$USE_COLOR" ]]; then
    if [[ -n "$pid" ]]; then wait "$pid" || rc=$?; fi
    PCT="$target"
    if [[ -z "$QUIET" && "$rc" -eq 0 ]]; then printf '%s\n' "$LABEL"; fi
    return "$rc"
  fi
  if [[ -n "$pid" ]]; then
    while kill -0 "$pid" 2>/dev/null; do
      if (( PCT < target - 1 )); then PCT=$(( PCT + (target - PCT + 7) / 8 )); fi
      if (( PCT >= target )); then PCT=$(( target - 1 )); fi
      hatch
      sleep 0.08
    done
    wait "$pid" || rc=$?
  fi
  PCT="$target"
  hatch
  return "$rc"
}

# Row glyphs degrade with the locale, not with the colour.
if [[ -n "$UTF8" ]]; then
  GL_NOTE="·" GL_WARN="!" GL_FAIL="✗"
else
  GL_NOTE="-" GL_WARN="!" GL_FAIL="x"
fi

say_step() { printf '  %s%s%s\n' "$W" "$1" "$X"; }
detail()   { [[ -n "${EMPRYO_VERBOSE:-}" ]] && printf '  %s%s %s%s\n' "$D" "$GL_NOTE" "$1" "$X"; return 0; }
note() {
  if [[ -n "$BLOCK" ]]; then NOTES+=("$GL_NOTE $1"); LABEL="$1"; hatch; return 0; fi
  printf '  %s%s %s%s\n' "$D" "$GL_NOTE" "$1" "$X"
}
warn() {
  if [[ -n "$BLOCK" ]]; then NOTES+=("$GL_WARN $1"); LABEL="$1"; hatch; return 0; fi
  printf '  %s%s %s%s\n' "$A" "$GL_WARN" "$1" "$X"
}
say()      { echo "  $*"; }
fail()     { printf '\n  %s%s %s%s\n' "$R" "$GL_FAIL" "$*" "$X" >&2; exit 1; }

banner() {
  [[ -n "$QUIET" ]] && return 0
  if [[ -n "$USE_COLOR" ]]; then
    printf '\n\033[?25l'
    LABEL="Reading this machine"
    block_draw
  else
    printf 'Empryo\n'
  fi
}

# Accept either curl or wget so both the `curl -fsSL … | bash` and the
# `wget -qO- … | bash` install lines work (some minimal images ship only one).
if command -v curl >/dev/null 2>&1; then
  DL=curl
elif command -v wget >/dev/null 2>&1; then
  DL=wget
else
  fail "curl or wget is required"
fi
command -v tar >/dev/null 2>&1 || fail "tar is required"

# fetch_file URL DEST — download to a file; fetch_stdout URL — to stdout. Both
# follow redirects, pin https + TLS 1.2 on the curl path, and retry 3×.
fetch_file() {
  # Always silent. The 69 MB download has a progress indicator — ours, the
  # graph line above — and curl's own meter is three header rows plus a
  # carriage-return smear of numbers that fights it for the same screen (and
  # lands in the middle of a log or a TUI viewport when nobody is watching).
  if [ "$DL" = curl ]; then
    curl -fsSL --retry 3 --proto '=https' --tlsv1.2 "$1" -o "$2"
  else
    wget -q --tries=3 -O "$2" "$1"
  fi
}
fetch_stdout() {
  if [ "$DL" = curl ]; then
    curl -fsSL --retry 3 --proto '=https' --tlsv1.2 "$1"
  else
    wget -q --tries=3 -O - "$1"
  fi
}

banner

# ── Platform detection ────────────────────────────────────────────────
case "$(uname -s)" in
  Darwin) PLATFORM="darwin" ;;
  Linux)  PLATFORM="linux"  ;;
  *) fail "unsupported platform: $(uname -s) — Windows users: irm https://empryo.com/install.ps1 | iex" ;;
esac

ARCH="$(uname -m)"
case "$ARCH" in
  arm64|aarch64) ARCH="arm64" ;;
  x86_64|amd64)  ARCH="x64"   ;;
  *) fail "unsupported architecture: $ARCH (need arm64 or x86_64)" ;;
esac

# Rosetta 2 reports x86_64 to translated shells — install the native arm64
# build instead of the emulated one.
if [[ "$PLATFORM" == "darwin" && "$ARCH" == "x64" ]]; then
  if [[ "$(sysctl -in sysctl.proc_translated 2>/dev/null || echo 0)" == "1" ]]; then
    detail "Apple Silicon detected under Rosetta; using the native build"
    ARCH="arm64"
  fi
fi

# The standard x64 build targets Haswell (2013): the binary contains AVX2,
# FMA, BMI1 and BMI2 instructions. Gating on `avx` alone shipped it to Sandy/
# Ivy Bridge CPUs (AVX since 2011, none of the rest) and to a large class of
# virtualized pre-Haswell vCPU models — SIGILL at first launch (#188). Check
# every flag family the binary actually uses; an unreadable cpuinfo keeps the
# safe baseline pick. A wrong baseline still runs everywhere; a wrong standard
# is a core dump.
if [[ "$PLATFORM" == "linux" && "$ARCH" == "x64" ]]; then
  CPU_FLAGS="$(grep -m1 '^flags' /proc/cpuinfo 2>/dev/null || true)"
  for f in avx2 fma bmi1 bmi2; do
    if [[ " ${CPU_FLAGS} " != *" $f "* ]]; then
      note "Older CPU detected; using the compatibility build"
      ARCH="x64-baseline"
      break
    fi
  done
fi

# Explicit variant override wins over every auto-detection above — the escape
# hatch when detection guesses wrong (containers masking cpuinfo, forced
# baseline testing).
if [[ -n "${EMPRYO_ARCH:-}" ]]; then
  case "${EMPRYO_ARCH}" in
    x64|arm64|x64-baseline) ARCH="${EMPRYO_ARCH}"; detail "Build pinned to ${ARCH}" ;;
    *) fail "invalid EMPRYO_ARCH '${EMPRYO_ARCH}' (use x64, arm64, or x64-baseline)" ;;
  esac
fi

# musl (Alpine) is unsupported by Bun's glibc binaries — fail with a clear
# message instead of a cryptic loader error at first launch.
if [[ "$PLATFORM" == "linux" ]] && command -v ldd >/dev/null 2>&1; then
  if ldd --version 2>&1 | grep -qi musl; then
    fail "musl libc detected (Alpine?) — Empryo requires a glibc distribution"
  fi
fi

detail "Platform ${PLATFORM}-${ARCH}"

# No runtime warning here. The shipped binary is compiled with `bun build
# --compile` and carries its own runtime — measured on a stock debian machine
# with no Bun anywhere on it: `empryo doctor` passes 9/9, natives bound, both
# workers spawned (qa/seeds/barrier-install.ts, first-run-on-a-virgin-machine).
# The old warning told a brand-new user, on the very first screen, to go and
# install a 100 MB runtime they do not need — and it said it in the one place
# where nobody can check the claim.

# ── Resolve version ───────────────────────────────────────────────────
if [[ -z "$VERSION" ]]; then
  # The release pipeline publishes a bare version string at /latest.txt
  # (short-TTL pointer). Pin a specific build with EMPRYO_VERSION=x.y.z.
  VERSION="$(fetch_stdout "${DL_BASE}/latest.txt")" \
    || fail "could not resolve the latest version from ${DL_BASE}/latest.txt"
fi
VERSION="${VERSION#v}"
VERSION="$(printf '%s' "$VERSION" | tr -d '[:space:]')"
[[ -n "$VERSION" ]] || fail "could not resolve a version to install"

BUNDLE="empryo-${VERSION}-${PLATFORM}-${ARCH}"
BASE_URL="${DL_BASE}/v${VERSION}"

detail "Release ${VERSION}"
if [[ -x "${HOME}/.empryo/bin/empryo" ]]; then
  TITLE="Updating to ${VERSION}"
else
  TITLE="Installing ${VERSION}"
fi
LABEL="Found ${VERSION}"
PCT=3
hatch
if [[ -z "$USE_COLOR" && -z "$QUIET" ]]; then printf '%s\n' "$TITLE"; fi

# ── Download + verify ─────────────────────────────────────────────────
TMP_DIR="$(mktemp -d -t empryo-install.XXXXXX)"
cleanup() {
  rm -rf "$TMP_DIR"
  if [[ -n "$USE_COLOR" ]]; then printf '\033[?25h'; fi
}
trap cleanup EXIT INT TERM

# Download, verify, extract and run the bundled installer for the current
# $BUNDLE. A function because it can run twice: the CPU probe above can be
# wrong in both directions (containers masking cpuinfo flags the host has,
# exotic vCPU models), so when the bundled installer's smoke test reports the
# binary DIED ON A SIGNAL (its distinct exit 86) the caller retries once with
# the baseline build instead of leaving a core dump as the last word. NOTE:
# called via `|| rc=$?`, which suspends `set -e` inside — every command here
# carries its own `|| fail`.
content_length() {
  if [ "$DL" = curl ]; then
    curl -fsSIL --retry 2 --proto '=https' --tlsv1.2 "$1" 2>/dev/null \
      | awk 'tolower($1) == "content-length:" { v = $2 } END { gsub(/\r/, "", v); print v }'
  else
    wget -q --spider -S "$1" 2>&1 \
      | awk 'tolower($1) == "content-length:" { v = $2 } END { gsub(/\r/, "", v); print v }'
  fi
}
megabytes() { awk -v b="$1" 'BEGIN { printf "%.1f", b / 1048576 }'; }

# download <url> <dest> <from%> <to%> — the bar follows the bytes on disk
# against the server's Content-Length; plain mode prints every quarter.
download() {
  local url="$1" dest="$2" from="$3" to="$4" total size pid rc=0 mark=0 quarter=0
  total="$(content_length "$url" || true)"
  [[ "$total" =~ ^[0-9]+$ && "$total" -gt 0 ]] || total=""
  fetch_file "$url" "$dest" &
  pid=$!
  LABEL="Downloading"
  while kill -0 "$pid" 2>/dev/null; do
    size="$( { wc -c < "$dest"; } 2>/dev/null | tr -d ' ' || true)"
    [[ "$size" =~ ^[0-9]+$ ]] || size=0
    if [[ -n "$total" ]]; then
      PCT=$(( from + (to - from) * size / total ))
      LABEL="Downloading  $(megabytes "$size") of $(megabytes "$total") MB"
      quarter=$(( size * 4 / total ))
    elif (( PCT < to - 1 )); then
      PCT=$(( PCT + 1 ))
    fi
    if [[ -n "$USE_COLOR" ]]; then
      hatch
    elif [[ -z "$QUIET" && -n "$total" ]] && (( quarter > mark && quarter < 4 )); then
      mark=$quarter
      printf 'Downloading %d%%\n' $(( quarter * 25 ))
    fi
    sleep 0.08
  done
  wait "$pid" || rc=$?
  if (( rc != 0 )); then return "$rc"; fi
  PCT="$to"
  LABEL="Downloaded"
  if [[ -n "$USE_COLOR" ]]; then hatch; elif [[ -z "$QUIET" ]]; then printf 'Downloaded\n'; fi
}

# The bundled installer always writes plain lines into a log here, whatever
# its age, because its stdout is not a terminal. Its step lines move the bar;
# everything else is kept and shown under Mote once it settles.
BUNDLE_SEEN=0
BUNDLE_TARGET=80
read_bundle_log() {
  local line
  while IFS= read -r line; do
    BUNDLE_SEEN=$((BUNDLE_SEEN + 1))
    line="${line#"${line%%[![:space:]]*}"}"
    case "$line" in
      Seeding*) PCT=80; BUNDLE_TARGET=88; LABEL="Wiring your shell" ;;
      Wiring*) PCT=88; BUNDLE_TARGET=96; LABEL="Waking Empryo up" ;;
      Probing*) PCT=96; BUNDLE_TARGET=100; LABEL="Almost there" ;;
      Online*) PCT=100; LABEL="Ready" ;;
      "" | Empryo | empryo | *" is ready"* | "$ "* | "\$"*) ;;
      *) NOTES+=("$GL_NOTE $line") ;;
    esac
  done < <(sed -n "$((BUNDLE_SEEN + 1)),\$p" "$1" 2>/dev/null)
}

run_bundled_rich() {
  local log="${TMP_DIR}/bundle.log" pid rc=0
  BUNDLE_SEEN=0
  BUNDLE_TARGET=80
  LABEL="Placing the runtime"
  EMPRYO_PLAIN=1 bash "${TMP_DIR}/${BUNDLE}/install.sh" > "$log" 2>&1 < /dev/null &
  pid=$!
  while kill -0 "$pid" 2>/dev/null; do
    read_bundle_log "$log"
    if (( PCT < BUNDLE_TARGET - 1 )); then PCT=$(( PCT + (BUNDLE_TARGET - PCT + 15) / 16 )); fi
    hatch
    sleep 0.08
  done
  wait "$pid" || rc=$?
  read_bundle_log "$log"
  BUNDLE_LOG="$log"
  if (( rc != 0 )); then return "$rc"; fi
  PCT=100
  LABEL="Ready"
  hatch
}

install_bundle() {
  detail "Downloading ${BUNDLE}.tar.gz"
  download "${BASE_URL}/${BUNDLE}.tar.gz" "${TMP_DIR}/${BUNDLE}.tar.gz" 4 58 \
    || fail "download failed: ${BASE_URL}/${BUNDLE}.tar.gz"
  LABEL="Checking the signature"
  hatch

  if [[ -z "$NO_VERIFY" ]]; then
    fetch_file "${BASE_URL}/SHA256SUMS.txt" "${TMP_DIR}/SHA256SUMS.txt" \
      || fail "could not fetch SHA256SUMS.txt — refusing to install unverified binaries (set EMPRYO_NO_VERIFY=1 to override)"

    # Verify the detached RSA signature over SHA256SUMS.txt against the pinned
    # key BEFORE trusting any checksum it contains.
    command -v openssl >/dev/null 2>&1 \
      || fail "openssl is required to verify the release signature (set EMPRYO_NO_VERIFY=1 to skip — not recommended)"
    fetch_file "${BASE_URL}/SHA256SUMS.txt.sig" "${TMP_DIR}/SHA256SUMS.txt.sig" \
      || fail "could not fetch SHA256SUMS.txt.sig — refusing to install (set EMPRYO_NO_VERIFY=1 to override)"
    printf '%s\n' "$EMPRYO_SIGN_PUBKEY" > "${TMP_DIR}/empryo-sign.pub"
    openssl dgst -sha256 -verify "${TMP_DIR}/empryo-sign.pub" \
      -signature "${TMP_DIR}/SHA256SUMS.txt.sig" "${TMP_DIR}/SHA256SUMS.txt" >/dev/null 2>&1 \
      || fail "SHA256SUMS signature verification FAILED — refusing to install (possible tampering)"
    detail "Signature verified"

    EXPECTED="$(grep "  ${BUNDLE}.tar.gz\$" "${TMP_DIR}/SHA256SUMS.txt" | awk '{print $1}')" || true
    [[ -n "$EXPECTED" ]] || fail "no checksum entry for ${BUNDLE}.tar.gz in SHA256SUMS.txt"
    if command -v sha256sum >/dev/null 2>&1; then
      ACTUAL="$(sha256sum "${TMP_DIR}/${BUNDLE}.tar.gz" | awk '{print $1}')"
    else
      ACTUAL="$(shasum -a 256 "${TMP_DIR}/${BUNDLE}.tar.gz" | awk '{print $1}')"
    fi
    [[ "$ACTUAL" == "$EXPECTED" ]] || fail "checksum mismatch for ${BUNDLE}.tar.gz
    expected: ${EXPECTED}
    actual:   ${ACTUAL}
The download is corrupt or tampered with — refusing to install."
    step 64 "Signature and checksum verified"
  else
    warn "EMPRYO_NO_VERIFY=1 — installing UNVERIFIED binaries"
  fi

  # ── Extract + run the bundled installer ─────────────────────────────
  tar xzf "${TMP_DIR}/${BUNDLE}.tar.gz" -C "$TMP_DIR" &
  step 68 "Unpacked" $! || fail "could not extract ${BUNDLE}.tar.gz"
  [[ -x "${TMP_DIR}/${BUNDLE}/install.sh" ]] || fail "bundle is missing install.sh"

  # The bundled installer inherits this script's verdict about the terminal:
  # colour and the mark only where we already proved they are safe, plain line
  # output everywhere else (a pipe, CI, the TUI's own update flow).
  #
  # EMPRYO_QUIET on a piped UPGRADE is the compatibility lever. EMPRYO_PLAIN is
  # new, so a tarball built before this change ignores it and still animates a
  # block wordmark with cursor-up rewrites and a hidden cursor — straight into
  # whatever is reading the pipe. Every bundled installer ever shipped honours
  # --quiet, and on an upgrade its one cost (the PATH line) is already paid, so
  # an in-app update is clean no matter how old the build it is replacing.
  # A FRESH piped install keeps the full path: PATH setup is the whole point
  # there, and nothing is watching a Dockerfile's scrollback.
  if [[ -n "$QUIET" ]]; then
    EMPRYO_QUIET=1 EMPRYO_PLAIN=1 bash "${TMP_DIR}/${BUNDLE}/install.sh" --quiet
  elif [[ -z "$USE_COLOR" && -x "${HOME}/.empryo/bin/empryo" ]]; then
    EMPRYO_QUIET=1 EMPRYO_PLAIN=1 bash "${TMP_DIR}/${BUNDLE}/install.sh" --quiet
  elif [[ -z "$USE_COLOR" ]]; then
    EMPRYO_PLAIN=1 bash "${TMP_DIR}/${BUNDLE}/install.sh"
  else
    run_bundled_rich
  fi
}

INSTALL_RC=0
install_bundle || INSTALL_RC=$?
# 86 = the bundled installer's smoke test saw the binary die on a signal
# (SIGILL class): this machine cannot execute the standard build and the flag
# probe above missed it. One retry with the baseline build, which targets the
# x86_64 floor — never loops (baseline's own 86 falls through), and never
# second-guesses an explicit EMPRYO_ARCH pin. (#188)
if [[ "$INSTALL_RC" -eq 86 && "$PLATFORM" == "linux" && "$ARCH" == "x64" && -z "${EMPRYO_ARCH:-}" ]]; then
  warn "That build will not run on this CPU; retrying with the compatibility build"
  ARCH="x64-baseline"
  BUNDLE="empryo-${VERSION}-${PLATFORM}-${ARCH}"
  INSTALL_RC=0
  install_bundle || INSTALL_RC=$?
fi
if [[ "$INSTALL_RC" -ne 0 ]]; then
  if [[ -n "$USE_COLOR" && -n "${BUNDLE_LOG:-}" && -f "${BUNDLE_LOG:-}" ]]; then
    printf '\n'
    tail -n 20 "$BUNDLE_LOG" | while IFS= read -r line; do printf '  %s%s%s\n' "$D" "$line" "$X"; done
  fi
  exit "$INSTALL_RC"
fi

# ── Count the install ─────────────────────────────────────────────────
# One anonymous "+1": no id, no fields, no reply. It is how the download number
# on empryo.com stays true when old releases are deleted — the count lives in a
# permanent ledger rather than inside the artifact that was fetched. Skipped by
# DO_NOT_TRACK=1 or EMPRYO_NO_COUNT=1, and never allowed to fail the install.
if [ -z "${DO_NOT_TRACK:-}${EMPRYO_NO_COUNT:-}" ]; then
  if [ "$DL" = curl ]; then
    curl -fsS -m 3 "https://reach.empryo.com/hit?k=script" >/dev/null 2>&1 || true
  else
    wget -q -T 3 -O - "https://reach.empryo.com/hit?k=script" >/dev/null 2>&1 || true
  fi
fi

# ── Finale ────────────────────────────────────────────────────────────
# Mote blinks once at rest, then the one line that matters: what to type.
if [[ -n "$USE_COLOR" ]]; then
  for FRAME in 10 11 11 10 "$MOTE_REST"; do
    TICK=0
    block_draw
    sleep 0.09
  done
  printf '\033[?25h\n'
  printf '  %s%s%s %s%sEmpryo %s%s %sis ready%s\n' "$G" "$GL_OK" "$X" "$W" "$B" "$VERSION" "$X" "$D" "$X"
  for line in "${NOTES[@]+"${NOTES[@]}"}"; do printf '    %s%s%s\n' "$D" "$line" "$X"; done
  case ":${PATH}:" in
    *":${HOME}/.empryo/bin:"*) START_CMD="empryo" ;;
    *)
      case "$(basename "${SHELL:-bash}")" in
        zsh) START_CMD="source ~/.zshrc && empryo" ;;
        fish) START_CMD="source ~/.config/fish/config.fish; and empryo" ;;
        *) START_CMD="source ~/.bashrc && empryo" ;;
      esac
      ;;
  esac
  printf '\n  %s$%s %s%s%s%s\n\n' "$D" "$X" "$G" "$B" "$START_CMD" "$X"
fi
