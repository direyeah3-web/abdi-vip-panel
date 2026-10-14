import shutil
import re

shutil.copy('public/index.html', 'public/index.html.backup_ai_iphone')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Beddel AI panel — iPhone-style wrapper
old_panel_pattern = r"<div class=\"panel ai-chat-container\".*?overflow:hidden;\">"
new_panel = '''<div class="ai-chat-wrapper" style="display:flex;flex-direction:column;height:100%;max-height:none;padding:0;overflow:hidden;position:relative;">'''

match = re.search(old_panel_pattern, c, re.DOTALL)
if match:
    c = c[:match.start()] + new_panel + c[match.end():]
    print("1. Panel wrapper: OK")
else:
    print("1. Panel wrapper: LAMA HELIN")

# 2. Beddel page logic — header + chat wrapper
old_page = '''c.innerHTML='<div class="panel-header" style="margin-bottom:20px;"><h1 style="font-size:24px;font-weight:800;"><i class="fa-solid fa-robot" style="color:var(--primary);"></i> AI Assistant</h1><button class="btn-secondary" onclick="clearAIChat()"><i class="fa-solid fa-trash"></i> Clear</button></div>'+'''

new_page = '''c.innerHTML='<div class="ai-page-container" style="display:flex;flex-direction:column;height:100%;">'+
            '<div class="panel-header" style="margin-bottom:12px;flex-shrink:0;"><h1 style="font-size:20px;font-weight:800;"><i class="fa-solid fa-robot" style="color:var(--primary);"></i> AI Assistant</h1><button class="btn-secondary" onclick="clearAIChat()" style="padding:8px 12px;font-size:12px;"><i class="fa-solid fa-trash"></i></button></div>'+'''

if old_page in c:
    c = c.replace(old_page, new_page, 1)
    print("2. Page header: OK")
else:
    print("2. Page header: LAMA HELIN")

# 3. Ku dar wrapper-ka dhamaystirka — messages + input area oo leh position sticky
old_close = "'''<div class=\"ai-input-area\""
# Halkan waa qaybta u dambaysa page logic — waa in aan ku darnaa </div> dheeraad ah
old_end = '''            '</div>';
            loadAIChat();
        }'''

new_end = '''            '</div>'+
            '</div>';
            loadAIChat();
            setTimeout(function(){var i=document.getElementById('ai-input');if(i)i.focus();},300);
        }'''

if old_end in c:
    c = c.replace(old_end, new_end, 1)
    print("3. Page close: OK")
else:
    print("3. Page close: LAMA HELIN")

# 4. Beddel input area — position sticky hoose
old_input = '''<div class="ai-input-area" style="padding:12px;border-top:1px solid var(--border);background:var(--card);padding-bottom:calc(12px + env(safe-area-inset-bottom));">'''

new_input = '''<div class="ai-input-area" style="position:sticky;bottom:0;padding:10px 12px;border-top:1px solid var(--border);background:var(--card);padding-bottom:calc(10px + env(safe-area-inset-bottom));flex-shrink:0;z-index:10;">'''

if old_input in c:
    c = c.replace(old_input, new_input, 1)
    print("4. Input sticky: OK")
else:
    print("4. Input sticky: LAMA HELIN")

# 5. CSS — iPhone-like layout
old_css_start = '.ai-chat-container { scroll-behavior: smooth; }'

new_css = '''.ai-chat-wrapper { position: relative; }
.ai-page-container { height: 100%; }
.ai-messages-scroll { scroll-behavior: smooth; -webkit-overflow-scrolling: touch; }
@media (max-width: 768px) {
    .ai-page-container { height: calc(100dvh - 140px) !important; }
    .ai-chat-wrapper { border-radius: 0 !important; margin: 0 !important; }
    .ai-messages-scroll { padding: 12px !important; }
    .ai-input-area { border-radius: 0 !important; }
    .panel-header h1 { font-size: 18px !important; }
}
.ai-messages-scroll::-webkit-scrollbar { width: 4px; }
.ai-messages-scroll::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }'''

if old_css_start in c:
    c = c.replace(old_css_start, new_css, 1)
    print("5. CSS: OK")
else:
    print("5. CSS: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_ai_iphone")
