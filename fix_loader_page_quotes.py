import shutil
import re

shutil.copy('public/index.html', 'public/index.html.backup_loader_page_quotes')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Raadi page logic-ka 'loader-config'
pattern = r"(else if\(p==='loader-config'\)\{\s*c\.innerHTML=)'(.*?)'(;\s*loadLoaderConfig\(\);\s*\})"
match = re.search(pattern, c, re.DOTALL)

if match:
    # Ku beddel single quotes → double quotes
    inner_html = match.group(2).replace('"', '\\"').replace("\\'", "'")
    new_block = match.group(1) + '"' + inner_html + '"' + match.group(3)
    c = c[:match.start()] + new_block + c[match.end():]
    print("1. Loader page quotes: OK")
else:
    print("1. Loader page quotes: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_loader_page_quotes")
