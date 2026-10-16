#!/usr/bin/env python3
"""Prepare and evaluate an unchanged Sakana CPU scaffold in its real container runtime.

No model calls, optimization, paper writing, or private project modification.
"""
from pathlib import Path
from dataclasses import asdict
import json
import logging
import os
import shutil
import sys
import tempfile

root = Path(__file__).resolve().parents[1]
upstream = root/'vendor/AI-Scientist-v3'
sys.path.insert(0,str(upstream))
os.environ['PATH'] = str(root/'tools/scientist-bin')+os.pathsep+os.environ['PATH']
os.environ['AGENTIC_TEMP_ROOT'] = str(Path.home()/'.local/state/agentic-workflow/scientist-tmp')
from src.investigation.temp_bootstrap import initialize_runtime_storage
from src.investigation.task_runtime import prepare_task_runtime_report

initialize_runtime_storage()
logging.basicConfig(level=logging.INFO,format='%(levelname)s %(message)s')
workspace = root/'verification/scientist-runtime'
workspace.mkdir(parents=True,exist_ok=True)
trial = Path(tempfile.mkdtemp(prefix='circpack-',dir=workspace))
task = trial/'task'
shutil.copytree(upstream/'examples/circpack',task,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.venv'))
os.chdir(upstream)
# The shipped example uses the legacy evaluator interface. Its supported
# retained-results path preserves evidence; contracted baseline archives are
# only valid for examples with a task contract.
report = prepare_task_runtime_report(task,timeout_seconds=300,containerize=True,container_image='agentic-scientist/agent-cli:latest',container_network='host',retained_results_dir=trial/'retained')
result = {'task_dir':str(task),'report':asdict(report),'ready':report.ready,'model_calls':0,'scope':'Unchanged shipped CPU scaffold: runtime preparation and baseline validation only.'}
(root/'evidence/scientist-task-runtime.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
print(json.dumps(result,indent=2,default=str))
raise SystemExit(0 if report.ready else 1)
