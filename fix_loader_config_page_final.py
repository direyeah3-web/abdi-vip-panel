import shutil
import re

shutil.copy('public/index.html', 'public/index.html.backup_lc_final')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Raadi line 795 oo dhan — isla markaana beddel template literal
# Marka hore: hel qoraalka saxda ah ee hadda jira
lines = c.split('\n')
new_lines = []
fixed = False

for i, line in enumerate(lines):
    if "p==='loader-config'" in line:
        # Line 794
        new_lines.append(line)
        continue
    if i > 0 and "p==='loader-config'" in lines[i-1]:
        # Line 795 — template literal
        new_lines.append('            c.innerHTML=`<div class="panel-header" style="margin-bottom:20px;"><h1 style="font-size:24px;font-weight:800;"><i class="fa-solid fa-sliders" style="color:var(--primary);"></i> Loader Config</h1><button class="btn-secondary" onclick="loadLoaderConfig()"><i class="fa-solid fa-refresh"></i> Refresh</button></div><div id="loader-config-content">Loading...</div>`;')
        fixed = True
        continue
    new_lines.append(line)

if fixed:
    print("1. Line 795 (template literal): OK")
else:
    print("1. Line 795: LAMA HELIN")

c = '\n'.join(new_lines)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_lc_final")
