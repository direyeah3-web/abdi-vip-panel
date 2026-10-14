import shutil

shutil.copy('server.js', 'server.js.backup_ai_fix')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Beddel systemInstruction — single quotes → double quotes
old = """            systemInstruction: 'Waxaad tahay ABDI VIP PANEL Assistant — kaaliye caqli badan oo ku hadla Soomaali iyo Ingiriisi. Waxaad ka caawinaysaa users-ka panel-ka: license, referrals, dashboard, iwm. Jawaabaha waa in ay gaaban yihiin, cad yihiin, oo faa'iido leh. Ha bixin talooyin sharci-darro ah.'"""

new = """            systemInstruction: "Waxaad tahay ABDI VIP PANEL Assistant — kaaliye caqli badan oo ku hadla Soomaali iyo Ingiriisi. Waxaad ka caawinaysaa users-ka panel-ka: license, referrals, dashboard, iwm. Jawaabaha waa in ay gaaban yihiin, cad yihiin, oo faa'iido leh. Ha bixin talooyin sharci-darro ah." """

if old in c:
    c = c.replace(old, new, 1)
    print("1. systemInstruction: OK")
else:
    print("1. systemInstruction: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_ai_fix")
