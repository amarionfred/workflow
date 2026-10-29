import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";

const source = fs.readFileSync(new URL("./install.sh", import.meta.url), "utf8");
function fixture(t, options = {}) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "lithos install "));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  fs.mkdirSync(path.join(root, "scripts"));
  fs.mkdirSync(path.join(root, "packages/cli"), { recursive: true });
  fs.mkdirSync(path.join(root, "bin"));
  fs.mkdirSync(path.join(root, "global/@lithos/cli/scripts"), { recursive: true });
  fs.writeFileSync(path.join(root, "global/@lithos/cli/scripts/check-abi.mjs"), "");
  fs.writeFileSync(path.join(root, "package.json"), "{}");
  fs.writeFileSync(path.join(root, "packages/cli/package.json"), "{}");
  const script = path.join(root, "scripts/install.sh");
  fs.writeFileSync(script, source);
  fs.writeFileSync(path.join(root, "bin/node"), `#!/bin/sh\nif [ "$1" = --version ]; then printf '%s\\n' "\${TEST_VERSION:-v24.1.0}"; else printf 'abi:check\\n' >>"$TEST_LOG"; fi\n`, { mode: 0o755 });
  fs.writeFileSync(path.join(root, "bin/npm"), `#!/bin/sh\nprintf '%s\\n' "$*" >>"$TEST_LOG"\n[ "\${FAIL_STEP:-}" != "$*" ] || exit 42\nif [ "$*" = "root -g" ]; then printf '%s\\n' "$TEST_MODULES"; fi\n`, { mode: 0o755 });
  const env = { ...process.env, PATH: `${root}/bin:/usr/bin:/bin`, TEST_LOG: `${root}/calls`, TEST_MODULES: `${root}/global`, ...options };
  return { root, env, run: (...args) => spawnSync("/bin/sh", [script, ...args], { env, encoding: "utf8" }),
    calls: () => fs.existsSync(env.TEST_LOG) ? fs.readFileSync(env.TEST_LOG, "utf8").trim().split("\n") : [] };
}

test("dry run explains the plan without installing", t => {
  const f = fixture(t); const result = f.run("--dry-run");
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /nothing changed/i);
  assert.deepEqual(f.calls(), []);
});

test("builds and installs the selected checkout, including paths with spaces", t => {
  const f = fixture(t); const result = f.run();
  assert.equal(result.status, 0, result.stderr);
  assert.deepEqual(f.calls(), ["ci", "run build:package", `install -g --install-links ${f.root}/packages/cli`, "root -g", "abi:check"]);
});

test("rejects unsupported Node and stops after a failed build", t => {
  const old = fixture(t, { TEST_VERSION: "v26.0.0" });
  assert.notEqual(old.run().status, 0); assert.deepEqual(old.calls(), []);
  const broken = fixture(t, { FAIL_STEP: "run build:package" });
  assert.equal(broken.run().status, 42);
  assert.deepEqual(broken.calls(), ["ci", "run build:package"]);
});
