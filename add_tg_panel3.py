import shutil

shutil.copy('public/index.html', 'public/index.html.backup3')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Meesha saxda ah: '</div>'</div>'; iyo } ee Settings page
old = """'<button class="export-btn" onclick="exportData()" style="width:100%;justify-content:center;"><i class="fa-solid fa-file-csv"></i> Export Users (CSV)</button>'+
                    '</div>'+
                    '</div>';
        }
        
        function saveProfile() {"""

new = """'<button class="export-btn" onclick="exportData()" style="width:100%;justify-content:center;"><i class="fa-solid fa-file-csv"></i> Export Users (CSV)</button>'+
                    '</div>'+
                    '<div class="panel" style="margin-top:20px;">'+
                    '<h3 style="margin-bottom:15px;font-size:16px;"><i class="fa-brands fa-telegram" style="color:#0088cc;margin-right:8px;"></i> Telegram Bot</h3>'+
                    '<div id="tg-status-row" style="display:flex;align-items:center;gap:10px;padding:12px;background:var(--input-bg);border-radius:10px;margin-bottom:12px;">'+
                    '<span id="tg-dot" style="width:12px;height:12px;border-radius:50%;background:#6b6b7e;display:inline-block;flex-shrink:0;"></span>'+
                    '<span id="tg-text" style="font-size:14px;font-weight:600;color:var(--muted);">Checking...</span>'+
                    '</div>'+
                    '<div id="tg-info" style="font-size:13px;color:var(--muted);line-height:1.9;"></div>'+
                    '<button class="btn-secondary" onclick="loadTelegramStatus()" style="width:100%;justify-content:center;margin-top:15px;"><i class="fa-solid fa-rotate"></i> Refresh Status</button>'+
                    '</div>'+
                    '</div>';
            loadTelegramStatus();
        }
        
        function saveProfile() {"""

if old in c:
    c = c.replace(old, new, 1)
    print("1. Panel: OK")
else:
    print("1. Panel: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup3")
