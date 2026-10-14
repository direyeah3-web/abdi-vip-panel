import shutil
import re

shutil.copy('public/index.html', 'public/index.html.safe3')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Soo qaado qoraalka loadPage('status') (regex)
status_pattern = r"(else if\(p==='status'\)\{.*?await loadSystemStatus\(\);\s*\n\s*\})"
match = re.search(status_pattern, c, re.DOTALL)

if match:
    status_block = match.group(1)
    print("1. Status block la helay")
    
    telegram_block = status_block + """
        else if(p==='telegram'){
            c.innerHTML='<div class="panel-header" style="margin-bottom:20px;"><h1 style="font-size:24px;font-weight:800;">Telegram Bot</h1><button class="btn-secondary" onclick="loadPage(\\'telegram\\')"><i class="fa-solid fa-refresh"></i> Refresh</button></div>'+
            '<div class="stats-grid">'+
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
    
    c = c.replace(status_block, telegram_block, 1)
    print("2. Telegram page: OK")
else:
    print("1. Status block: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.safe3")
