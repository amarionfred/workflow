import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";

const source = fs.readFileSync(new URL("./install-wsl.sh", import.meta.url), "utf8");
function fixture(t, options = {}) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "lithos-wsl-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const home = path.join(root, "home"), bin = path.join(root, "bin"), scripts = path.join(root, "scripts");
  fs.mkdirSync(path.join(home, ".nvm"), { recursive: true });
  fs.mkdirSync(bin); fs.mkdirSync(scripts);
  fs.writeFileSync(path.join(scripts, "install-wsl.sh"), source);
  fs.writeFileSync(path.join(scripts, "install.sh"), '#!/bin/sh\nprintf "install\\n" >> "$TEST_LOG"\n');
  fs.writeFileSync(path.join(home, ".nvm/nvm.sh"), 'nvm() { printf "nvm %s\\n" "$*" >> "$TEST_LOG"; }\n');
  for (const name of ["git", "curl", "tmux", "make", "g++", "python3", "npm"]) {
    fs.writeFileSync(path.join(bin, name), '#!/bin/sh\nexit 0\n', { mode: 0o755 });
  }
  fs.writeFileSync(path.join(bin, "node"), '#!/bin/sh\ncase "$1" in -p) echo "${TEST_NODE_PLATFORM:-linux}";; --version) echo v24.1.0;; esac\n', { mode: 0o755 });
  const env = { ...process.env, HOME: home, NVM_DIR: path.join(home, ".nvm"), PATH: `${bin}:/usr/bin:/bin`, WSL_DISTRO_NAME: "Ubuntu", TEST_LOG: path.join(root, "calls"), ...options };
  return { root, env, run: (...args) => spawnSync("/bin/bash", [path.join(scripts, "install-wsl.sh"), ...args], { env, encoding: "utf8" }),
    calls: () => fs.existsSync(env.TEST_LOG) ? fs.readFileSync(env.TEST_LOG, "utf8").trim().split("\n") : [] };
}

test("preview makes no changes", t => {
  const f = fixture(t); const result = f.run("--dry-run");
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /No changes made/);
  assert.deepEqual(f.calls(), []);
});

test("uses Linux Node 24 and installs the selected checkout", t => {
  const f = fixture(t); const result = f.run();
  assert.equal(result.status, 0, result.stderr);
  assert.deepEqual(f.calls(), ["nvm install 24", "nvm use 24", "install"]);
});

test("refuses a Windows Node executable before installing", t => {
  const f = fixture(t, { TEST_NODE_PLATFORM: "win32" }); const result = f.run();
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /inside Linux/);
  assert.deepEqual(f.calls(), ["nvm install 24", "nvm use 24"]);
});

test("stops if nvm cannot be downloaded", t => {
  const f = fixture(t);
  fs.unlinkSync(path.join(f.env.NVM_DIR, "nvm.sh"));
  fs.writeFileSync(path.join(f.root, "bin/curl"), '#!/bin/sh\nexit 7\n', { mode: 0o755 });
  const result = f.run();
  assert.notEqual(result.status, 0);
  assert.deepEqual(f.calls(), []);
});
