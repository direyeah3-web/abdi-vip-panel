import shutil
import re

shutil.copy('public/index.html', 'public/index.html.backup_ai_modern')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Page logic — HTML casri + popup fix
old_page_pattern = r"else if\(p==='ai'\)\{.*?\n        \}"
match = re.search(old_page_pattern, c, re.DOTALL)

new_page = """else if(p==='ai'){
            c.innerHTML='<div class="panel-header" style="margin-bottom:20px;"><h1 style="font-size:24px;font-weight:800;"><i class="fa-solid fa-robot" style="color:var(--primary);"></i> AI Assistant</h1><button class="btn-secondary" onclick="clearAIChat()"><i class="fa-solid fa-trash"></i> Clear</button></div>'+
            '<div class="panel" style="display:flex;flex-direction:column;height:650px;max-height:75vh;padding:0;overflow:hidden;">'+
                '<div id="ai-messages" style="flex:1;overflow-y:auto;padding:20px;background:var(--bg);"></div>'+
                '<div style="padding:15px;border-top:1px solid var(--border);background:var(--card);">'+
                    '<div style="display:flex;gap:10px;align-items:flex-end;background:var(--input-bg);border:1px solid var(--border);border-radius:14px;padding:6px 6px 6px 16px;">'+
                        '<textarea id="ai-input" placeholder="Weydii wax..." rows="1" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" name="ai-message-'+Date.now()+'" style="flex:1;padding:10px 0;background:transparent;border:none;color:var(--text);outline:none;resize:none;font-family:inherit;font-size:14px;max-height:120px;line-height:1.5;" onkeydown="if(event.key===&quot;Enter&quot;&amp;&amp;!event.shiftKey){event.preventDefault();sendAIMessage()}" oninput="this.style.height=&quot;auto&quot;;this.style.height=Math.min(this.scrollHeight,120)+&quot;px&quot;;this.style.overflowY=this.scrollHeight>120?&quot;auto&quot;:&quot;hidden&quot;;"></textarea>'+
                        '<button onclick="sendAIMessage()" id="ai-send-btn" style="width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,#00d4ff,#8b5cf6);border:none;color:#fff;cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center;"><i class="fa-solid fa-arrow-up" style="font-size:16px;"></i></button>'+
                    '</div>'+
                    '<div style="font-size:11px;color:var(--muted);text-align:center;margin-top:8px;">AI-ga waxaa laga yaabaa in uu khaldanaado. Hubi macluumaadka muhiimka ah.</div>'+
                '</div>'+
            '</div>';
            loadAIChat();
        }"""

if match:
    c = c[:match.start()] + new_page + c[match.end():]
    print("1. Page HTML: OK")
else:
    print("1. Page HTML: LAMA HELIN")

# 2. loadAIChat — ChatGPT-like bubbles
old_load_pattern = r"function loadAIChat\(\)\{.*?\n\}"
match2 = re.search(old_load_pattern, c, re.DOTALL)

