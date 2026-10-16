#!/usr/bin/env python3
"""Build the local Codex port from a pinned, unmodified pstack checkout."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'vendor/cursor-plugins/pstack'
DEST = Path.home() / 'plugins/pstack'

def main():
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=SOURCE, text=True).strip()
    for name in ['skills', 'agents', 'automations', 'docs', 'assets']:
        shutil.copytree(SOURCE / name, DEST / name, dirs_exist_ok=True)
    shutil.copy2(SOURCE / 'LICENSE', DEST / 'LICENSE')
    shutil.copy2(SOURCE / 'README.md', DEST / 'UPSTREAM-README.md')
    inventory = []
    for source in sorted(SOURCE.rglob('*')):
        if source.is_file():
            inventory.append({'path':str(source.relative_to(SOURCE)), 'sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
    for file in list((DEST / 'skills').rglob('*.md')) + list((DEST / 'automations').rglob('*.md')) + list((DEST / 'agents').rglob('*.md')):
        text = file.read_text()
        text = text.replace('~/.cursor/skills/', '~/.codex/skills/').replace('.cursor/skills/', '.agents/skills/')
        text = text.replace('~/.cursor/rules/pstack-models.mdc', '~/.config/agentic-workflow/pstack-models.md')
        text = text.replace("Cursor's built-in `create-skill`", "Codex's `skill-creator`")
        if file.name == 'SKILL.md':
            parts = text.split('---', 2)
            if len(parts) != 3:
                raise ValueError(f'No frontmatter: {file}')
            front, body = parts[1], parts[2]
            description = re.search(r'^description:\s*(.*(?:\n[ \t]+.*)*)', front, re.M)
            if not description:
                raise ValueError(f'No description: {file}')
            name = file.parent.name
            explicit = 'disable-model-invocation: true' in front
            new_front = f'---\nname: {name}\ndescription: {description.group(1)}\n---\n'
            relative = Path(__import__('os').path.relpath(DEST / 'CODEX.md', file.parent))
            text = new_front + f'\nRead [{relative}]({relative}) before applying this skill. It maps the upstream workflow to the available Codex tools.\n' + body
            if explicit:
                metadata = file.parent / 'agents/openai.yaml'
                metadata.parent.mkdir(exist_ok=True)
                metadata.write_text(f'interface:\n  display_name: {json.dumps(name)}\n  short_description: "Apply the pstack {name.removeprefix("principle-")} workflow"\npolicy:\n  allow_implicit_invocation: false\n')
        file.write_text(text)
    extras = []
    for original in sorted((DEST / 'automations/benny/skills').glob('*/SKILL.md')):
        name = original.parent.name
        target = DEST / 'skills' / name
        target.mkdir(exist_ok=True)
        desc = {'setup-benny':'Set up the Benny issue triage and reproduction workflow for an explicitly selected repository and tracker.',
                'triage-issue-reports':'Deduplicate and classify bug reports with source evidence and a configured issue tracker.',
                'reproduce-and-fix-issues':'Reproduce queued issues in the real application, fix confirmed defects, and verify the result.'}[name]
        target.joinpath('SKILL.md').write_text(f'---\nname: {name}\ndescription: {desc}\n---\n\nRead [Codex compatibility](../../CODEX.md), then follow the complete [upstream workflow](../../automations/benny/skills/{name}/SKILL.md). Keep the pack-relative template and reference paths relative to that original file.\n')
        (target / 'agents').mkdir(exist_ok=True)
        (target / 'agents/openai.yaml').write_text(f'interface:\n  display_name: {json.dumps(name)}\n  short_description: "Apply the Benny issue automation workflow"\npolicy:\n  allow_implicit_invocation: false\n')
        extras.append(name)
    manifest = json.loads((SOURCE / 'plugin.json').read_text())
    manifest.pop('$schema', None)
    manifest['version'] += '+codex.1'
    manifest['skills'] = './skills/'
    manifest['description'] = "Lauren Tan's complete public pstack, with a local Codex compatibility layer."
    manifest['interface'] = {'displayName':'pstack · Codex', 'shortDescription':'Lauren Tan’s engineering workflows, adapted for Codex.', 'longDescription':'All 54 public core skills, 23 playbooks, and 3 Benny automation skills. Includes model and tool mapping for Codex; preserves upstream sources and MIT attribution.', 'developerName':'Lauren Tan; local Codex adaptation for Park', 'category':'Productivity', 'capabilities':['Interactive','Write'], 'defaultPrompt':['Use poteto-mode to implement and verify this task.', 'Use sharpen to improve my task brief.', 'Use correct to prevent a repeated failure.'], 'brandColor':'#a6a6a6', 'logo':'./assets/logo.png'}
    (DEST / '.codex-plugin/plugin.json').write_text(json.dumps(manifest, indent=2)+'\n')
    record = {'repository':'https://github.com/cursor/plugins', 'commit':commit, 'upstream_version':manifest['version'].split('+')[0], 'core_skills':len(list((SOURCE/'skills').glob('*/SKILL.md'))), 'automation_skills':extras, 'source_files':inventory}
    (DEST / 'PROVENANCE.json').write_text(json.dumps(record, indent=2)+'\n')
    (ROOT / 'evidence/pstack-provenance.json').write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k!='source_files'}, indent=2))

if __name__ == '__main__':
    main()
