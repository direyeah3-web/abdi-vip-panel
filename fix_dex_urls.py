import shutil
import re

shutil.copy('server.js', 'server.js.backup_dex_urls')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Beddel URL regex — ka saar format strings (%s, %d)
old = "const urlRegex = /https?:\\\\/\\\\/[^\\\\x00-\\\\x20\"']+/g;"
new = "const urlRegex = /https?:\\\\/\\\\/[a-zA-Z0-9.\\\\-_~:\\\\/?#\\\\[\\\\]@!$&'()*+,;=%]+/g;"

if old in c:
    c = c.replace(old, new, 1)
    print("1. URL regex: OK")
else:
    print("1. URL regex: LAMA HELIN")

# Beddel essential extraction — ka saar format strings
old_e = """    const serverUrls = allUrls.filter(u => {
        const url = u.url || '';
        return url.startsWith('http') && !ignoreHosts.some(h => url.includes(h));
    });"""

new_e = """    const serverUrls = allUrls.filter(u => {
        const url = u.url || '';
        // Ka saar format strings (%s, %d, iwm)
        if (url.includes('%s') || url.includes('%d') || url.includes('%1$s')) return false;
        // Ka saar native lib URLs
        if (u.file && u.file.includes('lib/')) return false;
        return url.startsWith('http') && !ignoreHosts.some(h => url.includes(h));
    });"""

if old_e in c:
    c = c.replace(old_e, new_e, 1)
    print("2. Essential filter: OK")
else:
    print("2. Essential filter: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_dex_urls")
