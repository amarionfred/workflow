#!/usr/bin/env python3
"""Check private bind-mount ownership through the actual rootless adapter."""
from pathlib import Path
import json
import os
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
adapter = root/'tools/scientist-bin/docker'
with tempfile.TemporaryDirectory(prefix='rootless-check-',dir=Path.home()/'.local/state/agentic-workflow') as directory:
    mount = Path(directory)
    mount.chmod(0o700)
    (mount/'input.txt').write_text('rootless binding works\n')
    (mount/'input.txt').chmod(0o600)
    code = "from pathlib import Path; import os,json; p=Path('/check'); value=(p/'input.txt').read_text(); (p/'output.txt').write_text(value); print(json.dumps({'container_uid':os.getuid(),'input':value}))"
    command = [str(adapter),'run','--rm','--network','none','--cap-drop','ALL','--security-opt','no-new-privileges','--user',f'{os.getuid()}:{os.getgid()}', '--mount',f'type=bind,src={mount},dst=/check', 'python:3.12-slim','python','-c',code]
    result = subprocess.run(command,check=True,capture_output=True,text=True,timeout=60)
    observed = json.loads(result.stdout)
    assert observed['container_uid']==0
    assert (mount/'output.txt').read_text()=='rootless binding works\n'
    assert (mount/'output.txt').stat().st_uid==os.getuid()
    evidence = {'check':'private bind-mount read/write under rootless mapping','passed':True,'container_uid':0,'host_output_uid':os.getuid(),'network':'none','capabilities':'ALL dropped','no_new_privileges':True,'limit':'This checks UID mapping, not a full scientific campaign or sealed evaluator.'}
    (root/'evidence/scientist-rootless.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps(evidence,indent=2))
