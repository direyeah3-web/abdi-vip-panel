# soft_theme.py - Light Mode Midab Casri ah (Cream/Soft Warm)
import shutil

# Backup
shutil.copy("public/index.html", "public/index.html.backup_theme")
print("✅ Backup waa la sameeyay!")

with open("public/index.html", "r") as f:
    content = f.read()

# ===== 1. BEDDEL CSS-KA LIGHT MODE =====
old_light = '''[data-theme="light"]{--bg:#eef2f7;--sidebar:#ffffff;--card:#f8fafc;--card-hover:#e8eef5;--text:#1a2332;--muted:#64748b;--primary:#0ea5e9;--purple:#7c3aed;--green:#059669;--yellow:#d97706;--red:#dc2626;--border:#d1dbe8;}'''

new_light = '''[data-theme="light"]{
    --bg:#faf6f0;
    --sidebar:#fffbf5;
    --card:#ffffff;
    --card-hover:#f5ede0;
    --text:#3d2e1f;
    --muted:#8b7355;
    --primary:#e07a5f;
    --purple:#c17c5a;
    --green:#7a9e7e;
    --yellow:#d4a373;
    --red:#c75c5c;
    --border:#f0e6d6;
}
[data-theme="light"] body{
    background:linear-gradient(135deg,#faf6f0 0%,#f5ede0 50%,#faf6f0 100%) !important;
    transition:background 0.5s ease;
}
[data-theme="light"] .sidebar{
    background:linear-gradient(180deg,#fffbf5,#f5ede0) !important;
    border-right:1px solid #f0e6d6;
}
[data-theme="light"] .card,
[data-theme="light"] .stat-card,
[data-theme="light"] .panel,
[data-theme="light"] .hero{
    background:linear-gradient(135deg,#ffffff,#fdf9f3) !important;
    border:1px solid #f0e6d6 !important;
    box-shadow:0 4px 20px rgba(224,122,95,0.08) !important;
}
[data-theme="light"] .hero{
    background:linear-gradient(135deg,#fff5e6,#ffe8d6) !important;
}
[data-theme="light"] input,
[data-theme="light"] select{
    background:#fffbf5 !important;
    border:1px solid #f0e6d6 !important;
    color:#3d2e1f !important;
}
[data-theme="light"] input:focus{
    border-color:#e07a5f !important;
    box-shadow:0 0 0 3px rgba(224,122,95,0.15) !important;
}
[data-theme="light"] .quick-action{
    background:#f5ede0 !important;
    border:1px solid transparent;
}
[data-theme="light"] .quick-action:hover{
    background:#ffe8d6 !important;
    border-color:#e07a5f !important;
}
[data-theme="light"] .nav-item:hover,
[data-theme="light"] .nav-item.active{
    background:linear-gradient(135deg,rgba(224,122,95,0.15),rgba(193,124,90,0.15)) !important;
    color:#e07a5f !important;
}
[data-theme="light"] .topnav{
    background:rgba(255,251,245,0.9) !important;
    border-bottom:1px solid #f0e6d6 !important;
    backdrop-filter:blur(20px);
}
[data-theme="light"] .btn-primary{
    background:linear-gradient(135deg,#e07a5f,#c17c5a) !important;
    color:white !important;
}
[data-theme="light"] .submit-btn{
    background:linear-gradient(135deg,#e07a5f,#c17c5a) !important;
    color:white !important;
}
[data-theme="light"] .stat-value{
    background:linear-gradient(135deg,#e07a5f,#c17c5a) !important;
    -webkit-background-clip:text !important;
    -webkit-text-fill-color:transparent !important;
    background-clip:text !important;
}
[data-theme="light"] .live-clock{
    background:#f5ede0 !important;
    border:1px solid #f0e6d6 !important;
    color:#e07a5f !important;
}
[data-theme="light"] .online-badge{
    background:rgba(122,158,126,0.15) !important;
    border:1px solid rgba(122,158,126,0.3) !important;
    color:#7a9e7e !important;
}
[data-theme="light"] .icon-btn{
    background:#f5ede0 !important;
    border:1px solid #f0e6d6 !important;
    color:#3d2e1f !important;
}
[data-theme="light"] .toast{
    background:linear-gradient(135deg,#ffffff,#fdf9f3) !important;
    border:1px solid #f0e6d6 !important;
}
[data-theme="light"] .toast-title{color:#3d2e1f !important;}
[data-theme="light"] .toast-message{color:#8b7355 !important;}
[data-theme="light"] .theme-btn.active{
    background:#e07a5f !important;
    color:white !important;
}'''

if old_light in content:
    content = content.replace(old_light, new_light)
    print("✅ Light Mode CSS waa la beddelay (Cream/Soft Warm)!")
else:
    print("⚠️ CSS-ka hore lama helin — isku day qaab kale")

# ===== 2. KU DAR ANIMATION THEME =====
theme_anim_css = """
@keyframes themeTransition { from{opacity:0.5;transform:scale(0.98)} to{opacity:1;transform:scale(1)} }
[data-theme="light"] .main,
[data-theme="light"] .sidebar,
[data-theme="light"] .card,
[data-theme="light"] .panel {
    animation:themeTransition 0.4s ease-out;
}
.theme-btn { transition:all 0.3s cubic-bezier(0.34,1.56,0.64,1); }
.theme-btn:hover { transform:scale(1.15) rotate(15deg); }
"""

if "</style>" in content:
    content = content.replace("</style>", theme_anim_css + "\n</style>", 1)
    print("✅ Theme animation waa lagu daray!")

# ===== 3. HAGAaji setTheme FUNCTION =====
old_settheme = """function setTheme(theme) {
        var root = document.documentElement;
        var buttons = document.querySelectorAll('.theme-btn');
        buttons.forEach(function(btn) { btn.classList.remove('active'); });
        if (theme === 'light') {
            root.setAttribute('data-theme', 'light');
            if (buttons[1]) buttons[1].classList.add('active');
        } else if (theme === 'dark') {
            root.removeAttribute('data-theme');
            if (buttons[0]) buttons[0].classList.add('active');
        } else {
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
                root.setAttribute('data-theme', 'light');
            } else {
                root.removeAttribute('data-theme');
            }
            if (buttons[2]) buttons[2].classList.add('active');
        }
    }"""

new_settheme = """function setTheme(theme) {
        var root = document.documentElement;
        var buttons = document.querySelectorAll('.theme-btn');
        buttons.forEach(function(btn) { btn.classList.remove('active'); });
        if (theme === 'light') {
            root.setAttribute('data-theme', 'light');
            if (buttons[1]) buttons[1].classList.add('active');
            localStorage.setItem('abdi_theme', 'light');
            showToast('Theme', 'Light Mode (Cream/Soft) waa la shidey!', 'info');
        } else if (theme === 'dark') {
            root.removeAttribute('data-theme');
            if (buttons[0]) buttons[0].classList.add('active');
            localStorage.setItem('abdi_theme', 'dark');
            showToast('Theme', 'Dark Mode waa la shidey!', 'info');
        } else {
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
                root.setAttribute('data-theme', 'light');
            } else {
                root.removeAttribute('data-theme');
            }
            if (buttons[2]) buttons[2].classList.add('active');
            localStorage.setItem('abdi_theme', 'auto');
            showToast('Theme', 'Auto Mode waa la shidey!', 'info');
        }
    }"""

if old_settheme in content:
    content = content.replace(old_settheme, new_settheme)
    print("✅ setTheme waa la hagaajiyay!")
else:
    print("⚠️ setTheme lama helin — isku day qaab kale")

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
print("🔥 SOFT THEME waa dhammaatay!")
