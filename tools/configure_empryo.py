#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import json
import shutil

home = Path.home()
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
backup = home / '.local/state/agentic-workflow/backups' / stamp
backup.mkdir(parents=True, exist_ok=True)
config = home / '.empryo/config.json'
shutil.copy2(config, backup / 'empryo-config.json')
settings = json.loads(config.read_text())
settings['theme'] = {'name':'koda', 'transparent':True, 'userMessageOpacity':30, 'diffOpacity':30, 'borderStrength':'strong'}
settings['diffStyle'] = 'compact'
settings['chatLayout'] = 'rail'
settings['notifyTurns'] = True
config.write_text(json.dumps(settings, indent=2)+'\n')
theme = {'_extends':'proxysoul-undertow','_label':'Koda','_description':'Park’s dark monochrome desktop palette','_variant':'dark',
 'brand':'#c4c4c4','brand-secondary':'#a6a6a6','brand-dim':'#686868','brand-alt':'#e0e0e0',
 'text-primary':'#c4c4c4','text-secondary':'#a6a6a6','text-muted':'#8a8a8a','text-dim':'#707070','text-faint':'#5c5c5c','text-subtle':'#b0b0b0',
 'bg-app':'#080808','bg-primary':'#080808','bg-secondary':'#101010','bg-elevated':'#121212','bg-popup':'#121212','bg-popup-highlight':'#242424','bg-input':'#101010','bg-user':'#1a1a1a','bg-banner':'#141414','bg-overlay':'#080808',
 'border':'#3d3d3d','border-focused':'#a6a6a6','border-active':'#c4c4c4','border-slash':'#707070',
 'accent-user':'#e0e0e0','accent-assistant':'#a6a6a6','accent-system':'#848484',
 'success':'#b8c4b6','error':'#d2a9a9','warning':'#c6bca3','info':'#b8b8b8','amber':'#c6bca3',
 'diff-added-bg':'#172019','diff-removed-bg':'#241919','diff-added-sign':'#b8c4b6','diff-removed-sign':'#d2a9a9'}
themes = home / '.empryo/themes'
themes.mkdir(exist_ok=True)
(themes / 'koda.json').write_text(json.dumps(theme, indent=2)+'\n')
hypr = home / '.config/hypr/hyprland.lua'
bind = 'hl.bind(main_mod .. " + A", hl.dsp.exec_cmd("/home/park/.local/bin/agent-desk"))'
text = hypr.read_text()
if bind not in text:
    if '" + A"' in text:
        raise SystemExit('Super+A already used; select another binding explicitly.')
    shutil.copy2(hypr, backup / 'hyprland.lua')
    hypr.write_text(text+'\n-- Agent workspace picker.\n'+bind+'\n')
print('Empryo Koda theme and Super+A launcher configured. Backup:', backup)
