import { describe, expect, it } from "vitest";
import { createViewState } from "../src/state.js";
import { parseCommand } from "../src/grammar.js";
import { renderScreen } from "../src/render.js";
import { demoSnapshot } from "../src/demo-data.js";
import { createStyle, stripAnsi, detectColorMode } from "../src/theme.js";
import { stylizeLines } from "../src/stylize.js";

// Founder visual-polish directive: styling is a zero-width post-pass. The
// LOAD-BEARING invariant: stripAnsi(styled[i]) === plain[i] for EVERY line of
// EVERY view — color can never move a hit target, change a width, or shear a
// frame (the stable-frame guarantee stays proven).

const snap = demoSnapshot();

function screenFor(...commands: string[]) {
  const s = createViewState({ instanceId: "t", getSnapshot: () => snap });
  for (const c of commands) s.dispatch(parseCommand(c));
  return renderScreen(s.get(), snap, { cols: 140, rows: 34 });
}

const VIEWS: Array<[string, string[]]> = [
  ["topology table", ["rig openrig-build"]],
  ["topology overview", ["rig openrig-build", "tab overview"]],
  ["agent detail", ["agent dev50.driver"]],
  ["specs library", [":specs"]],
  ["rig spec", ["spec openrig-build-rig"]],
  ["agent spec", ["spec driver-agent"]],
  ["needs", [":needs"]],
  ["cross-nav running", ["running driver-agent"]],
  ["filtered", ["rig openrig-build", "/dev50"]],
  ["named error", ["agent nobody.here"]],
];

describe("stylize invariant: strip(styled) === plain, every view, every mode", () => {
  for (const mode of ["truecolor", "256", "16"] as const) {
    it(`holds in ${mode} mode across all views`, () => {
      const style = createStyle(mode);
      for (const [name, commands] of VIEWS) {
        const screen = screenFor(...commands);
        const styled = stylizeLines(screen, style);
        expect(styled.length, name).toBe(screen.lines.length);
        for (let i = 0; i < styled.length; i++) {
          expect(stripAnsi(styled[i]!), `${name} line ${i + 1} (${mode})`).toBe(screen.lines[i]!);
        }
      }
    });
  }

  it("none mode returns the plain lines untouched (NO_COLOR honesty)", () => {
    const screen = screenFor("rig openrig-build");
    expect(stylizeLines(screen, createStyle("none"))).toEqual(screen.lines);
  });

  it("emits only neutral ink in every supported color mode across the views", () => {
    for (const [, commands] of VIEWS) {
      const screen = screenFor(...commands);
      const rgb = stylizeLines(screen, createStyle("truecolor")).join("\n");
      for (const match of rgb.matchAll(/(?:38|48);2;(\d+);(\d+);(\d+)/g)) {
        expect(match[1]).toBe(match[2]);
        expect(match[2]).toBe(match[3]);
      }
      const indexed = stylizeLines(screen, createStyle("256")).join("\n");
      for (const match of indexed.matchAll(/(?:38|48);5;(\d+)/g)) {
        expect(Number(match[1])).toBeGreaterThanOrEqual(232);
        expect(Number(match[1])).toBeLessThanOrEqual(255);
      }
      const basic = stylizeLines(screen, createStyle("16")).join("\n");
      for (const match of basic.matchAll(/\x1b\[([0-9;]+)m/g)) {
        for (const code of match[1]!.split(";").map(Number)) {
          expect([0, 1, 5, 7, 30, 37, 40, 47, 90, 97, 100, 107]).toContain(code);
        }
      }
    }
  });
});

describe("Lithos monochrome treatment", () => {
  const style = createStyle("truecolor");

  it("keeps status words distinct with neutral emphasis", () => {
    const styled = stylizeLines(screenFor("rig openrig-build"), style).join("\n");
    expect(styled).toContain("\x1b[38;2;166;166;166mworking\x1b[0m");
    expect(styled).toContain("\x1b[38;2;208;208;208mneeds you\x1b[0m");
    expect(styled).toContain("\x1b[38;2;138;138;138munknown\x1b[0m");
  });

  it("paints selection as an inverse accent bar (visible highlight, not just a glyph)", () => {
    const styled = stylizeLines(screenFor(), style);
    const bar = styled.find((l) => l.includes("\x1b[1;38;2;196;196;196;48;2;26;26;26m"));
    expect(bar).toBeDefined();
    expect(stripAnsi(bar!)).toMatch(/^▶/);
  });

  it("links/acts get the neutral accent (term ▸, open ▸, tabs)", () => {
    const styled = stylizeLines(screenFor("rig openrig-build"), style).join("\n");
    expect(styled).toContain("\x1b[1;38;2;196;196;196mterm ▸\x1b[0m");
    expect(styled).toContain("\x1b[1;38;2;196;196;196mOpen terminals ▸\x1b[0m");
  });

  it("Attention styling preserves unavailable truth without legacy fleet alerts", () => {
    const styled = stylizeLines(screenFor(":needs"), style).join("\n");
    expect(stripAnsi(styled)).toContain("Unavailable: Feed");
    expect(stripAnsi(styled)).not.toContain("✖ remote-host");
    expect(styled).not.toMatch(/\x1b\[5;38;2;208;208;208m⚑/);
  });

  it("chrome rules carry pane titles; hint bar and status line are styled", () => {
    const styled = stylizeLines(screenFor("rig openrig-build"), style);
    expect(stripAnsi(styled[1]!)).toMatch(/EXPLORER.*╋.*TOPOLOGY/);
    const hint = styled.find((l) => stripAnsi(l).includes("q quit"));
    expect(hint).toBeDefined();
    expect(hint).toContain("\x1b[");
  });

  it("16-color mode emits only basic SGR (no 38;2 / 38;5) — sane degradation", () => {
    const styled = stylizeLines(screenFor("rig openrig-build"), createStyle("16")).join("\n");
    expect(styled).not.toContain("38;2;");
    expect(styled).not.toContain("38;5;");
    expect(styled).toContain("\x1b[");
  });

  it("256 mode uses 38;5 indexed colors", () => {
    const styled = stylizeLines(screenFor("rig openrig-build"), createStyle("256")).join("\n");
    expect(styled).toContain("38;5;");
    expect(styled).not.toContain("38;2;");
  });
});

describe("color-mode detection", () => {
  it("honors NO_COLOR, dumb terms, COLORTERM and 256color TERM", () => {
    expect(detectColorMode({ NO_COLOR: "1", TERM: "xterm-256color" })).toBe("none");
    expect(detectColorMode({ TERM: "dumb" })).toBe("none");
    expect(detectColorMode({ TERM: "xterm-256color", COLORTERM: "truecolor" })).toBe("truecolor");
    expect(detectColorMode({ TERM: "xterm-256color" })).toBe("256");
    expect(detectColorMode({ TERM: "xterm" })).toBe("16");
  });
});
