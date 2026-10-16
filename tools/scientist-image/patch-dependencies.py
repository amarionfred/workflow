"""Apply and verify a narrowly scoped dependency update in the local image."""
from pathlib import Path
import json
import subprocess

root = Path('/opt/headless')
lock = root / 'package-lock.json'
before = json.loads(lock.read_text())
subprocess.run(['npm', 'pkg', 'set', 'overrides.@grpc/grpc-js=1.14.5',
                'overrides.smol-toml=1.9.0'], check=True, cwd=root)
subprocess.run(['npm', 'install', '--ignore-scripts', '--omit=dev', '--no-audit'],
               check=True, cwd=root)
after = json.loads(lock.read_text())
changes = []
for name in sorted(set(before['packages']) | set(after['packages'])):
    old = before['packages'].get(name, {}).get('version')
    new = after['packages'].get(name, {}).get('version')
    if old != new:
        changes.append({'package': name, 'before': old, 'after': new})
expected = {
    'node_modules/@grpc/grpc-js': ('1.14.4', '1.14.5'),
    'node_modules/smol-toml': ('1.6.1', '1.9.0'),
}
assert {x['package']: (x['before'], x['after']) for x in changes} == expected, changes
for agent in ('codex', 'claude', 'opencode', 'pi'):
    subprocess.run(['headless', agent, '--debug', '--usage', '--allow', 'yolo',
                    '--print-command', '--prompt', 'runtime-contract-smoke'],
                   check=True, stdout=subprocess.DEVNULL, timeout=30)
audit = subprocess.run(['npm', 'audit', '--omit=dev', '--json'], cwd=root,
                       capture_output=True, text=True, timeout=60)
report = json.loads(audit.stdout)
assert audit.returncode == 0, report
result = {'changes': changes, 'production_audit': report,
          'command_contracts': ['codex', 'claude', 'opencode', 'pi'],
          'model_calls': 0}
(root / 'park-dependency-update.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
