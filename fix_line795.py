import shutil

shutil.copy('public/index.html', 'public/index.html.backup_line795')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Beddel onclick single quotes → double quotes (line 795)
old = "onclick='loadLoaderConfig()'"
new = 'onclick="loadLoaderConfig()"'

count = c.count(old)
if count > 0:
    c = c.replace(old, new)
    print(f"1. onclick fix: OK ({count} meelood)")
else:
    print("1. onclick fix: LAMA HELIN")

# Sidoo kale hubi haddii ay jiraan kale
old2 = "onclick='loadLoaderConfig()';"
new2 = 'onclick="loadLoaderConfig()";'
if old2 in c:
    c = c.replace(old2, new2)
    print("2. onclick fix v2: OK")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_line795")
