# fix_default_dark.py - Dark Mode default ka dhig

with open("public/index.html", "r") as f:
    content = f.read()

# ===== 1. KA SAAR AUTO-LOAD LIGHT THEME =====
old_auto = """// Soo celi theme-ka la keydiyay marka boggu furmo
    (function() {
        var saved = localStorage.getItem('abdi_theme');
        if (saved === 'light') {
            document.documentElement.setAttribute('data-theme', 'light');
        }
    })();"""

new_auto = """// Soo celi theme-ka la keydiyay marka boggu furmo (default: Dark)
    (function() {
        var saved = localStorage.getItem('abdi_theme');
        if (saved === 'light') {
            document.documentElement.setAttribute('data-theme', 'light');
        } else {
            document.documentElement.removeAttribute('data-theme');
        }
    })();"""

if old_auto in content:
    content = content.replace(old_auto, new_auto)
    print("✅ Auto-load theme waa la hagaajiyay (default: Dark)!")
else:
    print("⚠️ Auto-load lama helin — isku day qaab kale")

# ===== 2. HUBI IN DARK THEME UU DEFAULT YAHOO =====
# HTML-ka `<html>` waa inaan lahayn `data-theme="light"` si default uu u noqdo Dark
if '<html lang="en" data-theme="light">' in content:
    content = content.replace('<html lang="en" data-theme="light">', '<html lang="en">')
    print("✅ HTML tag-ka waa la hagaajiyay (default: Dark)!")
else:
    print("ℹ️ HTML tag-ku wuu saxan yahay (ma lahayn data-theme)")

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
