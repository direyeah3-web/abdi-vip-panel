import shutil

shutil.copy('server.js', 'server.js.backup_ai_model')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Beddel model-ka — gemini-1.5-flash → gemini-2.0-flash
old = "model: 'gemini-1.5-flash',"
new = "model: 'gemini-2.0-flash',"

if old in c:
    c = c.replace(old, new, 1)
    print("1. Model: OK")
else:
    print("1. Model: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_ai_model")
