import shutil

shutil.copy('public/index.html', 'public/index.html.backup5')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Meesha saxda ah: ka hor async function loadTelegramStatus()
old = "async function loadTelegramStatus(){"

new = """async function loadTelegramPage(){
    try{
        var t=localStorage.getItem('token');
        var r=await fetch('/api/telegram/status',{headers:{'Authorization':'Bearer '+t}});
        var d=await r.json();
        
        var statusEl=document.getElementById('tg-page-status');
        var userEl=document.getElementById('tg-page-username');
        var uptimeEl=document.getElementById('tg-page-uptime');
        var modeEl=document.getElementById('tg-page-mode');
        var detailsEl=document.getElementById('tg-page-details');
        var infoEl=document.getElementById('tg-page-info');
        
        if(d.success && d.online){
            statusEl.innerHTML='<span style="color:var(--green);font-size:16px;">●</span> Online';
            userEl.textContent='@'+(d.username||'N/A');
            uptimeEl.textContent=(d.uptime||0)+'s';
            modeEl.textContent=(d.polling?'Polling':'Webhook');
            
            detailsEl.innerHTML='<div style="font-size:13px;line-height:2;">'+
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Status:</span><strong style="color:var(--green);">Online</strong></div>'+
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Bot Name:</span><strong>'+(d.name||'N/A')+'</strong></div>'+
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Username:</span><strong>@'+(d.username||'N/A')+'</strong></div>'+
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Mode:</span><strong>'+(d.polling?'Polling':'Webhook')+'</strong></div>'+
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Uptime:</span><strong>'+(d.uptime||0)+'s</strong></div>'+
                '</div>';
            
            infoEl.innerHTML='<div style="font-size:13px;line-height:2;">'+
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Chat ID:</span><strong style="font-size:11px;"><code>'+(d.chat_id||'N/A')+'</code></strong></div>'+
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Version:</span><strong>'+(d.version||'3.0.0')+'</strong></div>'+
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Node:</span><strong>'+(d.node||'N/A')+'</strong></div>'+
                '<div style="margin-top:10px;padding:10px;background:rgba(16,185,129,0.1);border-radius:8px;font-size:12px;color:var(--green);">✅ Bot-ku wuu shaqaynayaa!</div>'+
                '</div>';
        } else {
            statusEl.innerHTML='<span style="color:var(--red);font-size:16px;">●</span> Offline';
            userEl.textContent='N/A';
            uptimeEl.textContent='0s';
            modeEl.textContent='N/A';
            detailsEl.innerHTML='<div style="padding:15px;background:rgba(239,68,68,0.1);border-radius:8px;color:var(--red);font-size:13px;">❌ '+(d.error||'Bot ma shaqeynayo')+'</div>';
            infoEl.innerHTML='';
        }
    }catch(e){
        console.error('Telegram page error:', e);
    }
}

async function testTelegramConnection(){
    var result=document.getElementById('tg-test-result');
    result.innerHTML='<p style="color:var(--muted);">Sending test message...</p>';
    try{
        var t=localStorage.getItem('token');
        var r=await fetch('/api/telegram/test',{method:'POST',headers:{'Authorization':'Bearer '+t}});
        var d=await r.json();
        if(d.success){
            result.innerHTML='<div style="padding:15px;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);border-radius:10px;">'+
                '<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;"><i class="fa-solid fa-check-circle" style="color:var(--green);font-size:20px;"></i><strong style="color:var(--green);">Test Message Sent!</strong></div>'+
                '<div style="font-size:13px;color:var(--muted);">Fariin test ah ayaa loo diray Telegram-kaaga. Fiiro gaar ah: <strong>@'+(localStorage.getItem('user')?JSON.parse(localStorage.getItem('user')).username:'admin')+'</strong></div>'+
                '</div>';
            showToast('Success', 'Test message la diray!', 'success');
        } else {
            result.innerHTML='<div style="padding:15px;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:10px;">'+
                '<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;"><i class="fa-solid fa-times-circle" style="color:var(--red);font-size:20px;"></i><strong style="color:var(--red);">Test Failed!</strong></div>'+
                '<div style="font-size:13px;color:var(--muted);">Error: <strong style="color:var(--red);">'+(d.error||'Unknown')+'</strong></div>'+
                '</div>';
        }
    }catch(e){
        result.innerHTML='<div style="padding:15px;background:rgba(239,68,68,0.1);border-radius:10px;"><strong style="color:var(--red);">Error: '+e.message+'</strong></div>';
    }
}

async function loadTelegramStatus(){"""

if old in c:
    c = c.replace(old, new, 1)
    print("1. Functions: OK")
else:
    print("1. Functions: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup5")
