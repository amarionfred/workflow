// OPR.0.4.3.29 — dashboard theming: registry + resolution + persistence + no-FOUC
// contract + provider/selector behavior. Proves the AC-level guarantees:
//  - switch applies (the .dark class toggles on <html>) and persists across reload
//  - fresh sessions use Lithos dark; explicit light/system remain available
//  - pre-paint and provider paths resolve the same preference
//  - an explicit choice wins over the OS
//  - extensibility: the selector is registry-driven (adding a theme is data-only)

import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { render, screen, cleanup, fireEvent, act } from "@testing-library/react";
import {
  THEME_STORAGE_KEY,
  THEMES,
  DEFAULT_THEME,
  readStoredTheme,
  writeStoredTheme,
  resolveTheme,
  applyTheme,
} from "../src/lib/theme.js";
import { ThemeProvider, useTheme } from "../src/components/ThemeProvider.js";
import { ThemeSelector } from "../src/components/ThemeSelector.js";

/** Override window.matchMedia so `(prefers-color-scheme: dark)` reports `osDark`. */
function mockOsDark(osDark: boolean) {
  Object.defineProperty(window, "matchMedia", {
    configurable: true,
    value: (query: string) => ({
      matches: query.includes("dark") ? osDark : false,
      media: query,
      onchange: null,
      addListener: () => {},
      removeListener: () => {},
      addEventListener: () => {},
      removeEventListener: () => {},
      dispatchEvent: () => false,
    }),
  });
}

describe("theme lib — registry + resolution", () => {
  beforeEach(() => {
    localStorage.clear();
    document.documentElement.classList.remove("dark");
    mockOsDark(false);
  });
  afterEach(cleanup);

  it("registry ships light + dark + system", () => {
    const ids = THEMES.map((t) => t.id);
    expect(ids).toEqual(["light", "dark", "system"]);
  });

  it("default is `dark` when nothing is stored", () => {
    expect(readStoredTheme()).toBe(DEFAULT_THEME);
    expect(DEFAULT_THEME).toBe("dark");
  });

  it("reads an explicit stored choice; ignores malformed values", () => {
    writeStoredTheme("dark");
    expect(readStoredTheme()).toBe("dark");
    localStorage.setItem(THEME_STORAGE_KEY, "chartreuse");
    expect(readStoredTheme()).toBe("dark"); // falls back to default
  });

  it("`system` follows the OS; explicit light/dark ignore it", () => {
    mockOsDark(true);
    expect(resolveTheme("system")).toBe("dark");
    expect(resolveTheme("light")).toBe("light"); // explicit wins over OS-dark
    mockOsDark(false);
    expect(resolveTheme("system")).toBe("light");
    expect(resolveTheme("dark")).toBe("dark"); // explicit wins over OS-light
  });

  it("applyTheme toggles the .dark class on <html>", () => {
    applyTheme("dark");
    expect(document.documentElement.classList.contains("dark")).toBe(true);
    applyTheme("light");
    expect(document.documentElement.classList.contains("dark")).toBe(false);
    mockOsDark(true);
    applyTheme("system");
    expect(document.documentElement.classList.contains("dark")).toBe(true);
  });

  it("pre-paint and provider agree for fresh, invalid and explicit preferences", () => {
    const html = readFileSync(resolve(__dirname, "../index.html"), "utf8");
    const script = html.match(/<script>([\s\S]*?)<\/script>/)![1]!;
    const prepaint = new Function("document", "window", "localStorage", script);
    for (const osDark of [false, true]) {
      mockOsDark(osDark);
      for (const stored of [null, "invalid", "dark", "light", "system"]) {
        localStorage.clear();
        if (stored !== null) localStorage.setItem(THEME_STORAGE_KEY, stored);
        const expected = resolveTheme(readStoredTheme()) === "dark";
        document.documentElement.classList.remove("dark");
        prepaint(document, window, localStorage);
        expect(document.documentElement.classList.contains("dark")).toBe(expected);
      }
    }
    document.documentElement.classList.remove("dark");
    prepaint(document, window, { getItem() { throw new Error("storage unavailable"); } });
    expect(document.documentElement.classList.contains("dark")).toBe(true);
  });
});

function Probe() {
  const { theme, resolved } = useTheme();
  return (
    <span data-testid="probe">
      {theme}:{resolved}
    </span>
  );
}

describe("ThemeProvider + ThemeSelector", () => {
  beforeEach(() => {
    localStorage.clear();
    document.documentElement.classList.remove("dark");
    mockOsDark(false);
  });
  afterEach(cleanup);

  it("first load with no stored choice uses Lithos dark even on a light OS", () => {
    mockOsDark(false);
    render(
      <ThemeProvider>
        <Probe />
      </ThemeProvider>,
    );
    expect(screen.getByTestId("probe").textContent).toBe("dark:dark");
    expect(document.documentElement.classList.contains("dark")).toBe(true);
  });

  it("an explicit stored choice wins over the OS", () => {
    writeStoredTheme("light");
    mockOsDark(true); // OS says dark, stored says light
    render(
      <ThemeProvider>
        <Probe />
      </ThemeProvider>,
    );
    expect(screen.getByTestId("probe").textContent).toBe("light:light");
    expect(document.documentElement.classList.contains("dark")).toBe(false);
  });

  it("selecting dark applies it and persists across a reload (remount)", () => {
    const { unmount } = render(
      <ThemeProvider>
        <ThemeSelector />
        <Probe />
      </ThemeProvider>,
    );
    act(() => {
      fireEvent.change(screen.getByTestId("theme-selector"), { target: { value: "dark" } });
    });
    expect(document.documentElement.classList.contains("dark")).toBe(true);
    expect(localStorage.getItem(THEME_STORAGE_KEY)).toBe("dark");

    // Simulate a reload: unmount + remount reads the persisted choice.
    unmount();
    document.documentElement.classList.remove("dark");
    render(
      <ThemeProvider>
        <Probe />
      </ThemeProvider>,
    );
    expect(screen.getByTestId("probe").textContent).toBe("dark:dark");
    expect(document.documentElement.classList.contains("dark")).toBe(true);
  });

  it("the selector is registry-driven — one <option> per registered theme (extensibility)", () => {
    render(
      <ThemeProvider>
        <ThemeSelector />
      </ThemeProvider>,
    );
    const options = screen.getByTestId("theme-selector").querySelectorAll("option");
    expect(options).toHaveLength(THEMES.length);
    expect(Array.from(options).map((o) => o.getAttribute("value"))).toEqual(
      THEMES.map((t) => t.id),
    );
  });
});
