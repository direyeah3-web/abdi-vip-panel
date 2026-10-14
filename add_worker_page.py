import shutil

shutil.copy('public/index.html', 'public/index.html.safe6')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Nav item — ka dib Telegram Bot
old_nav = """<a class="nav-item" onclick="loadPage('telegram',this)"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i> <span>Telegram Bot</span></a>"""
new_nav = old_nav + """
        <a class="nav-item" onclick="loadPage('worker',this)"><i class="fa-solid fa-cloud"></i> <span>Cloudflare Worker</span></a>"""

if old_nav in c:
    c = c.replace(old_nav, new_nav, 1)
    print("1. Nav item: OK")
else:
    print("1. Nav item: LAMA HELIN")

# 2. Page logic — ka dib loadPage('telegram')
old_page = """await loadTelegramPage();
        }"""
new_page = """await loadTelegramPage();
        }
        else if(p==='worker'){
            c.innerHTML='<div class="panel-header" style="margin-bottom:20px;"><h1 style="font-size:24px;font-weight:800;">Cloudflare Worker</h1><button class="btn-secondary" onclick="loadPage(\\'worker\\')"><i class="fa-solid fa-refresh"></i> Refresh</button></div>'+
            '<div class="stats-grid">'+
                '<div class="stat-card"><div class="stat-icon blue"><i class="fa-solid fa-cloud"></i></div><div class="stat-value" id="cw-status">...</div><div class="stat-label">Worker Status</div></div>'+
                '<div class="stat-card"><div class="stat-icon purple"><i class="fa-solid fa-code"></i></div><div class="stat-value" id="cw-code-size" style="font-size:16px;">...</div><div class="stat-label">Code Size</div></div>'+
                '<div class="stat-card"><div class="stat-icon green"><i class="fa-solid fa-clock"></i></div><div class="stat-value" id="cw-response">...</div><div class="stat-label">Response Time</div></div>'+
                '<div class="stat-card"><div class="stat-icon yellow"><i class="fa-solid fa-globe"></i></div><div class="stat-value" id="cw-url" style="font-size:11px;">...</div><div class="stat-label">Worker URL</div></div>'+
            '</div>'+
            '<div class="panel" style="margin-top:20px;"><div class="panel-header"><h3><i class="fa-solid fa-code"></i> Worker Code</h3><button class="btn-primary" onclick="saveWorkerCode()" id="cw-save-btn"><i class="fa-solid fa-save"></i> Deploy</button></div>'+
                '<textarea id="cw-code" style="width:100%;min-height:400px;background:#0a0a0f;color:#e6f1ff;border:1px solid var(--border);border-radius:10px;padding:15px;font-family:monospace;font-size:13px;line-height:1.5;"></textarea>'+
                '<div id="cw-result" style="margin-top:15px;"></div>'+
            '</div>';
            await loadWorkerPage();
        }"""

if old_page in c:
    c = c.replace(old_page, new_page, 1)
    print("2. Page: OK")
else:
    print("2. Page: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.safe6")
