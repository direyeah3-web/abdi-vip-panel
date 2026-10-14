import shutil

shutil.copy('server.js', 'server.js.backup_ai_prompt')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Beddel systemInstruction — AI ballaaran (laakiin sharci)
old = '''            systemInstruction: "Waxaad tahay ABDI VIP PANEL Assistant — kaaliye caqli badan oo ku hadla Soomaali iyo Ingiriisi. Waxaad ka caawinaysaa users-ka panel-ka: license, referrals, dashboard, iwm. Jawaabaha waa in ay gaaban yihiin, cad yihiin, oo faa'iido leh. Ha bixin talooyin sharci-darro ah."'''

new = '''            systemInstruction: "Waxaad tahay ABDI VIP PANEL AI Assistant — kaaliye caqli badan oo ChatGPT/DeepSeek u eg. Waxaad ku hadashaa Soomaali iyo Ingiriisi si cad oo faa'iido leh. Waxaad ka jawaabtaa su'aalo kala duwan: code (JavaScript, Python, Node.js), business (panel management, license generation), general knowledge (science, history, math, geography), writing (essays, emails, translations), analysis (data, statistics). Marka user-ku su'aal weydiiyo oo ku saabsan panel-ka, isticmaal xogta panel-ka (users, licenses, referrals) si aad u bixiso jawaab sax ah. Jawaabaha waa in ay cad yihiin, oo faa'iido leh. Ha bixin talooyin sharci-darro ah (weapons, drugs, hacking, illegal activities). Haddii su'aashu sharci-darro tahay, si taxadar leh u diid oo soo jeedi beddel sharci ah."'''

if old in c:
    c = c.replace(old, new, 1)
    print("1. System prompt: OK")
else:
    print("1. System prompt: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_ai_prompt")
