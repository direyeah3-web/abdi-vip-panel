import shutil
import re

shutil.copy('public/index.html', 'public/index.html.backup_ai_ui')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Page logic — UI casri (ChatGPT-like)
old_page = """else if(p==='ai'){
            c.innerHTML='<div class="panel-header" style="margin-bottom:20px;"><h1 style="font-size:24px;font-weight:800;">AI Assistant</h1><button class="btn-secondary" onclick="clearAIChat()"><i class="fa-solid fa-trash"></i> Clear</button></div>'+
            '<div class="panel" style="display:flex;flex-direction:column;height:600px;max-height:70vh;">'+
                '<div id="ai-messages" style="flex:1;overflow-y:auto;padding:15px;background:var(--input-bg);border-radius:10px;margin-bottom:15px;min-height:300px;"></div>'+
                '<div style="display:flex;gap:10px;">'+
                    '<input type="text" id="ai-input" placeholder="Weydii wax..." style="flex:1;padding:14px;background:var(--input-bg);border:1px solid var(--border);border-radius:10px;color:var(--text);outline:none;" onkeydown="if(event.key===&quot;Enter&quot;)sendAIMessage()">'+
                    '<button class="btn-primary" onclick="sendAIMessage()" id="ai-send-btn" style="padding:14px 20px;"><i class="fa-solid fa-paper-plane"></i></button>'+
                '</div>'+
            '</div>';
            loadAIChat();
        }"""

new_page = """else if(p==='ai'){
            c.innerHTML='<div class="panel-header" style="margin-bottom:20px;"><h1 style="font-size:24px;font-weight:800;"><i class="fa-solid fa-robot" style="color:var(--primary);"></i> AI Assistant</h1><button class="btn-secondary" onclick="clearAIChat()"><i class="fa-solid fa-trash"></i> Clear Chat</button></div>'+
            '<div class="panel" style="display:flex;flex-direction:column;height:650px;max-height:75vh;padding:0;overflow:hidden;">'+
                '<div id="ai-messages" style="flex:1;overflow-y:auto;padding:20px;background:var(--bg);"></div>'+
                '<div style="padding:15px;border-top:1px solid var(--border);background:var(--card);display:flex;gap:10px;align-items:flex-end;">'+
                    '<textarea id="ai-input" placeholder="Weydii wax..." rows="1" style="flex:1;padding:14px;background:var(--input-bg);border:1px solid var(--border);border-radius:12px;color:var(--text);outline:none;resize:none;font-family:inherit;font-size:14px;max-height:120px;" onkeydown="if(event.key===&quot;Enter&quot;&amp;&amp;!event.shiftKey){event.preventDefault();sendAIMessage()}" oninput="this.style.height=&quot;auto&quot;;this.style.height=Math.min(this.scrollHeight,120)+&quot;px&quot;"></textarea>'+
                    '<button class="btn-primary" onclick="sendAIMessage()" id="ai-send-btn" style="padding:14px 18px;border-radius:12px;"><i class="fa-solid fa-paper-plane"></i></button>'+
                '</div>'+
            '</div>';
            loadAIChat();
        }"""

if old_page in c:
    c = c.replace(old_page, new_page, 1)
    print("1. Page UI: OK")
else:
    print("1. Page UI: LAMA HELIN")

# 2. loadAIChat function — ChatGPT-like bubbles
old_load = """function loadAIChat(){
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
}"""

