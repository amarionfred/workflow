#!/usr/bin/env python3
"""Inspect the installed image and exercise its real diagram exporter, without model calls."""
from pathlib import Path
import json
import os
import struct
import subprocess
import uuid
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
adapter = str(root/'tools/scientist-bin/docker')
image = 'agentic-scientist/agent-cli:latest'
image_info = json.loads(subprocess.check_output([adapter,'image','inspect',image],text=True))[0]
base_info = json.loads(subprocess.check_output([adapter,'image','inspect','agentic-scientist/agent-cli:upstream-2b8aa39285c3'],text=True))[0]
dependency_update = json.loads(subprocess.check_output([adapter,'run','--rm','--network','none',image,'cat','/opt/headless/park-dependency-update.json'],text=True,timeout=30))
(root/'evidence/headless-dependency-update.json').write_text(json.dumps(dependency_update,indent=2)+'\n')
probe = '''import json,subprocess
commands = [['codex','--version'],['headless','--version'],['autoillustrate','--version'],['pdflatex','--version']]
results = []
for command in commands:
 p = subprocess.run(command,capture_output=True,text=True,timeout=30)
 results.append({'command':command,'returncode':p.returncode,'output':(p.stdout+p.stderr).splitlines()[:3]})
print(json.dumps(results))
raise SystemExit(any(item['returncode'] for item in results))
'''
versions = json.loads(subprocess.check_output([adapter,'run','--rm','--network','none',image,'python','-c',probe],text=True,timeout=120))
directory = root/'evidence/scientist-renderer'
directory.mkdir(parents=True,exist_ok=True)
source = directory/'runtime.drawio'
source.write_text('''<mxfile><diagram name="Runtime"><mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/><mxCell id="2" value="Runtime check" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1"><mxGeometry x="40" y="40" width="180" height="80" as="geometry"/></mxCell></root></mxGraphModel></diagram></mxfile>''')
output = directory/'runtime.svg'
png = directory/'runtime.png'
if output.exists() or png.exists():
    raise SystemExit('A prior renderer artifact exists; inspect it instead of overwriting evidence.')
for format_name in ('svg', 'png'):
    container_name = 'park-renderer-check-' + uuid.uuid4().hex[:12]
    # xvfb-run waits for its server's readiness signal. Give the direct CLI
    # invocation an init process instead of running the waiting shell as PID 1.
    command = [adapter,'run','--rm','--init','--name',container_name,'--network','none','--cap-drop','ALL','--security-opt','no-new-privileges','--user',f'{os.getuid()}:{os.getgid()}','--mount',f'type=bind,src={directory},dst=/check',image,'drawio','--export','--format',format_name,'--output',f'/check/runtime.{format_name}','/check/runtime.drawio']
    try:
        render = subprocess.run(command,capture_output=True,text=True,timeout=90)
    except subprocess.TimeoutExpired:
        subprocess.run([adapter,'stop','--timeout','5',container_name],capture_output=True,timeout=15)
        raise
    (directory/f'renderer-{format_name}.log').write_text(render.stdout+render.stderr)
    assert render.returncode==0, (render.returncode,(render.stdout+render.stderr)[-1500:])
tree = ET.parse(output)
assert tree.getroot().tag.endswith('svg')
assert 'Runtime check' in output.read_text()
assert output.stat().st_uid==os.getuid()
png_data = png.read_bytes()
assert png_data[:8] == b'\x89PNG\r\n\x1a\n'
width, height = struct.unpack('>II', png_data[16:24])
assert width > 100 and height > 40
assert png.stat().st_uid == os.getuid()
result = {'image_id':image_info['Id'],'upstream_image_id':base_info['Id'],'image_size_bytes':image_info['Size'],'versions':versions,'diagram_export':{'passed':True,'svg':str(output),'png':str(png),'dimensions':[width,height]},'model_calls':0,'limit':'Tool and renderer checks; no generated research paper or full Autoillustrate model workflow.'}
(root/'evidence/scientist-image.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
