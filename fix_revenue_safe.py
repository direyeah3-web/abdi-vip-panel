# fix_revenue_safe.py - Beddel Revenue card si taxadar leh

with open("public/index.html", "r") as f:
    content = f.read()

# Calaamadda saxda ah - qaybta $2,500
old_marker = '<div style="font-size:36px;font-weight:800;">$2,500</div><div style="color:var(--muted);font-size:13px;">Total revenue this month</div>'

# Qaybta cusub - sawirkaaga oo keliya
new_marker = '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:10px 0;"><div style="width:90px;height:90px;border-radius:50%;overflow:hidden;border:3px solid var(--primary);box-shadow:0 0 30px rgba(139,92,246,0.5);animation:floaty 4s ease-in-out infinite;"><img src="/logo.png" alt="ABDI VIP" style="width:100%;height:100%;object-fit:cover;"></div></div>'

if old_marker in content:
    content = content.replace(old_marker, new_marker)
    print("✅ Revenue card waa la beddelay sawirkaaga oo keliya!")
else:
    print("⚠️ Calaamadda lama helin — isku day qaab kale")

# Tirtir "+12.5%" oo keliya
content = content.replace('<span style="color:var(--green);font-size:13px;font-weight:600;"><i class="fa-solid fa-arrow-up"></i> +12.5%</span>', '')
print("✅ +12.5% waa la tirtiray!")

# Tirtir "<h3>Revenue</h3>" oo keliya
content = content.replace('<h3>Revenue</h3>', '<h3>Profile</h3>')
print("✅ Revenue → Profile!")

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
