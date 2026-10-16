#!/usr/bin/env python3
"""Exercise record persistence and observable setup outputs without LLM calls."""
from pathlib import Path
import argparse
import importlib.util
import json
import subprocess
import tempfile
import sys

root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'tools'))
spec=importlib.util.spec_from_file_location('workflow',root/'tools/workflow.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
checks=[]
with tempfile.TemporaryDirectory(prefix='workflow-check-') as d:
    base=Path(d)
    module.BRAIN=base/'brain'
    evidence=base/'observed.txt';evidence.write_text('Observed test artifact.\n')
    args=argparse.Namespace(task='fixture',outcome='incomplete',evidence=[base/'missing'],corrections=0,lesson='',seconds=None,cost=None)
    try:module.record(args)
    except SystemExit:checks.append('missing evidence rejected')
    else:raise AssertionError('Missing evidence was accepted')
    assert not (module.BRAIN/'runs/receipts.jsonl').exists()
    args.evidence=[evidence]
    module.record(args)
    args.task='follow-up';module.record(args)
    rows=[json.loads(x) for x in (module.BRAIN/'runs/receipts.jsonl').read_text().splitlines()]
    assert [r['task'] for r in rows]==['fixture','follow-up']
    assert all(r['evidence']==[str(evidence)] for r in rows)
    checks.append('receipts preserve separate runs and actual evidence paths')
    module.health()
    report=json.loads((module.BRAIN/'runs/health.json').read_text())
    assert report['home_free_bytes']>0
    assert 'Active sessions may differ' in (module.BRAIN/'runs/health.md').read_text()
    checks.append('health produces readable JSON and Markdown artifacts')
    module.report(7)
    weekly=json.loads((module.BRAIN/'runs/weekly.json').read_text())
    assert weekly['total']==2 and weekly['outcomes']['incomplete']==2
    assert weekly['known_cost_usd'] is None and weekly['cost_coverage']==0
    checks.append('weekly report counts actual receipts and preserves unknown cost')
    (module.BRAIN/'runs/receipts.jsonl').write_text('{malformed}\n')
    try:module.report(7)
    except SystemExit:checks.append('malformed receipts stop reporting instead of silently inflating success')
    else:raise AssertionError('Malformed receipt was accepted')
out=subprocess.check_output([str(Path.home()/'.local/bin/agent-desk'),'--list'],text=True)
assert str(root) in out.splitlines()
assert all(Path(x).is_dir() for x in out.splitlines())
checks.append('workspace picker lists existing project directories')
for card in (Path.home()/'Documents/agent-brain/projects').glob('*.md'):
    import re
    for link in re.findall(r'\]\((/[^)]+)\)',card.read_text()):assert Path(link).exists(),link
checks.append('knowledge cards resolve to existing canonical files')
(root/'evidence/workflow-checks.json').write_text(json.dumps({'passed':checks},indent=2)+'\n')
print('\n'.join('PASS '+s for s in checks))
