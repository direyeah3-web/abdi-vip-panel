import shutil
import re

shutil.copy('public/index.html', 'public/index.html.backup_ai_style')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Beddel "AI wuu fikirayaa" — qoraal degdeg ah
old_typing = '''<i class="fa-solid fa-circle-notch fa-spin"></i> AI wuu fikirayaa...'''
new_typing = '''<span style="display:inline-block;">●</span> <span style="display:inline-block;animation:pulse 1.4s infinite;">●</span> <span style="display:inline-block;animation:pulse 1.4s infinite 0.2s;">●</span>'''

if old_typing in c:
    c = c.replace(old_typing, new_typing, 1)
    print("1. Typing dots: OK")
else:
    print("1. Typing dots: LAMA HELIN")

# 2. Ku dar CSS animation (ka hor </style> ama </head>)
if '@keyframes pulse' not in c:
    css_insert = """<style>
@keyframes pulse {0%,100%{opacity:0.3;}50%{opacity:1;}}
.ai-fade-in {animation:aiFadeIn 0.3s ease-out;}
@keyframes aiFadeIn {from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:translateY(0);}}
</style>"""
    if '</head>' in c:
        c = c.replace('</head>', css_insert + '</head>', 1)
        print("2. CSS animation: OK")
    else:
        print("2. CSS: </head> LAMA HELIN")

# 3. Beddel system prompt — emoji + degdeg + fun
old_prompt = '''systemInstruction: "Waxaad tahay ABDI VIP PANEL AI Assistant — kaaliye caqli badan oo ChatGPT/DeepSeek u eg. Waxaad ku hadashaa Soomaali iyo Ingiriisi si cad oo faa'iido leh. Waxaad ka jawaabtaa su'aalo kala duwan: code (JavaScript, Python, Node.js), business (panel management, license generation), general knowledge (science, history, math, geography), writing (essays, emails, translations), analysis (data, statistics). Marka user-ku su'aal weydiiyo oo ku saabsan panel-ka, isticmaal xogta panel-ka (users, licenses, referrals) si aad u bixiso jawaab sax ah. Jawaabaha waa in ay cad yihiin, oo faa'iido leh. Ha bixin talooyin sharci-darro ah (weapons, drugs, hacking, illegal activities). Haddii su'aashu sharci-darro tahay, si taxadar leh u diid oo soo jeedi beddel sharci ah."'''

new_prompt = '''systemInstruction: "Waxaad tahay ABDI VIP PANEL AI Assistant — saaxiib caqli badan oo ChatGPT/DeepSeek u eg, laakiin fun badan. Waxaad ku hadashaa Soomaali iyo Ingiriisi si degdeg ah, gaaban, oo casri ah. Isticmaal emoji-ga badan sida 😂😭🔥💯✨👋👍🎯🚀💻🧠. Jawaabahaagu waa in ay gaaban yihiin (1-3 sadar), degdeg ah, oo aan buuq lahayn. Waxaad ka jawaabtaa su'aalo kala duwan: code, business, general knowledge, writing, analysis. Haddii user-ku su'aal weydiiyo oo panel-ka ku saabsan, isticmaal xogta panel-ka (users, licenses, referrals) si aad u bixiso jawaab sax ah. Ka fogow hadal dheer, ka fogow buuq, ka fogow faafin. Haddii su'aashu sharci-darro tahay, si fudud u diid (1 sadar) oo soo jeedi beddel sharci ah. Waxaad tahay mid fun ah, laakiin mid xushmad leh."'''

if old_prompt in c:
    c = c.replace(old_prompt, new_prompt, 1)
    print("3. System prompt: OK")
else:
    print("3. System prompt: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_ai_style")
