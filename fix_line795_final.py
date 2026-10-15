import shutil

shutil.copy('public/index.html', 'public/index.html.backup_line795_final')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Beddel line 795 — single quotes → template literal (backticks)
old = """c.innerHTML="<div class='panel-header' style='margin-bottom:20px;'><h1 style='font-size:24px;font-weight:800;'><i class='fa-solid fa-sliders' style='color:var(--primary);'></i> Loader Config</h1><button class='btn-secondary' onclick='loadLoaderConfig()'><i class='fa-solid fa-refresh'></i> Refresh</button></div><div id='loader-config-content'>Loading...</div>";"""

new = """c.innerHTML=`<div class="panel-header" style="margin-bottom:20px;"><h1 style="font-size:24px;font-weight:800;"><i class="fa-solid fa-sliders" style="color:var(--primary);"></i> Loader Config</h1><button class="btn-secondary" onclick="loadLoaderConfig()"><i class="fa-solid fa-refresh"></i> Refresh</button></div><div id="loader-config-content">Loading...</div>`;"""

if old in c:
    c = c.replace(old, new, 1)
    print("1. Line 795 (template literal): OK")
else:
    print("1. Line 795: LAMA HELIN — hubi qoraalka")
    # Haddii aan la helin, beddel regex ahaan
    import re
    pattern = r'c\.innerHTML="<div class=.panel-header. style=.margin-bottom:20px;.>.*?Loading\.\.\.</div>";'
    match = re.search(pattern, c, re.DOTALL)
    if match:
        c = c[:match.start()] + new + c[match.end():]
        print("2. Line 795 (regex): OK")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_line795_final")
