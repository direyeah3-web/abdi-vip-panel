import shutil

shutil.copy('public/index.html', 'public/index.html.backup_ai_page')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Nav item — ka dib Loader Helper
old_nav = """<a class="nav-item" onclick="loadPage('helper',this)"><i class="fa-solid fa-wand-magic-sparkles"></i> <span>Loader Helper</span></a>"""
new_nav = old_nav + """
        <a class="nav-item" onclick="loadPage('ai',this)"><i class="fa-solid fa-robot"></i> <span>AI Assistant</span></a>"""

if old_nav in c:
    c = c.replace(old_nav, new_nav, 1)
    print("1. Nav item: OK")
else:
    print("1. Nav item: LAMA HELIN")

# 2. Page logic — ka dib Loader Helper page
old_page = """await loadWorkerPage();
        }
        else if(p==='helper'){"""
new_page = """await loadWorkerPage();
        }
        else if(p==='ai'){
            c.innerHTML='<div class="panel-header" style="margin-bottom:20px;"><h1 style="font-size:24px;font-weight:800;">AI Assistant</h1><button class="btn-secondary" onclick="clearAIChat()"><i class="fa-solid fa-trash"></i> Clear</button></div>'+
            '<div class="panel" style="display:flex;flex-direction:column;height:calc(100vh - 250px);min-height:500px;">'+
                '<div id="ai-messages" style="flex:1;overflow-y:auto;padding:15px;background:var(--input-bg);border-radius:10px;margin-bottom:15px;"></div>'+
                '<div style="display:flex;gap:10px;">'+
                    '<input type="text" id="ai-input" placeholder="Weydii wax..." style="flex:1;padding:14px;background:var(--input-bg);border:1px solid var(--border);border-radius:10px;color:var(--text);outline:none;" onkeydown="if(event.key===&quot;Enter&quot;)sendAIMessage()">'+
                    '<button class="btn-primary" onclick="sendAIMessage()" id="ai-send-btn" style="padding:14px 20px;"><i class="fa-solid fa-paper-plane"></i></button>'+
                '</div>'+
            '</div>';
            loadAIChat();
        }
        else if(p==='helper'){"""

if old_page in c:
    c = c.replace(old_page, new_page, 1)
    print("2. Page logic: OK")
else:
    print("2. Page logic: LAMA HELIN")

# 3. Functions — ka hor loadTelegramStatus
old_func = "async function loadTelegramStatus(){"
new_func = """function loadAIChat(){
    var msgs=JSON.parse(localStorage.getItem('ai_chat')||'[]');
    var el=document.getElementById('ai-messages');
    if(!el)return;
    if(msgs.length===0){
        el.innerHTML='<div style="text-align:center;color:var(--muted);padding:40px;">'+
            '<i class="fa-solid fa-robot" style="font-size:48px;color:var(--primary);margin-bottom:15px;"></i>'+
            '<p style="font-size:14px;">Ku soo dhawoow AI Assistant!</p>'+
            '<p style="font-size:12px;">Weydii wax kasta oo ku saabsan panel-ka: license, referrals, dashboard, iwm.</p>'+
            '</div>';
        return;
    }
    el.innerHTML=msgs.map(function(m){
        var isUser=m.role==='user';
        return '<div style="display:flex;justify-content:'+(isUser?'flex-end':'flex-start')+';margin-bottom:12px;">'+
            '<div style="max-width:80%;padding:10px 14px;border-radius:12px;font-size:13px;line-height:1.5;background:'+(isUser?'var(--primary)':'var(--card)')+';color:'+(isUser?'#fff':'var(--text)')+';word-wrap:break-word;">'+
            m.text.replace(/\\n/g,'<br>')+'</div></div>';
    }).join('');
    el.scrollTop=el.scrollHeight;
}

async function sendAIMessage(){
    var input=document.getElementById('ai-input');
    var btn=document.getElementById('ai-send-btn');
    var msg=input.value.trim();
    if(!msg)return;
    input.value='';
    btn.disabled=true;
    btn.innerHTML='<i class="fa-solid fa-spinner fa-spin"></i>';
    var msgs=JSON.parse(localStorage.getItem('ai_chat')||'[]');
    msgs.push({role:'user',text:msg});
    localStorage.setItem('ai_chat',JSON.stringify(msgs));
    loadAIChat();
    var el=document.getElementById('ai-messages');
    el.innerHTML+='<div style="display:flex;justify-content:flex-start;margin-bottom:12px;"><div style="max-width:80%;padding:10px 14px;border-radius:12px;font-size:13px;background:var(--card);color:var(--muted);">Typing...</div></div>';
    el.scrollTop=el.scrollHeight;
    try{
        var t=localStorage.getItem('token');
        var r=await fetch('/api/ai/chat',{method:'POST',headers:{'Authorization':'Bearer '+t,'Content-Type':'application/json'},body:JSON.stringify({message:msg,history:msgs.slice(-10)})});
        var d=await r.json();
        if(d.success){
            msgs.push({role:'assistant',text:d.response});
            localStorage.setItem('ai_chat',JSON.stringify(msgs));
            loadAIChat();
        } else {
            msgs.push({role:'assistant',text:'❌ Error: '+(d.error||'Unknown')});
            localStorage.setItem('ai_chat',JSON.stringify(msgs));
            loadAIChat();
        }
    }catch(e){
        msgs.push({role:'assistant',text:'❌ Error: '+e.message});
        localStorage.setItem('ai_chat',JSON.stringify(msgs));
        loadAIChat();
    }
    btn.disabled=false;
    btn.innerHTML='<i class="fa-solid fa-paper-plane"></i>';
}

function clearAIChat(){
    localStorage.removeItem('ai_chat');
    loadAIChat();
    showToast('Success','Chat la tirtiray','success');
}

async function loadTelegramStatus(){"""

if old_func in c:
    c = c.replace(old_func, new_func, 1)
    print("3. Functions: OK")
else:
    print("3. Functions: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_ai_page")
