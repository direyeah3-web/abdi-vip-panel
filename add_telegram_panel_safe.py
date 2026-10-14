import shutil

shutil.copy('public/index.html', 'public/index.html.backup')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Meesha saxda ah: ka dib Export Data panel, ka hor '}'
old_block = """'<button class="export-btn" onclick="exportData()" style="width:100%;justify-content:center;"><i class="fa-solid fa-file-csv"></i> Export Users (CSV)</button>'+
                    '</div>'+
                    '</div>';
        }"""

new_block = """'<button class="export-btn" onclick="exportData()" style="width:100%;justify-content:center;"><i class="fa-solid fa-file-csv"></i> Export Users (CSV)</button>'+
                    '</div>'+
                    '<div class="panel" style="margin-top:20px;">'+
                    '<h3 style="margin-bottom:15px;font-size:16px;"><i class="fa-brands fa-telegram" style="color:#0088cc;margin-right:8px;"></i> Telegram Bot</h3>'+
                    '<div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">'+
                    '<span id="tg-dot" style="width:12px;height:12px;border-radius:50%;background:#6b6b7e;display:inline-block;"></span>'+
                    '<span id="tg-text" style="font-size:14px;color:var(--muted);">Checking...</span>'+
                    '</div>'+
                    '<div id="tg-info" style="font-size:13px;color:var(--muted);line-height:1.8;margin-bottom:15px;"></div>'+
                    '<button class="btn-secondary" onclick="loadTelegramStatus()" style="width:100%;justify-content:center;"><i class="fa-solid fa-rotate"></i> Refresh Status</button>'+
                    '</div>'+
                    '</div>';
            loadTelegramStatus();
        }"""

if old_block in c:
    c = c.replace(old_block, new_block, 1)
    print("1. Panel: OK")
else:
    print("1. Panel: LAMA HELIN")

# Ku dar function loadTelegramStatus() — ka hor handleLogout
old_logout = "function handleLogout()"
new_logout = """async function loadTelegramStatus(){
    var dot=document.getElementById('tg-dot');
    var txt=document.getElementById('tg-text');
    var info=document.getElementById('tg-info');
    if(!dot||!txt||!info)return;
    dot.style.background='#f59e0b';
    txt.textContent='Checking...';
    info.innerHTML='';
    try{
        var t=localStorage.getItem('token');
        var r=await fetch('/api/telegram/status',{headers:{'Authorization':'Bearer '+t}});
        var d=await r.json();
        if(d.success&&d.online){
            dot.style.background='#10b981';
            txt.textContent='Online';
            txt.style.color='#10b981';
            info.innerHTML='🤖 <b>Bot:</b> @'+(d.username||'N/A')+'<br>📡 <b>Mode:</b> '+(d.polling?'Polling':'Webhook')+'<br>⏱️ <b>Uptime:</b> '+(d.uptime||0)+'s';
        } else {
            dot.style.background='#ef4444';
            txt.textContent='Offline';
            txt.style.color='#ef4444';
            info.innerHTML='❌ '+(d.error||'Ma shaqeynayo');
        }
    }catch(e){
        dot.style.background='#ef4444';
        txt.textContent='Error';
        txt.style.color='#ef4444';
        info.innerHTML='❌ '+e.message;
    }
}
function handleLogout()"""

if old_logout in c:
    c = c.replace(old_logout, new_logout, 1)
    print("2. Function: OK")
else:
    print("2. Function: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup")
