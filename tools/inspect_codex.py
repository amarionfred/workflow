#!/usr/bin/env python3
"""Inspect configuration and skill discovery without starting a model turn."""
from pathlib import Path
import json
import selectors
import subprocess
import tempfile
import time

root = Path(__file__).resolve().parents[1]
with tempfile.TemporaryFile(mode='w+') as errors:
    process = subprocess.Popen(['codex','app-server'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errors, text=True, bufsize=1, cwd=root)
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    def send(message):
        process.stdin.write(json.dumps(message)+'\n')
        process.stdin.flush()
    def request(number, method, params):
        send({'id':number,'method':method,'params':params})
        deadline = time.monotonic()+40
        while time.monotonic() < deadline:
            if not selector.select(timeout=1): continue
            line = process.stdout.readline()
            if not line: raise RuntimeError('App-server exited before replying')
            value = json.loads(line)
            if value.get('id') == number:
                if 'error' in value: raise RuntimeError(value['error'])
                return value['result']
        raise TimeoutError(method)
    try:
        request(1,'initialize',{'clientInfo':{'name':'workflow-audit','version':'1.0'},'capabilities':{'experimentalApi':True}})
        send({'method':'initialized'})
        config = request(2,'config/read',{'includeLayers':False})
        data = config.get('config',config)
        safe_config = {k:v for k,v in data.items() if k in ['approval_policy','sandbox_mode','model','model_reasoning_effort','default_permissions']}
        skills = request(3,'skills/list',{'cwds':[str(root)],'forceReload':True})
        entries = skills.get('data',[])
        selected = [s for e in entries for s in e.get('skills',[]) if '/pstack/' in s.get('path','')]
        personal = [s['name'] for e in entries for s in e.get('skills',[]) if '/park-workflow/' in s.get('path','')]
        thread = request(4,'thread/start',{'cwd':str(root),'ephemeral':True})
        permissions = {k:thread.get(k) for k in ['approvalPolicy','sandbox','activePermissionProfile','model','reasoningEffort']}
        result = {'effective_config':safe_config,'pstack_skill_count':len(selected),'pstack_skills':[{'name':s['name'],'path':s.get('path'),'enabled':s.get('enabled')} for s in selected], 'discovery_errors':[err for e in entries for err in e.get('errors',[])]}
        result['park_workflow_skills']=personal
        result['ephemeral_thread_permissions']=permissions
        (root/'evidence/codex-discovery.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items() if k!='pstack_skills'},indent=2))
        if len(selected)!=57 or len(personal)!=3 or result['discovery_errors']: raise SystemExit(1)
        if permissions['approvalPolicy']!='never' or permissions['sandbox'].get('type')!='dangerFullAccess':raise SystemExit('Fresh thread did not receive full-access defaults.')
    finally:
        process.terminate()
        try: process.wait(timeout=5)
        except subprocess.TimeoutExpired: process.kill(); process.wait()
