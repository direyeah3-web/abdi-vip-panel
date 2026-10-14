import shutil

shutil.copy('public/index.html', 'public/index.html.safe2')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Nav item — ka dib System Status
old_nav = """<a class="nav-item" onclick="loadPage('status',this)"><i class="fa-solid fa-signal"></i> <span>System Status</span></a>"""

new_nav = """<a class="nav-item" onclick="loadPage('status',this)"><i class="fa-solid fa-signal"></i> <span>System Status</span></a>
        <a class="nav-item" onclick="loadPage('telegram',this)"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i> <span>Telegram Bot</span></a>"""

if old_nav in c:
    c = c.replace(old_nav, new_nav, 1)
    print("1. Nav item: OK")
else:
    print("1. Nav item: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.safe2")
