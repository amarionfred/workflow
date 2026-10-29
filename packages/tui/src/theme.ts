// Lithos monochrome palette. Semantic roles retain their names so state text,
// symbols and layout remain independent of terminal color support.

export type ColorMode = "truecolor" | "256" | "16" | "none";

export function detectColorMode(env: NodeJS.ProcessEnv = process.env): ColorMode {
  if (env["NO_COLOR"] != null && env["NO_COLOR"] !== "") return "none";
  const term = env["TERM"] ?? "";
  if (term === "dumb" || term === "") return "none";
  const colorterm = env["COLORTERM"] ?? "";
  if (/truecolor|24bit/i.test(colorterm)) return "truecolor";
  if (/256color/.test(term)) return "256";
  return "16";
}

/** Semantic roles. Runtime token names retain upstream compatibility. */
export type Token =
  | "accent" | "accentBright" | "warn" | "error" | "ok" | "info"
  | "dim" | "bright" | "chrome" | "selection"
  | "actActive" | "actIdle" | "actDetached" | "actAttention"
  | "clawd" | "clawdEye" | "markInk" | "markBg" | "codexBlue";

// [truecolor rgb, xterm grayscale index, neutral 16-color SGR].
// Unpainted text and ground inherit the desktop terminal (#a6a6a6 / #080808).
const PALETTE: Record<Token, [[number, number, number], number, number]> = {
  accent: [[196, 196, 196], 251, 37],
  accentBright: [[224, 224, 224], 254, 97],
  warn: [[208, 208, 208], 252, 97],
  error: [[224, 224, 224], 254, 97],
  ok: [[166, 166, 166], 248, 37],
  info: [[184, 184, 184], 250, 37],
  dim: [[138, 138, 138], 245, 37],
  bright: [[224, 224, 224], 254, 97],
  chrome: [[61, 61, 61], 237, 90],
  selection: [[26, 26, 26], 234, 30],
  actActive: [[166, 166, 166], 248, 37],
  actIdle: [[138, 138, 138], 245, 37],
  actDetached: [[104, 104, 104], 242, 90],
  actAttention: [[208, 208, 208], 252, 97],
  clawd: [[176, 176, 176], 249, 37],
  clawdEye: [[24, 24, 24], 234, 30],
  markInk: [[192, 192, 192], 250, 97],
  markBg: [[8, 8, 8], 232, 30],
  codexBlue: [[184, 184, 184], 250, 37],
};

export interface Style {
  /** wrap text in the token's SGR (plus bold/inverse); identity in "none" mode */
  paint(token: Token, text: string, opts?: { bold?: boolean; inverse?: boolean; bg?: Token; blink?: boolean }): string;
  readonly mode: ColorMode;
}

export function createStyle(mode: ColorMode = detectColorMode()): Style {
  function open(token: Token, opts?: { bold?: boolean; inverse?: boolean; bg?: Token; blink?: boolean }): string {
    if (mode === "none") return "";
    const parts: string[] = [];
    if (opts?.bold) parts.push("1");
    if (opts?.blink) parts.push("5");
    if (opts?.inverse) parts.push("7");
    const [rgb, x256, basic] = PALETTE[token];
    if (mode === "truecolor") parts.push(`38;2;${rgb[0]};${rgb[1]};${rgb[2]}`);
    else if (mode === "256") parts.push(`38;5;${x256}`);
    else parts.push(String(basic));
    if (opts?.bg) {
      const [brgb, b256, bBasic] = PALETTE[opts.bg];
      if (mode === "truecolor") parts.push(`48;2;${brgb[0]};${brgb[1]};${brgb[2]}`);
      else if (mode === "256") parts.push(`48;5;${b256}`);
      // 16-color: fg code + 10 = the matching bg code (30-37→40-47, 90-97→100-107)
      else parts.push(String(bBasic + 10));
    }
    return `\x1b[${parts.join(";")}m`;
  }
  return {
    mode,
    paint(token, text, opts) {
      if (mode === "none" || text === "") return text;
      return `${open(token, opts)}${text}\x1b[0m`;
    },
  };
}

const ANSI_RE = /\x1b\[[0-9;]*m/g;

/** The stylize invariant: stripping a styled line returns the plain line —
 * styling can never change layout, widths, or hit coordinates. */
export function stripAnsi(text: string): string {
  return text.replace(ANSI_RE, "");
}
