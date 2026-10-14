import shutil
import re

shutil.copy('public/index.html', 'public/index.html.backup4')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Nav item — ka dib System Status nav item
old_nav = """<a class="nav-item" onclick="loadPage('status',this)"><i class="fa-solid fa-signal"></i> <span>System Status</span></a>"""
new_nav = """<a class="nav-item" onclick="loadPage('status',this)"><i class="fa-solid fa-signal"></i> <span>System Status</span></a>
        <a class="nav-item" onclick="loadPage('telegram',this)"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i> <span>Telegram Bot</span></a>"""

if old_nav in c:
    c = c.replace(old_nav, new_nav, 1)
    print("1. Nav item: OK")
else:
    print("1. Nav item: LAMA HELIN")

# 2. loadPage('telegram') — ka dib loadPage('status')
# Soo qaado qoraalka status page oo dhan (regex)
status_pattern = r"(else if\(p==='status'\)\{.*?\n\})"
match = re.search(status_pattern, c, re.DOTALL)

if match:
    status_block = match.group(1)
    
    telegram_block = """else if(p==='telegram'){
            c.innerHTML='<div class="panel-header" style="margin-bottom:20px;"><h1 style="font-size:24px;font-weight:800;">Telegram Bot</h1><button class="btn-secondary" onclick="loadPage(\\'telegram\\')"><i class="fa-solid fa-refresh"></i> Refresh</button></div>'+
            '<div class="stats-grid" id="tg-stats-grid">'+
                '<div class="stat-card"><div class="stat-icon blue"><i class="fa-brands fa-telegram"></i></div><div class="stat-value" id="tg-page-status">...</div><div class="stat-label">Bot Status</div></div>'+
                '<div class="stat-card"><div class="stat-icon purple"><i class="fa-solid fa-robot"></i></div><div class="stat-value" id="tg-page-username" style="font-size:14px;">...</div><div class="stat-label">Bot Username</div></div>'+
                '<div class="stat-card"><div class="stat-icon green"><i class="fa-solid fa-clock"></i></div><div class="stat-value" id="tg-page-uptime">...</div><div class="stat-label">Uptime</div></div>'+
                '<div class="stat-card"><div class="stat-icon yellow"><i class="fa-solid fa-comment"></i></div><div class="stat-value" id="tg-page-mode">...</div><div class="stat-label">Mode</div></div>'+
            '</div>'+
            '<div class="content-grid" style="margin-top:20px;">'+
                '<div class="panel"><div class="panel-header"><h3>Bot Details</h3></div><div id="tg-page-details">Loading...</div></div>'+
                '<div class="panel"><div class="panel-header"><h3>Bot Info</h3></div><div id="tg-page-info">Loading...</div></div>'+
            '</div>'+
            '<div class="panel" style="margin-top:20px;"><div class="panel-header"><h3>Test Connection</h3></div>'+
                '<p style="color:var(--muted);font-size:13px;margin-bottom:15px;">Test the connection between Telegram Bot and Railway Server.</p>'+
                '<button class="btn-primary" onclick="testTelegramConnection()"><i class="fa-solid fa-paper-plane"></i> Send Test Message</button>'+
                '<div id="tg-test-result" style="margin-top:20px;"></div>'+
            '</div>';
            await loadTelegramPage();
        }"""
    
    c = c.replace(status_block, status_block + "\n        " + telegram_block, 1)
    print("2. loadPage('telegram'): OK")
else:
    print("2. loadPage('telegram'): LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup4")
