import shutil

shutil.copy('public/index.html', 'public/index.html.backup_ai_height')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Beddel page logic — height sax
old = """'<div class="panel" style="display:flex;flex-direction:column;height:calc(100vh - 250px);min-height:500px;">'+
                '<div id="ai-messages" style="flex:1;overflow-y:auto;padding:15px;background:var(--input-bg);border-radius:10px;margin-bottom:15px;"></div>'+"""

new = """'<div class="panel" style="display:flex;flex-direction:column;height:600px;max-height:70vh;">'+
                '<div id="ai-messages" style="flex:1;overflow-y:auto;padding:15px;background:var(--input-bg);border-radius:10px;margin-bottom:15px;min-height:300px;"></div>'+"""

if old in c:
    c = c.replace(old, new, 1)
    print("1. Height fix: OK")
else:
    print("1. Height fix: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_ai_height")
