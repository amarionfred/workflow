#!/usr/bin/env python3
"""Capture explicitly selected workflow files without touching installed sources."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import tomllib


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "setup-snapshot"
HOME = Path.home()
SKIP = {".git", ".system", "node_modules", ".venv", "venv", "__pycache__",
        ".cache", ".empryo", ".DS_Store"}


def main():
    manifest_path = SNAPSHOT / "manifest.json"
    entries = {item["name"]: item for item in json.loads(manifest_path.read_text())}

    def record(destination, source, selection=None):
        name = destination.relative_to(SNAPSHOT).as_posix()
        entries[name] = {
            "name": name,
            "source": str(source),
            "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
        }
        if selection is not None:
            entries[name]["selected_fields"] = selection

    def copy(source, destination):
        if source.is_symlink():
            raise ValueError(f"Review symbolic link before snapshotting: {source}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        record(destination, source)

    def tree(source, destination):
        for base, directories, files in os.walk(source):
            directories[:] = sorted(d for d in directories if d not in SKIP)
            for directory in directories:
                if (Path(base) / directory).is_symlink():
                    raise ValueError(f"Review symbolic link: {Path(base) / directory}")
            for name in sorted(files):
                if name in SKIP or name.endswith((".pyc", ".pyo")):
                    continue
                path = Path(base) / name
                copy(path, destination / path.relative_to(source))

    # Refresh the original launchers, theme, adapter, model roles, and timer units.
    for name in (
        "agent-desk", "agent-workflow", "agent-scientist", "koda.json",
        "empryo-koda.desktop", "pstack-CODEX.md", "pstack-models.md",
        "agent-workflow-health.service", "agent-workflow-health.timer",
        "agent-workflow-review.service", "agent-workflow-review.timer",
    ):
        copy(Path(entries[name]["source"]), SNAPSHOT / name)

    for name in ("pstack", "park-workflow", "prison-production"):
        tree(HOME / "plugins" / name, SNAPSHOT / "plugins" / name)
    tree(HOME / ".codex/skills", SNAPSHOT / "skills")
    tree(HOME / "Documents/agent-brain", SNAPSHOT / "agent-brain")
    copy(HOME / ".codex/AGENTS.md", SNAPSHOT / "codex-AGENTS.md")
    copy(HOME / ".agents/plugins/marketplace.json", SNAPSHOT / "personal-marketplace.json")
    copy(HOME / ".config/systemd/user/docker.service", SNAPSHOT / "docker.service")

    # Export only the workflow settings, never the complete provider/MCP config.
    source = HOME / ".codex/config.toml"
    config = tomllib.loads(source.read_text())
    selected = ["approval_policy", "sandbox_mode", "model", "model_reasoning_effort"]
    lines = ["# Selected workflow settings; merge into the existing config."]
    lines += [f"{key} = {json.dumps(config[key])}" for key in selected]
    for name in ("pstack@personal", "park-workflow@personal", "prison-production@personal"):
        enabled = config["plugins"][name]["enabled"]
        lines += ["", f"[plugins.{json.dumps(name)}]", f"enabled = {str(enabled).lower()}"]
    destination = SNAPSHOT / "codex-workflow.toml"
    destination.write_text("\n".join(lines) + "\n")
    tomllib.loads(destination.read_text())
    record(destination, source, selected + ["plugins.*@personal.enabled"])

    source = HOME / ".empryo/config.json"
    config = json.loads(source.read_text())
    selected = ["chatLayout", "defaultModel", "diffStyle", "nerdFont", "notifyTurns", "theme"]
    destination = SNAPSHOT / "empryo-workflow.json"
    destination.write_text(json.dumps({key: config[key] for key in selected if key in config}, indent=2) + "\n")
    record(destination, source, selected)

    manifest_path.write_text(json.dumps([entries[key] for key in sorted(entries)], indent=2) + "\n")
    print(f"Captured {len(entries)} files in {SNAPSHOT}")


if __name__ == "__main__":
    main()
