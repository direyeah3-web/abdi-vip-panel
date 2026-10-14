import shutil

shutil.copy('public/index.html', 'public/index.html.safe10')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Beddel line 882 — getItem('theme') → getItem('abdi_theme')
old_line = "var saved = localStorage.getItem('theme');"
new_line = "var saved = localStorage.getItem('abdi_theme') || localStorage.getItem('theme');"

count = c.count(old_line)
if count > 0:
    c = c.replace(old_line, new_line)
    print(f"1. Line 882: OK ({count} meelood)")
else:
    print("1. Line 882: LAMA HELIN")

# Sidoo kale hubi haddii ay jiraan keydka kale ee 'theme' oo aan la beddelin
old_set_dark = "localStorage.setItem('theme', 'dark');"
old_set_light = "localStorage.setItem('theme', 'light');"
if old_set_dark in c:
    c = c.replace(old_set_dark, "localStorage.setItem('abdi_theme', 'dark');")
    print("2. setItem dark: OK")
if old_set_light in c:
    c = c.replace(old_set_light, "localStorage.setItem('abdi_theme', 'light');")
    print("3. setItem light: OK")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.safe10")
