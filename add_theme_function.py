# add_theme_function.py - Ku dar setTheme function iyo Soft Theme CSS

with open("public/index.html", "r") as f:
    content = f.read()

# ===== 1. KU DAR SETTHEME FUNCTION (ka hor function handleLogout) =====
settheme_js = """
    // ===== THEME SWITCHER =====
    function setTheme(theme) {
        var root = document.documentElement;
        var buttons = document.querySelectorAll('.theme-btn');
        buttons.forEach(function(btn) { btn.classList.remove('active'); });
        if (theme === 'light') {
            root.setAttribute('data-theme', 'light');
            if (buttons[1]) buttons[1].classList.add('active');
            localStorage.setItem('abdi_theme', 'light');
            if (typeof showToast === 'function') showToast('Theme', 'Light Mode (Cream/Soft) waa la shidey!', 'info');
        } else if (theme === 'dark') {
            root.removeAttribute('data-theme');
            if (buttons[0]) buttons[0].classList.add('active');
            localStorage.setItem('abdi_theme', 'dark');
            if (typeof showToast === 'function') showToast('Theme', 'Dark Mode waa la shidey!', 'info');
        } else {
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
                root.setAttribute('data-theme', 'light');
            } else {
                root.removeAttribute('data-theme');
            }
            if (buttons[2]) buttons[2].classList.add('active');
            localStorage.setItem('abdi_theme', 'auto');
            if (typeof showToast === 'function') showToast('Theme', 'Auto Mode waa la shidey!', 'info');
        }
    }
    
    // Soo celi theme-ka la keydiyay marka boggu furmo
    (function() {
        var saved = localStorage.getItem('abdi_theme');
        if (saved === 'light') {
            document.documentElement.setAttribute('data-theme', 'light');
        }
    })();
"""

if "function setTheme" not in content:
    if "function handleLogout()" in content:
        content = content.replace("function handleLogout()", settheme_js + "\n    function handleLogout()", 1)
        print("✅ setTheme function waa lagu daray!")
    else:
        print("⚠️ handleLogout lama helin")
else:
    print("ℹ️ setTheme horey ayuu u jiray!")

# ===== 2. BEDDEL CSS-KA LIGHT MODE =====
old_light_css = '''[data-theme="light"]{--bg:#eef2f7;--sidebar:#ffffff;--card:#f8fafc;--card-hover:#e8eef5;--text:#1a2332;--muted:#64748b;--primary:#0ea5e9;--purple:#7c3aed;--green:#059669;--yellow:#d97706;--red:#dc2626;--border:#d1dbe8;box-shadow:0 1px 3px rgba(0,0,0,.05);}'''

new_light_css = '''[data-theme="light"]{--bg:#faf6f0;--sidebar:#fffbf5;--card:#ffffff;--card-hover:#f5ede0;--text:#3d2e1f;--muted:#8b7355;--primary:#e07a5f;--purple:#c17c5a;--green:#7a9e7e;--yellow:#d4a373;--red:#c75c5c;--border:#f0e6d6;}'''

if old_light_css in content:
    content = content.replace(old_light_css, new_light_css)
    print("✅ Light Mode CSS waa la beddelay (Cream/Soft)!")

# ===== 3. BEDDEL QAYBAHA KALE EE LIGHT MODE =====
content = content.replace(
    '[data-theme="light"] body{background:linear-gradient(135deg,#eef2f7 0%,#e0e7ff 100%);}',
    '[data-theme="light"] body{background:linear-gradient(135deg,#faf6f0 0%,#f5ede0 50%,#faf6f0 100%) !important;}'
)
content = content.replace(
    '[data-theme="light"] .sidebar{background:#ffffff;border-right:1px solid var(--border);}',
    '[data-theme="light"] .sidebar{background:linear-gradient(180deg,#fffbf5,#f5ede0) !important;border-right:1px solid #f0e6d6;}'
)
content = content.replace(
    '[data-theme="light"] .card,[data-theme="light"] .stat-card,[data-theme="light"] .panel,[data-theme="light"] .hero{background:#ffffff;border:1px solid var(--border);}',
    '[data-theme="light"] .card,[data-theme="light"] .stat-card,[data-theme="light"] .panel,[data-theme="light"] .hero{background:linear-gradient(135deg,#ffffff,#fdf9f3) !important;border:1px solid #f0e6d6 !important;box-shadow:0 4px 20px rgba(224,122,95,0.08) !important;}'
)
content = content.replace(
    '[data-theme="light"] input,[data-theme="light"] select{background:#ffffff;border:1px solid var(--border);color:var(--text);}',
    '[data-theme="light"] input,[data-theme="light"] select{background:#fffbf5 !important;border:1px solid #f0e6d6 !important;color:#3d2e1f !important;}'
)
print("✅ Qaybaha kale ee Light Mode waa la beddelay!")

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
print("🔥 SOFT THEME + FUNCTION waa dhammaatay!")
