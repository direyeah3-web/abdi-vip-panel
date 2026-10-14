import shutil

shutil.copy('server.js', 'server.js.backup_ai_model_v2')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Beddel model-ka — mid kasta oo duug ah → mid cusub
replacements = [
    ("model: 'gemini-2.0-flash',", "model: 'gemini-2.5-flash',"),
    ("model: 'gemini-1.5-flash',", "model: 'gemini-2.5-flash',"),
    ("model: 'gemini-1.5-pro',", "model: 'gemini-2.5-flash',")
]

for old, new in replacements:
    if old in c:
        c = c.replace(old, new, 1)
        print(f"1. Model beddel: {old} → {new}")
        break
else:
    print("1. Model: LAMA HELIN (hubi model-ka hadda jira)")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_ai_model_v2")