new_load = """function formatAIText(text){
    var html = text
        .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
        .replace(/```([\\s\\S]*?)```/g,'<pre style="background:#0a0a0f;color:#e6f1ff;padding:12px;border-radius:10px;overflow-x:auto;font-size:12px;margin:10px 0;border:1px solid #1e1e2e;">$1</pre>')
        .replace(/`([^`]+)`/g,'<code style="background:rgba(0,212,255,0.15);color:#00d4ff;padding:2px 6px;border-radius:4px;font-size:12px;">$1</code>')
        .replace(/\\*\\*([^*]+)\\*\\*/g,'<b style="color:#fff;">$1</b>')
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
            '<div style="width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,#00d4ff,#8b5cf6);display:inline-flex;align-items:center;justify-content:center;margin-bottom:20px;box-shadow:0 8px 32px rgba(0,212,255,0.3);">'+
            '<i class="fa-solid fa-robot" style="font-size:32px;color:#fff;"></i></div>'+
            '<h2 style="font-size:20px;font-weight:700;color:var(--text);margin-bottom:8px;">Ku soo dhawoow AI Assistant</h2>'+
            '<p style="font-size:13px;max-width:380px;margin:0 auto;line-height:1.6;">Weydii wax kasta: license, referrals, dashboard, code, programming, ama su\\'aalo kale.</p>'+
            '<div style="margin-top:24px;display:flex;gap:8px;flex-wrap:wrap;justify-content:center;">'+
            '<div onclick="quickAsk(\\'Sidee license u sameeyaa?\\')" style="padding:8px 14px;background:var(--input-bg);border:1px solid var(--border);border-radius:20px;font-size:12px;cursor:pointer;color:var(--muted);">🔑 Sidee license u sameeyaa?</div>'+
            '<div onclick="quickAsk(\\'Immisa users ayaa jira?\\')" style="padding:8px 14px;background:var(--input-bg);border:1px solid var(--border);border-radius:20px;font-size:12px;cursor:pointer;color:var(--muted);">👥 Immisa users?</div>'+
            '<div onclick="quickAsk(\\'Write a JavaScript function.\\')" style="padding:8px 14px;background:var(--input-bg);border:1px solid var(--border);border-radius:20px;font-size:12px;cursor:pointer;color:var(--muted);">💻 Write JS code</div>'+
            '</div></div>';
        return;
    }
    el.innerHTML=msgs.map(function(m){
        var isUser=m.role==='user';
        return '<div style="display:flex;gap:12px;justify-content:'+(isUser?'flex-end':'flex-start')+';margin-bottom:20px;align-items:flex-start;">'+
            (isUser?'':'<div style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#00d4ff,#8b5cf6);display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:0 4px 12px rgba(0,212,255,0.25);"><i class="fa-solid fa-robot" style="font-size:14px;color:#fff;"></i></div>')+
            '<div style="max-width:75%;padding:12px 16px;border-radius:18px;font-size:14px;line-height:1.6;background:'+(isUser?'linear-gradient(135deg,#00d4ff,#8b5cf6)':'var(--card)')+';color:'+(isUser?'#fff':'var(--text)')+';word-wrap:break-word;overflow-wrap:break-word;'+(isUser?'border-bottom-right-radius:4px;':'border-bottom-left-radius:4px;border:1px solid var(--border);')+'">'+
            (isUser?m.text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\\n/g,'<br>'):formatAIText(m.text))+'</div>'+
            (isUser?'<div style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#3a3a4a,#5a5a6a);display:flex;align-items:center;justify-content:center;flex-shrink:0;"><i class="fa-solid fa-user" style="font-size:14px;color:#fff;"></i></div>':'')+
            '</div>';
    }).join('');
    el.scrollTop=el.scrollHeight;
}

function quickAsk(msg){
    var input=document.getElementById('ai-input');
    if(input){input.value=msg;}
    sendAIMessage();
}"""

if match2:
    c = c[:match2.start()] + new_load + c[match2.end():]
    print("2. loadAIChat: OK")
else:
    print("2. loadAIChat: LAMA HELIN")

# 3. sendAIMessage typing indicator
old_send = "el.innerHTML+='<div style=\"display:flex;justify-content:flex-start;margin-bottom:12px;\"><div style=\"max-width:80%;padding:10px 14px;border-radius:12px;font-size:13px;background:var(--card);color:var(--muted);\">Typing...</div></div>';"
new_send = "el.innerHTML+='<div style=\"display:flex;gap:12px;margin-bottom:20px;\"><div style=\"width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#00d4ff,#8b5cf6);display:flex;align-items:center;justify-content:center;flex-shrink:0;\"><i class=\"fa-solid fa-robot\" style=\"font-size:14px;color:#fff;\"></i></div><div style=\"padding:12px 16px;border-radius:18px;border-bottom-left-radius:4px;background:var(--card);border:1px solid var(--border);color:var(--muted);font-size:14px;\"><i class=\"fa-solid fa-circle-notch fa-spin\"></i> AI wuu fikirayaa...</div></div>';"

if old_send in c:
    c = c.replace(old_send, new_send, 1)
    print("3. Typing: OK")
else:
    print("3. Typing: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_ai_modern")
