# replace_revenue_v2.py - Beddel $2,500 oo ku dar sawirkaaga

with open("public/index.html", "r") as f:
    content = f.read()

# Calaamadda saxda ah - qaybta $2,500
old_marker = '''<div style="font-size:36px;font-weight:800;">$2,500</div><div style="color:var(--muted);font-size:13px;">Total revenue this month</div>'''

# Sawirkaaga - Beddel logo.png haddii aad rabto sawir kale
new_marker = '''<div style="display:flex;align-items:center;gap:15px;"><div style="width:70px;height:70px;border-radius:50%;overflow:hidden;border:3px solid var(--primary);box-shadow:0 0 25px rgba(139,92,246,0.4);"><img src="/logo.png" alt="ABDI VIP" style="width:100%;height:100%;object-fit:cover;"></div><div><div style="font-size:22px;font-weight:800;background:linear-gradient(135deg,#fff,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">ABDI VIP</div><div style="color:var(--muted);font-size:13px;">Autonomous Panel Owner</div></div></div>'''

if old_marker in content:
    content = content.replace(old_marker, new_marker)
    print("✅ $2,500 waa la beddelay sawirkaaga!")
else:
    print("⚠️ Calaamadda lama helin — isku day qaab kale")

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
