import shutil
import re

shutil.copy('public/index.html', 'public/index.html.backup_ai_mobile')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Beddel panel-ka AI — mobile-friendly layout
old_panel = '''<div class="panel" style="display:flex;flex-direction:column;height:650px;max-height:75vh;padding:0;overflow:hidden;">'''

new_panel = '''<div class="panel ai-chat-container" style="display:flex;flex-direction:column;height:calc(100dvh - 180px);min-height:400px;max-height:700px;padding:0;overflow:hidden;">'''

if old_panel in c:
    c = c.replace(old_panel, new_panel, 1)
    print("1. Panel height: OK")
else:
    print("1. Panel height: LAMA HELIN")

# 2. Beddel messages area — flex-1 + overflow
old_msgs = '''<div id="ai-messages" style="flex:1;overflow-y:auto;padding:20px;background:var(--bg);"></div>'''

new_msgs = '''<div id="ai-messages" class="ai-messages-scroll" style="flex:1;overflow-y:auto;padding:16px;background:var(--bg);-webkit-overflow-scrolling:touch;"></div>'''

if old_msgs in c:
    c = c.replace(old_msgs, new_msgs, 1)
    print("2. Messages area: OK")
else:
    print("2. Messages area: LAMA HELIN")

# 3. Beddel input area — safe-area + 16px font
old_input_area = '''<div style="padding:15px;border-top:1px solid var(--border);background:var(--card);">'''

new_input_area = '''<div class="ai-input-area" style="padding:12px;border-top:1px solid var(--border);background:var(--card);padding-bottom:calc(12px + env(safe-area-inset-bottom));">'''

if old_input_area in c:
    c = c.replace(old_input_area, new_input_area, 1)
    print("3. Input area: OK")
else:
    print("3. Input area: LAMA HELIN")

# 4. Beddel textarea — 16px font (iOS no zoom)
old_textarea = '''style="flex:1;padding:10px 8px;background:transparent;border:none;color:var(--text);outline:none;resize:none;font-family:inherit;font-size:14px;max-height:120px;line-height:1.5;"'''

new_textarea = '''style="flex:1;padding:10px 8px;background:transparent;border:none;color:var(--text);outline:none;resize:none;font-family:inherit;font-size:16px;max-height:120px;line-height:1.5;"'''

if old_textarea in c:
    c = c.replace(old_textarea, new_textarea, 1)
    print("4. Textarea font: OK")
else:
    print("4. Textarea font: LAMA HELIN")

# 5. Ku dar CSS — mobile-specific
if '.ai-chat-container' not in c:
    css_insert = """<style>
.ai-chat-container { scroll-behavior: smooth; }
.ai-messages-scroll::-webkit-scrollbar { width: 4px; }
.ai-messages-scroll::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
@media (max-width: 768px) {
    .ai-chat-container {
        height: calc(100dvh - 160px) !important;
        max-height: none !important;
        border-radius: 0 !important;
        margin: -15px !important;
    }
    .ai-messages-scroll { padding: 12px !important; }
    .ai-input-area { padding: 10px !important; padding-bottom: calc(10px + env(safe-area-inset-bottom)) !important; }
}
</style>"""
    if '</head>' in c:
        c = c.replace('</head>', css_insert + '</head>', 1)
        print("5. Mobile CSS: OK")
    else:
        print("5. Mobile CSS: </head> LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_ai_mobile")
