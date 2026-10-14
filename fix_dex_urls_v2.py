import shutil
import re

shutil.copy('server.js', 'server.js.backup_dex_v2')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Beddel DEX URL extraction
old_dex = """                // URLs with line numbers
                lines.forEach((line, idx) => {
                    const matches = line.match(urlRegex);
                    if (matches) {
                        matches.forEach(u => {
                            urlsList.push({ file: name, line: idx + 1, url: u });
                        });
                    }
                });"""

new_dex = """                // URLs with line numbers — DEX strings (latin1)
                lines.forEach((line, idx) => {
                    // Ka saar format strings (%s, %d)
                    if (line.includes('%s') || line.includes('%d') || line.includes('%1$s')) return;
                    const matches = line.match(urlRegex);
                    if (matches) {
                        matches.forEach(u => {
                            // Kaliya URL-yada sax ah (ma aha format strings)
                            if (u.includes('%') && !u.includes('%20')) return;
                            urlsList.push({ file: name, line: idx + 1, url: u });
                        });
                    }
                });"""

if old_dex in c:
    c = c.replace(old_dex, new_dex, 1)
    print("1. DEX URLs filter: OK")
else:
    print("1. DEX URLs filter: LAMA HELIN")

# Beddel extractEssential — ka saar native URLs
old_e = """    const serverUrls = allUrls.filter(u => {
        const url = u.url || '';
        return url.startsWith('http') && !ignoreHosts.some(h => url.includes(h));
    });"""

new_e = """    const serverUrls = allUrls.filter(u => {
        const url = u.url || '';
        // Ka saar format strings
        if (url.includes('%s') || url.includes('%d')) return false;
        // Ka saar native libs — DEX kaliya
        if (u.file && u.file.includes('lib/')) return false;
        // Ka saar useless URLs
        if (url.includes('schemas.android.com') || url.includes('crbug.com') || url.includes('google.com') || url.includes('github.com') || url.includes('curl.se') || url.includes('llvm.org') || url.includes('DeNA')) return false;
        return url.startsWith('http');
    });"""

if old_e in c:
    c = c.replace(old_e, new_e, 1)
    print("2. Essential filter: OK")
else:
    print("2. Essential filter: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_dex_v2")
