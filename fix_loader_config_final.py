import shutil
import re

shutil.copy('public/index.html', 'public/index.html.backup_loader_config_final')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Baadh haddii page logic jiro
if "p==='loader-config'" in c:
    # Raadi oo beddel block-ka oo dhan — isticmaal double quotes
    pattern = r"else if\(p==='loader-config'\)\{.*?\n        \}"
    match = re.search(pattern, c, re.DOTALL)
    
    if match:
        # Ku beddel block-ka cusub — DOUBLE QUOTES (sax)
        new_block = '''else if(p==='loader-config'){
            c.innerHTML="<div class='panel-header' style='margin-bottom:20px;'><h1 style='font-size:24px;font-weight:800;'><i class='fa-solid fa-sliders' style='color:var(--primary);'></i> Loader Config</h1><button class='btn-secondary' onclick='loadLoaderConfig()'><i class='fa-solid fa-refresh'></i> Refresh</button></div><div id='loader-config-content'>Loading...</div>";
            loadLoaderConfig();
        }'''
        c = c[:match.start()] + new_block + c[match.end():]
        print("1. Loader Config page: OK")
    else:
        print("1. Loader Config page: LAMA HELIN (pattern khaldan)")
else:
    print("1. Loader Config page: ma jiro (restore ayaa tirtiray)")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_loader_config_final")
