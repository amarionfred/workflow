import { afterEach, describe, expect, it, vi } from "vitest";
import { mkdtempSync, mkdirSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const ORIGINAL_LITHOS_HOME = process.env.LITHOS_HOME;
const ORIGINAL_OPENRIG_HOME = process.env.OPENRIG_HOME;
const ORIGINAL_RIGGED_HOME = process.env.RIGGED_HOME;

afterEach(() => {
  if (ORIGINAL_LITHOS_HOME === undefined) delete process.env.LITHOS_HOME;
  else process.env.LITHOS_HOME = ORIGINAL_LITHOS_HOME;
  if (ORIGINAL_OPENRIG_HOME === undefined) delete process.env.OPENRIG_HOME;
  else process.env.OPENRIG_HOME = ORIGINAL_OPENRIG_HOME;

  if (ORIGINAL_RIGGED_HOME === undefined) delete process.env.RIGGED_HOME;
  else process.env.RIGGED_HOME = ORIGINAL_RIGGED_HOME;

  vi.resetModules();
  vi.restoreAllMocks();
});

describe("openrig-compat", () => {
  it("prefers LITHOS_HOME while accepting the existing home setting", async () => {
    process.env.LITHOS_HOME = "/tmp/lithos-home";
    process.env.OPENRIG_HOME = "/tmp/existing-home";
    const mod = await import("../src/openrig-compat.js");
    expect(mod.getOpenRigHome()).toBe("/tmp/lithos-home");
    delete process.env.LITHOS_HOME;
    expect(mod.getOpenRigHome()).toBe("/tmp/existing-home");
  });
  it("uses a Lithos home for new installs and keeps an existing home", async () => {
    const originalHome = process.env.HOME;
    const dir = mkdtempSync(join(tmpdir(), "lithos-home-test-"));
    try {
      process.env.HOME = dir;
      delete process.env.LITHOS_HOME;
      delete process.env.OPENRIG_HOME;
      delete process.env.RIGGED_HOME;
      const mod = await import("../src/openrig-compat.js");
      expect(mod.getOpenRigHome()).toBe(join(dir, ".lithos"));
      mkdirSync(join(dir, ".openrig"));
      expect(mod.getOpenRigHome()).toBe(join(dir, ".openrig"));
      mkdirSync(join(dir, ".lithos"));
      expect(mod.getOpenRigHome()).toBe(join(dir, ".lithos"));
    } finally {
      if (originalHome === undefined) delete process.env.HOME;
      else process.env.HOME = originalHome;
      rmSync(dir, { recursive: true, force: true });
    }
  });

  it("getOpenRigHome prefers OPENRIG_HOME when set", async () => {
    delete process.env.LITHOS_HOME;
    process.env.OPENRIG_HOME = "/tmp/custom-openrig-home";
    delete process.env.RIGGED_HOME;

    const mod = await import("../src/openrig-compat.js");

    expect(mod.getOpenRigHome()).toBe("/tmp/custom-openrig-home");
    expect(mod.getDefaultOpenRigPath("daemon.json")).toBe("/tmp/custom-openrig-home/daemon.json");
  });

  it("getOpenRigHome falls back to RIGGED_HOME with warning", async () => {
    delete process.env.LITHOS_HOME;
    delete process.env.OPENRIG_HOME;
    process.env.RIGGED_HOME = "/tmp/legacy-rigged-home";
    const warnSpy = vi.spyOn(console, "warn").mockImplementation(() => {});

    const mod = await import("../src/openrig-compat.js");

    expect(mod.getOpenRigHome()).toBe("/tmp/legacy-rigged-home");
    expect(warnSpy).toHaveBeenCalledWith(
      "Warning: RIGGED_HOME is deprecated; use OPENRIG_HOME instead.",
    );
  });
});
