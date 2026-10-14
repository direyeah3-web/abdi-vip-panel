import shutil
import re

shutil.copy('public/index.html', 'public/index.html.backup_ai_upload_ui')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Beddel page logic — ku dar upload button + preview
old_page = '''<div style="padding:15px;border-top:1px solid var(--border);background:var(--card);">'+
                    '<div style="display:flex;gap:10px;align-items:flex-end;background:var(--input-bg);border:1px solid var(--border);border-radius:14px;padding:6px 6px 6px 16px;">'+
                        '<textarea id="ai-input" placeholder="Weydii wax..." rows="1" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" name="ai-message-'+Date.now()+'" style="flex:1;padding:10px 0;background:transparent;border:none;color:var(--text);outline:none;resize:none;font-family:inherit;font-size:14px;max-height:120px;line-height:1.5;" onkeydown="if(event.key===&quot;Enter&quot;&amp;&amp;!event.shiftKey){event.preventDefault();sendAIMessage()}" oninput="this.style.height=&quot;auto&quot;;this.style.height=Math.min(this.scrollHeight,120)+&quot;px&quot;;this.style.overflowY=this.scrollHeight>120?&quot;auto&quot;:&quot;hidden&quot;;"></textarea>'+
                        '<button onclick="sendAIMessage()" id="ai-send-btn" style="width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,#00d4ff,#8b5cf6);border:none;color:#fff;cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center;"><i class="fa-solid fa-arrow-up" style="font-size:16px;"></i></button>'+
                    '</div>'+
                    '<div style="font-size:11px;color:var(--muted);text-align:center;margin-top:8px;">AI-ga waxaa laga yaabaa in uu khaldanaado. Hubi macluumaadka muhiimka ah.</div>'+
                '</div>'''

new_page = '''<div style="padding:15px;border-top:1px solid var(--border);background:var(--card);">'+
                    '<div id="ai-file-preview" style="display:none;margin-bottom:10px;padding:10px;background:var(--input-bg);border-radius:10px;position:relative;"></div>'+
                    '<div style="display:flex;gap:10px;align-items:flex-end;background:var(--input-bg);border:1px solid var(--border);border-radius:14px;padding:6px;">'+
                        '<input type="file" id="ai-file-input" accept="image/*,video/*,text/*,.pdf" style="display:none;" onchange="handleAIFile(this)">'+
                        '<button onclick="document.getElementById(&quot;ai-file-input&quot;).click()" title="Upload file" style="width:38px;height:38px;border-radius:10px;background:transparent;border:none;color:var(--muted);cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center;"><i class="fa-solid fa-paperclip" style="font-size:18px;"></i></button>'+
                        '<textarea id="ai-input" placeholder="Weydii wax..." rows="1" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" name="ai-message-'+Date.now()+'" style="flex:1;padding:10px 8px;background:transparent;border:none;color:var(--text);outline:none;resize:none;font-family:inherit;font-size:14px;max-height:120px;line-height:1.5;" onkeydown="if(event.key===&quot;Enter&quot;&amp;&amp;!event.shiftKey){event.preventDefault();sendAIMessage()}" oninput="this.style.height=&quot;auto&quot;;this.style.height=Math.min(this.scrollHeight,120)+&quot;px&quot;;this.style.overflowY=this.scrollHeight>120?&quot;auto&quot;:&quot;hidden&quot;;"></textarea>'+
                        '<button onclick="sendAIMessage()" id="ai-send-btn" style="width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,#00d4ff,#8b5cf6);border:none;color:#fff;cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center;"><i class="fa-solid fa-arrow-up" style="font-size:16px;"></i></button>'+
                    '</div>'+
                    '<div style="font-size:11px;color:var(--muted);text-align:center;margin-top:8px;">AI-ga waxaa laga yaabaa in uu khaldanaado. Hubi macluumaadka muhiimka ah.</div>'+
                '</div>'''

if old_page in c:
    c = c.replace(old_page, new_page, 1)
    print("1. Page upload UI: OK")
else:
    print("1. Page upload UI: LAMA HELIN")

