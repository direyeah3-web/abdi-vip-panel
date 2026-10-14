import shutil
import re

shutil.copy('public/index.html', 'public/index.html.backup_ai_ui_safe')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Raadi function-ka loadAIChat (hadda jira)
pattern = r"function loadAIChat\(\)\{.*?\n\}"
match = re.search(pattern, c, re.DOTALL)

# Beddel kaliya qaybta message rendering — ChatGPT-like bubbles
new_load = """function formatAIText(text){
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
        el.innerHTML='<div style="text-align:center;color:var(--muted);padding:40px 20px;">'+
            '<div style="width:70px;height:70px;border-radius:50%;background:linear-gradient(135deg,#00d4ff,#8b5cf6);display:inline-flex;align-items:center;justify-content:center;margin-bottom:15px;">'+
            '<i class="fa-solid fa-robot" style="font-size:30px;color:#fff;"></i></div>'+
            '<h2 style="font-size:18px;font-weight:700;color:var(--text);margin-bottom:8px;">Ku soo dhawoow AI Assistant</h2>'+
            '<p style="font-size:13px;max-width:400px;margin:0 auto;line-height:1.6;">Weydii wax kasta: license, referrals, dashboard, code, ama su\\'aalo kale.</p>'+
            '</div>';
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

if match:
    c = c[:match.start()] + new_load + c[match.end():]
    print("1. loadAIChat (safe): OK")
else:
    print("1. loadAIChat: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_ai_ui_safe")
