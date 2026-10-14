import shutil

# 1. Backup
shutil.copy('public/index.html', 'public/index.html.backup')

# 2. Akhri
with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 3. Beddel body-ga light — sawir wallpaper
old_body = '[data-theme="light"] body{background:linear-gradient(135deg,#0d1b2a 0%,#0f2236 50%,#0d1b2a 100%) !important;}'
new_body = '[data-theme="light"] body{background:url(\'/bg-light.png\') center/cover no-repeat fixed !important;}'
if old_body in c:
    c = c.replace(old_body, new_body, 1)
    print("1. Body background: OK")
else:
    print("1. Body background: LAMA HELIN")

# 4. Sidebar-ka light — transparent (si sawirka uga muuqdo)
old_sidebar = '[data-theme="light"] .sidebar{background:linear-gradient(180deg,#0f2236,#0d1b2a) !important;border-right:1px solid #1e3a5f;}'
new_sidebar = '[data-theme="light"] .sidebar{background:rgba(15,34,54,0.75) !important;border-right:1px solid #1e3a5f;backdrop-filter:blur(15px);}'
if old_sidebar in c:
    c = c.replace(old_sidebar, new_sidebar, 1)
    print("2. Sidebar: OK")
else:
    print("2. Sidebar: LAMA HELIN")

# 5. Top nav-ka light — transparent
old_topnav = '[data-theme="light"] .topnav{background:#ffffff;border-bottom:1px solid var(--border);}'
new_topnav = '[data-theme="light"] .topnav{background:rgba(255,255,255,0.7) !important;border-bottom:1px solid var(--border);backdrop-filter:blur(15px);}'
if old_topnav in c:
    c = c.replace(old_topnav, new_topnav, 1)
    print("3. Topnav: OK")
else:
    print("3. Topnav: LAMA HELIN")

# 6. Main-ka light — transparent (si sawirka uga muuqdo)
old_main = '[data-theme="light"] .main{background:'
if old_main in c:
    print("4. Main: horey wuu jiraa — aan baadhno")
else:
    # Ku dar main transparent
    marker = '[data-theme="light"] .card{'
    addition = '[data-theme="light"] .main{background:transparent !important;}\n'
    if marker in c:
        c = c.replace(marker, addition + marker, 1)
        print("4. Main transparent: OK")
    else:
        print("4. Main: LAMA HELIN")

# 7. Qor
with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup")