# 2. Ku dar functions — ka hor loadTelegramStatus
old_func = "async function loadTelegramStatus(){"
new_func = """var aiPendingFile = null;

function handleAIFile(input){
    var file = input.files[0];
    if(!file) return;
    if(file.size > 20 * 1024 * 1024){
        showToast('Warning','File waa weyn (max 20MB)','info');
        return;
    }
    aiPendingFile = file;
    var preview = document.getElementById('ai-file-preview');
    if(!preview) return;
    preview.style.display = 'block';
    if(file.type.startsWith('image/')){
        var url = URL.createObjectURL(file);
        preview.innerHTML = '<div style="display:flex;align-items:center;gap:10px;">'+
            '<img src="'+url+'" style="width:60px;height:60px;object-fit:cover;border-radius:8px;">'+
            '<div style="flex:1;font-size:12px;"><b>'+file.name+'</b><br><span style="color:var(--muted);">'+(file.size/1024).toFixed(1)+' KB</span></div>'+
            '<button onclick="removeAIFile()" style="background:transparent;border:none;color:var(--red);cursor:pointer;font-size:18px;">&times;</button>'+
            '</div>';
    } else {
        preview.innerHTML = '<div style="display:flex;align-items:center;gap:10px;">'+
            '<div style="width:60px;height:60px;background:var(--card);border-radius:8px;display:flex;align-items:center;justify-content:center;"><i class="fa-solid fa-file" style="font-size:24px;color:var(--primary);"></i></div>'+
            '<div style="flex:1;font-size:12px;"><b>'+file.name+'</b><br><span style="color:var(--muted);">'+(file.size/1024).toFixed(1)+' KB</span></div>'+
            '<button onclick="removeAIFile()" style="background:transparent;border:none;color:var(--red);cursor:pointer;font-size:18px;">&times;</button>'+
            '</div>';
    }
}

function removeAIFile(){
    aiPendingFile = null;
    var input = document.getElementById('ai-file-input');
    if(input) input.value = '';
    var preview = document.getElementById('ai-file-preview');
    if(preview) preview.style.display = 'none';
}

async function loadTelegramStatus(){"""

if old_func in c:
    c = c.replace(old_func, new_func, 1)
    print("2. handleAIFile: OK")
else:
    print("2. handleAIFile: LAMA HELIN")

# 3. Beddel sendAIMessage — file upload support
old_send_pattern = r"async function sendAIMessage\(\)\{.*?\n\}"
match_send = re.search(old_send_pattern, c, re.DOTALL)

new_send = """async function sendAIMessage(){
    var input=document.getElementById('ai-input');
    var btn=document.getElementById('ai-send-btn');
    var msg=input.value.trim();
    if(!msg && !aiPendingFile)return;
    input.value='';
    input.style.height='auto';
    btn.disabled=true;
    btn.innerHTML='<i class="fa-solid fa-spinner fa-spin"></i>';
    var msgs=JSON.parse(localStorage.getItem('ai_chat')||'[]');
    var userMsg = {role:'user',text:msg || '(file)'};
    if(aiPendingFile){
        userMsg.fileName = aiPendingFile.name;
        userMsg.fileType = aiPendingFile.type;
        if(aiPendingFile.type.startsWith('image/')){
            userMsg.filePreview = URL.createObjectURL(aiPendingFile);
        }
    }
    msgs.push(userMsg);
    localStorage.setItem('ai_chat',JSON.stringify(msgs));
    loadAIChat();
    var el=document.getElementById('ai-messages');
    el.innerHTML+='<div style="display:flex;gap:12px;margin-bottom:20px;"><div style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#00d4ff,#8b5cf6);display:flex;align-items:center;justify-content:center;flex-shrink:0;"><i class="fa-solid fa-robot" style="font-size:14px;color:#fff;"></i></div><div style="padding:12px 16px;border-radius:18px;border-bottom-left-radius:4px;background:var(--card);border:1px solid var(--border);color:var(--muted);font-size:14px;"><span style="color:var(--muted);font-size:13px;">Wuu qorayaa...</span></div></div>';
    el.scrollTop=el.scrollHeight;
    try{
        var t=localStorage.getItem('token');
        var r;
        if(aiPendingFile){
            var formData = new FormData();
            formData.append('file', aiPendingFile);
            formData.append('message', msg || 'Falanqee file-kan.');
            formData.append('history', JSON.stringify(msgs.slice(-10)));
            r = await fetch('/api/ai/chat-with-file',{method:'POST',headers:{'Authorization':'Bearer '+t},body:formData});
        } else {
            r = await fetch('/api/ai/chat',{method:'POST',headers:{'Authorization':'Bearer '+t,'Content-Type':'application/json'},body:JSON.stringify({message:msg,history:msgs.slice(-10)})});
        }
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
    btn.innerHTML='<i class="fa-solid fa-arrow-up" style="font-size:16px;"></i>';
    aiPendingFile = null;
    removeAIFile();
}"""

if match_send:
    c = c[:match_send.start()] + new_send + c[match_send.end():]
    print("3. sendAIMessage: OK")
else:
    print("3. sendAIMessage: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_ai_upload_ui")