new_load = """function formatAIText(text){
    // Markdown-lite: **bold**, *italic*, `code`, ```code blocks```
    var html = text
        .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
        .replace(/```([\\s\\S]*?)```/g,'<pre style="background:#0a0a0f;color:#e6f1ff;padding:10px;border-radius:8px;overflow-x:auto;font-size:12px;margin:8px 0;">$1</pre>')
        .replace(/`([^`]+)`/g,'<code style="background:rgba(0,212,255,0.15);color:#00d4ff;padding:2px 6px;border-radius:4px;font-size:12px;">$1</code>')
        .replace(/\\*\\*([^*]+)\\*\\*/g,'<b>$1</b>')
        .replace(/\\*([^*]+)\\*/g,'<i>$1</i>')
        .replace(/\\n/g,'<br>');
    return html;
}

function loadAIChat(){
    var msgs=JSON.parse(localStorage.getItem('ai_chat')||'[]');
    var el=document.getElementById('ai-messages');
    if(!el)return;
    if(msgs.length===0){
        el.innerHTML='<div style="text-align:center;color:var(--muted);padding:60px 20px;">'+
            '<div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#00d4ff,#8b5cf6);display:inline-flex;align-items:center;justify-content:center;margin-bottom:20px;">'+
            '<i class="fa-solid fa-robot" style="font-size:36px;color:#fff;"></i></div>'+
            '<h2 style="font-size:20px;font-weight:700;color:var(--text);margin-bottom:8px;">Ku soo dhawoow AI Assistant</h2>'+
            '<p style="font-size:13px;max-width:400px;margin:0 auto;line-height:1.6;">Weydii wax kasta: license, referrals, dashboard, code, programming, ama su\'aalo kale.</p>'+
            '<div style="margin-top:25px;display:flex;gap:8px;flex-wrap:wrap;justify-content:center;">'+
            '<div onclick="document.getElementById(\\'ai-input\\').value=\\'Sidee license u sameeyaa?\\';sendAIMessage()" style="padding:8px 14px;background:var(--input-bg);border:1px solid var(--border);border-radius:20px;font-size:12px;cursor:pointer;color:var(--muted);">Sidee license u sameeyaa?</div>'+
            '<div onclick="document.getElementById(\\'ai-input\\').value=\\'Immisa users ayaa jira?\\';sendAIMessage()" style="padding:8px 14px;background:var(--input-bg);border:1px solid var(--border);border-radius:20px;font-size:12px;cursor:pointer;color:var(--muted);">Immisa users ayaa jira?</div>'+
            '<div onclick="document.getElementById(\\'ai-input\\').value=\\'Write a JavaScript function.\\';sendAIMessage()" style="padding:8px 14px;background:var(--input-bg);border:1px solid var(--border);border-radius:20px;font-size:12px;cursor:pointer;color:var(--muted);">Write JS code</div>'+
            '</div></div>';
        return;
    }
    el.innerHTML=msgs.map(function(m){
        var isUser=m.role==='user';
        return '<div style="display:flex;gap:10px;justify-content:'+(isUser?'flex-end':'flex-start')+';margin-bottom:16px;align-items:flex-start;">'+
            (isUser?'':'<div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#00d4ff,#8b5cf6);display:flex;align-items:center;justify-content:center;flex-shrink:0;"><i class="fa-solid fa-robot" style="font-size:14px;color:#fff;"></i></div>')+
            '<div style="max-width:75%;padding:12px 16px;border-radius:16px;font-size:13px;line-height:1.6;background:'+(isUser?'linear-gradient(135deg,#00d4ff,#8b5cf6)':'var(--card)')+';color:'+(isUser?'#fff':'var(--text)')+';word-wrap:break-word;'+(isUser?'border-bottom-right-radius:4px;':'border-bottom-left-radius:4px;border:1px solid var(--border);')+'">'+
            (isUser?m.text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\\n/g,'<br>'):formatAIText(m.text))+'</div>'+
            (isUser?'<div style="width:32px;height:32px;border-radius:50%;background:var(--input-bg);display:flex;align-items:center;justify-content:center;flex-shrink:0;"><i class="fa-solid fa-user" style="font-size:13px;color:var(--text);"></i></div>':'')+
            '</div>';
    }).join('');
    el.scrollTop=el.scrollHeight;
}"""

if old_load in c:
    c = c.replace(old_load, new_load, 1)
    print("2. loadAIChat: OK")
else:
    print("2. loadAIChat: LAMA HELIN")

# 3. sendAIMessage — input fix + scroll
old_send = """    var el=document.getElementById('ai-messages');
    el.innerHTML+='<div style="display:flex;justify-content:flex-start;margin-bottom:12px;"><div style="max-width:80%;padding:10px 14px;border-radius:12px;font-size:13px;background:var(--card);color:var(--muted);">Typing...</div></div>';
    el.scrollTop=el.scrollHeight;"""

new_send = """    var el=document.getElementById('ai-messages');
    el.innerHTML+='<div style="display:flex;gap:10px;margin-bottom:16px;"><div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#00d4ff,#8b5cf6);display:flex;align-items:center;justify-content:center;flex-shrink:0;"><i class="fa-solid fa-robot" style="font-size:14px;color:#fff;"></i></div><div style="padding:12px 16px;border-radius:16px;border-bottom-left-radius:4px;background:var(--card);border:1px solid var(--border);color:var(--muted);font-size:13px;"><i class="fa-solid fa-spinner fa-spin"></i> AI wuu fikirayaa...</div></div>';
    el.scrollTop=el.scrollHeight;"""

if old_send in c:
    c = c.replace(old_send, new_send, 1)
    print("3. sendAIMessage typing: OK")
else:
    print("3. sendAIMessage typing: LAMA HELIN")

# 4. Popup fix — input autocomplete off
old_input_kw = """input type="text" id="ai-input\""""
new_input_kw = """textarea id="ai-input" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false\""""
# Sidoo kale haddii input type uu jiro
if 'type="text" id="ai-input"' in c:
    c = c.replace('type="text" id="ai-input"', 'id="ai-input" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false"', 1)
    print("4. Popup fix: OK")
else:
    print("4. Popup fix: horey waa la beddelay")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_ai_ui")
