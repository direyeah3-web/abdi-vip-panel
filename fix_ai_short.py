import shutil

shutil.copy('server.js', 'server.js.backup_ai_short')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Ku dar maxOutputTokens iyo temperature
old = "const model = genAI.getGenerativeModel({"
new = """const model = genAI.getGenerativeModel({
            generationConfig: {
                maxOutputTokens: 500,
                temperature: 0.9,
                topP: 0.95
            },"""

if old in c:
    c = c.replace(old, new, 1)
    print("1. Generation config: OK")
else:
    print("1. Generation config: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_ai_short")
