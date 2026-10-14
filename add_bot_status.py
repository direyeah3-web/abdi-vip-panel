import shutil

shutil.copy('public/index.html', 'public/index.html.backup')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Ku dar Telegram Bot panel — ka dib Export Data panel
old_export = """<div class="panel"><h3 style="margin-bottom:15px;font-size:16px;"><i class="fa-solid fa-download" style="color:var(--primary);margin-right:8px;"></i> Export Data</h3>"""
if old_export in c:
    # Raadi dhammaadka Export Data panel-ka
    # Waxaan ku dareynaa Telegram Bot panel ka dib marka Export Data dhammaado
    pass

# Habka saxda ah: raadi qoraalka Export Data oo dhamaystiran
import re
# Soo qaado qoraalka Export Data oo dhan
match = re.search(r"(<div class=\"panel\"><h3 style=\"margin-bottom:15px;font-size:16px;\"><i class=\"fa-solid fa-download\".*?</div>\s*</div>)", c, re.DOTALL)
if match:
    export_block = match.group(1)
    telegram_block = export_block + """<div class="panel" style="margin-top:20px;">
<h3 style="margin-bottom:15px;font-size:16px;"><i class="fa-brands fa-telegram" style="color:#0088cc;margin-right:8px;"></i> Telegram Bot</h3>
<div id="telegram-status-box" style="display:flex;align-items:center;gap:12px;margin-bottom:15px;">
<span id="telegram-status-dot" style="width:12px;height:12px;border-radius:50%;background:#6b6b7e;display:inline-block;"></span>
<span id="telegram-status-text" style="font-size:14px;color:var(--muted);">Loading...</span>
</div>
<div id="telegram-details" style="font-size:13px;color:var(--muted);line-height:1.8;margin-bottom:15px;"></div>
<button class="btn-primary" onclick="loadTelegramStatus()" style="width:100%;"><i class="fa-solid fa-rotate"></i> Refresh Status</button>
</div>"""
    c = c.replace(export_block, telegram_block, 1)
    print("1. Telegram panel: OK")
else:
    print("1. Telegram panel: LAMA HELIN")

# 2. Ku dar function loadTelegramStatus() — ka hor handleLogout
old_logout = "function handleLogout()"
new_logout = """async function loadTelegramStatus(){
    var dot=document.getElementById('telegram-status-dot');
    var txt=document.getElementById('telegram-status-text');
    var det=document.getElementById('telegram-details');
    if(!dot||!txt||!det)return;
    dot.style.background='#f59e0b';
    txt.textContent='Checking...';
    det.innerHTML='';
    try{
        var t=localStorage.getItem('token');
        var r=await fetch('/api/telegram/status',{headers:{'Authorization':'Bearer '+t}});
        var d=await r.json();
        if(d.success&&d.online){
            dot.style.background='#10b981';
            txt.textContent='Online';
            txt.style.color='#10b981';
            det.innerHTML='🤖 <b>Bot:</b> @'+(d.username||'N/A')+'<br>📡 <b>Status:</b> Connected<br>📊 <b>Mode:</b> '+(d.polling?'Polling':'Webhook')+'<br>🕐 <b>Checked:</b> '+new Date().toLocaleTimeString();
        } else {
            dot.style.background='#ef4444';
            txt.textContent='Offline';
            txt.style.color='#ef4444';
            det.innerHTML='❌ <b>Bot:</b> '+(d.error||'Ma shaqeynayo');
        }
    }catch(e){
        dot.style.background='#ef4444';
        txt.textContent='Error';
        txt.style.color='#ef4444';
        det.innerHTML='❌ '+e.message;
    }
}
function handleLogout()"""
if old_logout in c:
    c = c.replace(old_logout, new_logout, 1)
    print("2. loadTelegramStatus: OK")
else:
    print("2. loadTelegramStatus: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup")
