# replace_revenue_final.py - Tirtir Revenue card oo dhan, ku dar Profile Card

with open("public/index.html", "r") as f:
    content = f.read()

# ===== 1. TIRTIR REVENUE CARD OO DHAN =====
# Hel qaybta Revenue (laga bilaabo '<h3>Revenue</h3>' ilaa dhammaadka panel-ka)
start_marker = "'<div class=\"panel\"><div class=\"panel-header\"><h3>Revenue</h3>"
end_marker = "'</div></div></div><div class=\"panel\"><div class=\"panel-header\"><h3>Top Users</h3>"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    # Qaybta cusub ee Profile Card
    profile_card = '''<div class="panel" style="position:relative;overflow:hidden;">
                <div class="panel-header"><h3>Profile</h3><span style="color:var(--primary);font-size:13px;font-weight:600;"><i class="fa-solid fa-crown"></i> Admin</span></div>
                <div style="display:flex;flex-direction:column;align-items:center;padding:20px 0;position:relative;z-index:1;">
                    <div style="width:100px;height:100px;border-radius:50%;overflow:hidden;border:4px solid var(--primary);box-shadow:0 0 40px rgba(139,92,246,0.5);margin-bottom:16px;animation:floaty 4s ease-in-out infinite;">
                        <img src="/logo.png" alt="ABDI VIP" style="width:100%;height:100%;object-fit:cover;">
                    </div>
                    <div style="font-size:22px;font-weight:800;background:linear-gradient(135deg,#fff,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:4px;">ABDI VIP</div>
                    <div style="color:var(--muted);font-size:13px;">Autonomous Panel Owner</div>
                </div>
            </div>'''
    
    # Beddel qaybta Revenue
    content = content[:start_idx] + profile_card + content[end_idx:]
    print("✅ Revenue card waa la tirtiray, Profile Card casri ah waa lagu daray!")
else:
    print("⚠️ Revenue card lama helin")

# ===== 2. KU DAR PROFILE CARD CSS =====
profile_css = """
.profile-card-bg::before { content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle,rgba(139,92,246,0.15) 0%,transparent 60%);animation:floaty 6s ease-in-out infinite;pointer-events:none; }
"""

if "</style>" in content:
    content = content.replace("</style>", profile_css + "\n</style>", 1)

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
