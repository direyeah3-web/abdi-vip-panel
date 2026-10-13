# replace_revenue.py - Beddel Revenue Card sawirkaaga

with open("public/index.html", "r") as f:
    content = f.read()

# Calaamadda Revenue hore
old_revenue = '''<div class="panel"><div class="panel-header"><h3>Revenue</h3><span style="color:var(--green);font-size:13px;font-weight:600;"><i class="fa-solid fa-arrow-up"></i> +12.5%</span></div><div style="display:flex;align-items:center;gap:20px;padding:10px 0;"><div style="width:60px;height:60px;background:linear-gradient(135deg,var(--primary),var(--purple));border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:24px;color:#fff;"><i class="fa-solid fa-dollar-sign"></i></div><div><div style="font-size:36px;font-weight:800;">$2,500</div><div style="color:var(--muted);font-size:13px;">Total revenue this month</div></div></div></div>'''

# Sawirkaaga - Beddel "logo.png" haddii aad rabto sawir kale
new_revenue = '''<div class="panel"><div class="panel-header"><h3>Welcome</h3><span style="color:var(--primary);font-size:13px;font-weight:600;"><i class="fa-solid fa-crown"></i> Admin</span></div><div style="display:flex;align-items:center;gap:20px;padding:10px 0;"><div style="width:80px;height:80px;border-radius:50%;overflow:hidden;border:3px solid var(--primary);box-shadow:0 0 30px rgba(139,92,246,0.4);"><img src="/logo.png" alt="Profile" style="width:100%;height:100%;object-fit:cover;"></div><div><div style="font-size:20px;font-weight:800;color:var(--text);">ABDI VIP</div><div style="color:var(--muted);font-size:13px;">Autonomous Panel Owner</div></div></div></div>'''

if old_revenue in content:
    content = content.replace(old_revenue, new_revenue)
    print("✅ Revenue card waa la beddelay sawirkaaga!")
else:
    print("⚠️ Revenue card lama helin — isku day qaab kale")

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
