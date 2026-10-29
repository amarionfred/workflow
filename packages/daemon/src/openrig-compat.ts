import { existsSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const warnedKeys = new Set<string>();

export function getOpenRigHome(): string {
  const configured = readOpenRigEnv("OPENRIG_HOME", "RIGGED_HOME");
  if (configured !== undefined) return configured;
  const lithosHome = join(homedir(), ".lithos");
  const previousHome = join(homedir(), ".openrig");
  // Keep an existing instance in place; fresh installations use the Lithos name.
  return existsSync(lithosHome) || !existsSync(previousHome) ? lithosHome : previousHome;
}

export function getLegacyRiggedHome(): string {
  return join(homedir(), ".rigged");
}

export const OPENRIG_HOME = getOpenRigHome();
export const LEGACY_RIGGED_HOME = getLegacyRiggedHome();

function warnOnce(key: string, message: string): void {
  if (warnedKeys.has(key)) return;
  warnedKeys.add(key);
  console.warn(message);
}

export function readOpenRigEnv(primary: string, legacy?: string): string | undefined {
  const lithosKey = primary === "OPENRIG_HOME" ? "LITHOS_HOME" : primary;
  const lithosValue = process.env[lithosKey];
  if (lithosValue !== undefined && lithosValue !== "") return lithosValue;

  const primaryValue = process.env[primary];
  if (primaryValue !== undefined && primaryValue !== "") return primaryValue;

  if (legacy) {
    const legacyValue = process.env[legacy];
    if (legacyValue !== undefined && legacyValue !== "") {
      warnOnce(`env:${legacy}`, `Warning: ${legacy} is deprecated; use ${primary} instead.`);
      return legacyValue;
    }
  }

  return undefined;
}

export function getPreferredOpenRigHome(): string {
  const openrigHome = getOpenRigHome();
  const legacyRiggedHome = getLegacyRiggedHome();

  if (existsSync(openrigHome)) return openrigHome;
  if (existsSync(legacyRiggedHome)) {
    warnOnce(
      "path:home",
      `Warning: using legacy state directory ${legacyRiggedHome}; migrate to ${openrigHome}.`,
    );
    return legacyRiggedHome;
  }
  return openrigHome;
}

export function getDefaultOpenRigPath(filename: string): string {
  return join(getOpenRigHome(), filename);
}

export function getCompatibleOpenRigPath(filename: string): string {
  const openrigHome = getOpenRigHome();
  const legacyRiggedHome = getLegacyRiggedHome();
  const primaryPath = join(openrigHome, filename);
  if (existsSync(primaryPath)) return primaryPath;

  const legacyPath = join(legacyRiggedHome, filename);
  if (existsSync(legacyPath)) {
    warnOnce(
      `path:${filename}`,
      `Warning: using legacy state path ${legacyPath}; migrate to ${primaryPath}.`,
    );
    return legacyPath;
  }

  return primaryPath;
}
