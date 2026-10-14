# navy_theme.py - Navy Blue Theme (sida sawirka)
import shutil

# Backup
shutil.copy("public/index.html", "public/index.html.backup_navy")
print("✅ Backup waa la sameeyay!")

with open("public/index.html", "r") as f:
    content = f.read()

# ===== 1. BEDDEL CSS-KA LIGHT MODE =====
old_light = '''[data-theme="light"]{--bg:#faf6f0;--sidebar:#fffbf5;--card:#ffffff;--card-hover:#f5ede0;--text:#3d2e1f;--muted:#8b7355;--primary:#e07a5f;--purple:#c17c5a;--green:#7a9e7e;--yellow:#d4a373;--red:#c75c5c;--border:#f0e6d6;}'''

new_light = '''[data-theme="light"]{
    --bg:#0d1b2a;
    --sidebar:#0f2236;
    --card:#142a42;
    --card-hover:#1a3554;
    --text:#e6f1ff;
    --muted:#7b98b8;
    --primary:#00d4ff;
    --purple:#8b5cf6;
    --green:#10b981;
    --yellow:#f59e0b;
    --red:#ef4444;
    --border:#1e3a5f;
}'''

if old_light in content:
    content = content.replace(old_light, new_light)
    print("✅ Navy Blue CSS waa lagu daray!")

# ===== 2. BEDDEL QAYBAHA KALE =====
content = content.replace(
    '[data-theme="light"] body{background:linear-gradient(135deg,#faf6f0 0%,#f5ede0 50%,#faf6f0 100%) !important;}',
    '[data-theme="light"] body{background:linear-gradient(135deg,#0d1b2a 0%,#0f2236 50%,#0d1b2a 100%) !important;}'
)
content = content.replace(
    '[data-theme="light"] .sidebar{background:linear-gradient(180deg,#fffbf5,#f5ede0) !important;border-right:1px solid #f0e6d6;}',
    '[data-theme="light"] .sidebar{background:linear-gradient(180deg,#0f2236,#0d1b2a) !important;border-right:1px solid #1e3a5f;}'
)
content = content.replace(
    '[data-theme="light"] .card,[data-theme="light"] .stat-card,[data-theme="light"] .panel,[data-theme="light"] .hero{background:linear-gradient(135deg,#ffffff,#fdf9f3) !important;border:1px solid #f0e6d6 !important;box-shadow:0 4px 20px rgba(224,122,95,0.08) !important;}',
    '[data-theme="light"] .card,[data-theme="light"] .stat-card,[data-theme="light"] .panel,[data-theme="light"] .hero{background:linear-gradient(135deg,#142a42,#0f2236) !important;border:1px solid #1e3a5f !important;box-shadow:0 4px 20px rgba(0,212,255,0.1) !important;}'
)
content = content.replace(
    '[data-theme="light"] input,[data-theme="light"] select{background:#fffbf5 !important;border:1px solid #f0e6d6 !important;color:#3d2e1f !important;}',
    '[data-theme="light"] input,[data-theme="light"] select{background:#0d1b2a !important;border:1px solid #1e3a5f !important;color:#e6f1ff !important;}'
)

# ===== 3. KU DAR QAYBAHA KALE EE NAVY =====
navy_css = """
[data-theme="light"] .quick-action{background:#0d1b2a !important;border:1px solid #1e3a5f;}
[data-theme="light"] .quick-action:hover{background:#1a3554 !important;border-color:#00d4ff !important;}
[data-theme="light"] .nav-item:hover,[data-theme="light"] .nav-item.active{background:linear-gradient(135deg,rgba(0,212,255,0.15),rgba(139,92,246,0.15)) !important;color:#00d4ff !important;}
[data-theme="light"] .topnav{background:rgba(15,34,54,0.9) !important;border-bottom:1px solid #1e3a5f !important;backdrop-filter:blur(20px);}
[data-theme="light"] .btn-primary{background:linear-gradient(135deg,#00d4ff,#8b5cf6) !important;color:white !important;}
[data-theme="light"] .submit-btn{background:linear-gradient(135deg,#00d4ff,#8b5cf6) !important;color:white !important;}
[data-theme="light"] .stat-value{background:linear-gradient(135deg,#00d4ff,#8b5cf6) !important;-webkit-background-clip:text !important;-webkit-text-fill-color:transparent !important;background-clip:text !important;}
[data-theme="light"] .live-clock{background:#0d1b2a !important;border:1px solid #1e3a5f !important;color:#00d4ff !important;}
[data-theme="light"] .online-badge{background:rgba(16,185,129,0.15) !important;border:1px solid rgba(16,185,129,0.3) !important;color:#10b981 !important;}
[data-theme="light"] .icon-btn{background:#142a42 !important;border:1px solid #1e3a5f !important;color:#e6f1ff !important;}
[data-theme="light"] .toast{background:linear-gradient(135deg,#142a42,#0f2236) !important;border:1px solid #1e3a5f !important;}
[data-theme="light"] .toast-title{color:#e6f1ff !important;}
[data-theme="light"] .toast-message{color:#7b98b8 !important;}
[data-theme="light"] .theme-btn.active{background:#00d4ff !important;color:#0d1b2a !important;}
[data-theme="light"] .status-badge{background:rgba(16,185,129,0.15) !important;border:1px solid rgba(16,185,129,0.3) !important;color:#10b981 !important;}
[data-theme="light"] .chart-box{background:linear-gradient(135deg,#142a42,#0f2236) !important;}
"""

if "</style>" in content:
    content = content.replace("</style>", navy_css + "\n</style>", 1)
    print("✅ Navy Blue qaybaha kale waa lagu daray!")

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
print("🔥 NAVY BLUE THEME waa dhammaatay!")
