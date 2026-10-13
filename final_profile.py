# final_profile.py - Sawirkaaga oo keliya, qoraalka oo dhan la tirtiray

with open("public/index.html", "r") as f:
    content = f.read()

import re

# Hel qaybta Revenue (laga bilaabo '<h3>Revenue</h3>' ilaa Top Users)
start_marker = "'<div class=\"panel\"><div class=\"panel-header\"><h3>Revenue</h3>"
end_marker = "'<div class=\"panel\"><div class=\"panel-header\"><h3>Top Users</h3>"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    # Qaybta cusub - Sawirkaaga oo keliya
    profile_card = '''<div class="panel" style="display:flex;align-items:center;justify-content:center;padding:30px;position:relative;overflow:hidden;">
                <div style="position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle,rgba(139,92,246,0.2) 0%,transparent 60%);animation:floaty 6s ease-in-out infinite;pointer-events:none;"></div>
                <div style="position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;">
                    <div style="width:120px;height:120px;border-radius:50%;overflow:hidden;border:4px solid var(--primary);box-shadow:0 0 50px rgba(139,92,246,0.6),0 0 100px rgba(139,92,246,0.3);animation:floaty 4s ease-in-out infinite;">
                        <img src="/logo.png" alt="Profile" style="width:100%;height:100%;object-fit:cover;">
                    </div>
                </div>
            </div>'''
    
    # Beddel qaybta Revenue
    content = content[:start_idx] + profile_card + content[end_idx:]
    print("✅ Qoraalka oo dhan waa la tirtiray, sawirkaaga oo keliya waa la saaray!")
else:
    print("⚠️ Revenue card lama helin")

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
