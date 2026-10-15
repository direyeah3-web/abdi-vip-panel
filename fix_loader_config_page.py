import shutil
import re

shutil.copy('public/index.html', 'public/index.html.backup_loader_config_fix')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Raadi meesha page logic-ka 'helper' (Loader Helper)
pattern = r"(else if\(p==='helper'\)\{.*?\n        \})"
match = re.search(pattern, c, re.DOTALL)

if match:
    helper_block = match.group(1)
    loader_config_block = helper_block + """
        else if(p==='loader-config'){
            c.innerHTML='<div class="panel-header" style="margin-bottom:20px;"><h1 style="font-size:24px;font-weight:800;"><i class="fa-solid fa-sliders" style="color:var(--primary);"></i> Loader Config</h1><button class="btn-secondary" onclick="loadLoaderConfig()"><i class="fa-solid fa-refresh"></i> Refresh</button></div>'+
            '<div id="loader-config-content">Loading...</div>';
            loadLoaderConfig();
        }"""
    c = c.replace(helper_block, loader_config_block, 1)
    print("1. Page logic: OK")
else:
    print("1. Page logic: LAMA HELIN (helper page ma jiro)")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_loader_config_fix")
