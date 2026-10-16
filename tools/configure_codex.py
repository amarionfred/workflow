#!/usr/bin/env python3
"""Apply the user's requested full-access defaults, retaining an exact backup."""
from pathlib import Path
from datetime import datetime, timezone
import json
import re
import shutil
import tomllib

root = Path.home() / '.codex'
config = root / 'config.toml'
before = config.read_text()
data = tomllib.loads(before)
if data.get('approval_policy') != 'never' or data.get('sandbox_mode') != 'danger-full-access':
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup = root / 'backups' / ('agentic-workflow-' + stamp)
    backup.mkdir(parents=True, exist_ok=False)
    shutil.copy2(config, backup / 'config.toml')
    lines = before.splitlines(keepends=True)
    in_top = True
    kept = []
    for line in lines:
        if line.lstrip().startswith('['): in_top = False
        if in_top and re.match(r'\s*(approval_policy|sandbox_mode|default_permissions)\s*=', line): continue
        kept.append(line)
    after = '# Full access requested by Park, 2026-10-16. Applies to new sessions.\napproval_policy = "never"\nsandbox_mode = "danger-full-access"\n' + ''.join(kept)
    parsed = tomllib.loads(after)
    assert parsed['model'] == data['model']
    assert parsed.get('mcp_servers') == data.get('mcp_servers')
    config.write_text(after)
    print('Backup:', backup)
else:
    print('Full-access defaults already configured.')
guidance = root / 'AGENTS.md'
content = '''# Park's working preferences

For substantial engineering work, use the installed pstack poteto-mode workflow when it fits. Read its CODEX.md adapter before applying Cursor-specific instructions. Keep small tasks direct.

Personal context and project pointers live in `/home/park/Documents/agent-brain/AGENTS.md`. Read the index only when prior context, a standing project, a correction, or a handoff matters; retrieve the relevant topic rather than the whole archive. Project AGENTS.md files and canonical research records remain authoritative.

Own the requested outcome through verification. State assumptions that affect the result, keep a short decision trail for long runs, and continue authorized independent work when one branch is blocked. Ask only for decisions or access that cannot be inferred or obtained from the available evidence. Existing authorization persists.

Teach alongside delivery when Park asks to learn. Explain what changed, why, how to use it, and what observable check supports it. Offer a small prediction or exercise; distinguish Park's contributions from agent-written work.

After a demonstrated repeat failure, prefer a structural fix or executable check. Put project facts in the project record, general methods in skills, and personal preferences in the knowledge base. Do not add broad rules from a single accident.

Use the current session's real tools, limits, and permissions. Full-access settings do not imply that a tool is available, a computer stays awake, or an external action is authorized. Never report a saved prompt as a running automation or an installation as proven productivity.
'''
if guidance.exists() and guidance.read_text() != content:
    raise SystemExit('AGENTS.md exists with other content; merge it deliberately instead of overwriting.')
guidance.write_text(content)
print(json.dumps({k:tomllib.loads(config.read_text())[k] for k in ['approval_policy','sandbox_mode','model','model_reasoning_effort']}))
