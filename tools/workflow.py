#!/usr/bin/env python3
"""Local workflow records. This tool never starts an LLM or sends a message."""
from pathlib import Path
from datetime import datetime, timedelta, timezone
import argparse
import fcntl
import json
import math
import os
import shutil
import tempfile
import tomllib
from receipt_stats import summarize_receipts

HOME_DIR = Path.home()
BRAIN = HOME_DIR/'Documents/agent-brain'

def atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w',dir=path.parent,delete=False) as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
        temporary = Path(f.name)
    temporary.replace(path)

def health():
    now = datetime.now(timezone.utc).isoformat()
    free = shutil.disk_usage(HOME_DIR).free
    config = tomllib.loads((HOME_DIR/'.codex/config.toml').read_text())
    installed = config.get('plugins',{})
    report = {'checked_at':now, 'home_free_bytes':free, 'disk_status':'low' if free < 5*1024**3 else 'ok',
              'codex_default_approval':config.get('approval_policy','unspecified'),
              'codex_default_sandbox':config.get('sandbox_mode','unspecified'),
              'pstack_enabled':installed.get('pstack@personal',{}).get('enabled',False),
              'empryo_binary_present':(HOME_DIR/'.empryo/bin/empryo').is_file(),
              'knowledge_project_cards':len(list((BRAIN/'projects').glob('*.md')))}
    atomic_write(BRAIN/'runs/health.json',json.dumps(report,indent=2)+'\n')
    text = f'# Local workflow health\n\nChecked {now}. This is a deterministic local check; no model calls or external messages.\n\n'
    text += f'- Home disk free: {free/1024**3:.2f} GiB ({report["disk_status"]}).\n'
    text += f'- Codex defaults: `{report["codex_default_sandbox"]}`, approvals `{report["codex_default_approval"]}`. Active sessions may differ.\n'
    text += f'- pstack enabled in config: {report["pstack_enabled"]}.\n- Empryo binary present: {report["empryo_binary_present"]}.\n'
    text += f'- Knowledge project cards: {report["knowledge_project_cards"]}.\n\nThese checks do not prove provider login, app behavior, model quality, or project completion. See the run receipts and task evidence for those.\n'
    atomic_write(BRAIN/'runs/health.md',text)
    print(json.dumps(report,indent=2))

def record(args):
    files = [p.expanduser().resolve() for p in args.evidence]
    missing = [str(p) for p in files if not p.exists()]
    if missing: raise SystemExit('Evidence does not exist: '+', '.join(missing))
    item = {'date':datetime.now(timezone.utc).isoformat(),'task':args.task,'outcome':args.outcome,'evidence':[str(p) for p in files], 'corrections':args.corrections,'lesson':args.lesson,'duration_seconds':args.seconds,'cost_usd':args.cost}
    path = BRAIN/'runs/receipts.jsonl'
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a') as f:
        fcntl.flock(f,fcntl.LOCK_EX)
        f.write(json.dumps(item)+'\n')
        f.flush()
        os.fsync(f.fileno())
    print('Recorded observed outcome. Evidence existence is checked; acceptance remains a review judgment.')

def report(days):
    now = datetime.now(timezone.utc)
    since = now - timedelta(days=days)
    source = BRAIN/'runs/receipts.jsonl'
    rows = []
    if source.exists():
        with source.open() as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            for number, line in enumerate(f, 1):
                try:
                    row = json.loads(line)
                    date = datetime.fromisoformat(row['date'])
                    if date.tzinfo is None:
                        raise ValueError('receipt date must include timezone')
                    if since <= date <= now:
                        rows.append(row)
                except (ValueError, KeyError, TypeError) as exc:
                    raise SystemExit(f'{source}:{number}: invalid receipt: {exc}')
    try:
        stats = summarize_receipts(rows)
    except ValueError as exc:
        raise SystemExit(f'Cannot summarize invalid receipts: {exc}')
    result = {'generated_at':now.isoformat(), 'since':since.isoformat(), 'days':days, **stats}
    atomic_write(BRAIN/'runs/weekly.json', json.dumps(result, indent=2)+'\n')
    rate = 'unknown' if stats['acceptance_rate'] is None else f'{stats["acceptance_rate"]:.0%}'
    coverage = 'unknown' if stats['cost_coverage'] is None else f'{stats["cost_coverage"]:.0%}'
    known_cost = 'unknown' if stats['known_cost_usd'] is None else f'${stats["known_cost_usd"]:.4f}'
    lines = [f'# Workflow review: last {days} days', '', f'Generated {now.isoformat()}.', '',
             f'- Recorded tasks: {stats["total"]}; accepted fraction: {rate}.',
             f'- Outcomes: {json.dumps(stats["outcomes"])}.',
             f'- Recorded corrections: {stats["corrections"]}.',
             f'- Known cost subtotal: {known_cost}; coverage: {coverage}.', '',
             'These are reviewed receipts, not a randomized productivity benchmark. A subscription token estimate is not an invoice. Missing receipts can bias these figures.', '',
             'Review the following evidence before changing a rule or adding a skill:', '']
    for row in rows:
        if row.get('corrections',0) or row['outcome'] != 'accepted' or row.get('lesson'):
            task = str(row.get('task','Untitled')).replace('\n',' ')
            lines.extend([f'- {task}: {row["outcome"]}; corrections {row.get("corrections",0)}.',
                          f'  Lesson: {str(row.get("lesson") or "None recorded").replace(chr(10), " ")}',
                          f'  Evidence: {json.dumps(row.get("evidence",[]))}'])
    if not rows:
        lines.append('No recorded tasks in this interval. Start with a real task and its evidence.')
    atomic_write(BRAIN/'runs/weekly.md', '\n'.join(lines)+'\n')
    print(json.dumps(result,indent=2))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('health')
    review=sub.add_parser('report')
    review.add_argument('--days',type=int,default=7)
    r=sub.add_parser('record')
    r.add_argument('--task',required=True)
    r.add_argument('--outcome',choices=['accepted','needs-correction','blocked','incomplete'],required=True)
    r.add_argument('--evidence',type=Path,nargs='+',required=True)
    r.add_argument('--corrections',type=int,default=0)
    r.add_argument('--lesson',default='')
    r.add_argument('--seconds',type=float)
    r.add_argument('--cost',type=float)
    a=p.parse_args()
    if a.command=='health':health()
    elif a.command=='report':
        if a.days<1:p.error('Days must be positive.')
        report(a.days)
    else:
        if a.corrections < 0 or any(x is not None and (not math.isfinite(x) or x<0) for x in (a.seconds,a.cost)):p.error('Counts and resource measurements must be finite and nonnegative.')
        record(a)

if __name__=='__main__':main()
