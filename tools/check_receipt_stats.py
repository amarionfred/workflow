#!/usr/bin/env python3
"""Independent caller-level checks for the Empryo fixture or integrated module."""
from pathlib import Path
import copy
import importlib.util
import json
import math
import sys

root = Path(__file__).resolve().parents[1]
path = Path(sys.argv[1]) if len(sys.argv) > 1 else root/'verification/empryo-smoke/receipt_stats.py'
spec = importlib.util.spec_from_file_location('receipt_stats', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
checks = []
failures = []

def check(name, test):
    try:
        test()
    except Exception as exc:
        failures.append({'check': name, 'error': f'{type(exc).__name__}: {exc}'})
    else:
        checks.append(name)

def equal(actual, expected):
    assert actual == expected, (actual, expected)

empty = {'total':0, 'outcomes':{'accepted':0,'needs-correction':0,'blocked':0,'incomplete':0}, 'acceptance_rate':None, 'corrections':0, 'known_cost_usd':None, 'cost_coverage':None}
check('empty input retains unknown rates and cost', lambda: equal(module.summarize_receipts(iter([])), empty))
rows = [{'outcome':'accepted','cost_usd':0.0}, {'outcome':'needs-correction','corrections':2,'cost_usd':1.5}, {'outcome':'blocked','cost_usd':None}, {'outcome':'incomplete'}]
original = copy.deepcopy(rows)
expected = {'total':4, 'outcomes':{'accepted':1,'needs-correction':1,'blocked':1,'incomplete':1}, 'acceptance_rate':0.25, 'corrections':2, 'known_cost_usd':1.5, 'cost_coverage':0.5}
check('one-shot input, every outcome, zero cost, partial cost coverage', lambda: equal(module.summarize_receipts(iter(rows)), expected))
check('caller input is unchanged', lambda: equal(rows, original))
check('all unknown cost stays unknown', lambda: equal(module.summarize_receipts([{'outcome':'accepted'}])['known_cost_usd'], None))
for field, values in [('outcome',['wrong',None,[],{},False]), ('corrections',[-1,1.2,True,None,'2']), ('cost_usd',[-1,math.nan,math.inf,-math.inf,False,'0',[],{}])]:
    for index,value in enumerate(values):
        row = {'outcome':'accepted', field:value}
        def rejects(row=row):
            try:
                module.summarize_receipts([row])
            except ValueError:
                return
            raise AssertionError('invalid input did not raise ValueError')
        check(f'{field} invalid case {index + 1}', rejects)
result = {'module':str(path), 'passed':checks, 'failures':failures}
print(json.dumps(result, indent=2))
raise SystemExit(bool(failures))
