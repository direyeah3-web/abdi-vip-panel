import shutil

shutil.copy('public/index.html', 'public/index.html.backup')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Beddel function-ka soo celinta theme-ka — 'light' kaliya ha soo celin
old_restore = '''(function() {
    var saved = localStorage.getItem("abdi_theme");
    if (saved === 'light') {
        document.documentElement.setAttribute("data-theme", "light");
    }
})();'''

new_restore = '''(function() {
    var saved = localStorage.getItem("abdi_theme");
    // Default: Dark (haddii 'light' si gaar ah loo keydiyay, waa la soo celinayaa)
    // Haddii 'dark' ama wax kale, Dark ayaa default ah (data-theme lama dhigo)
    if (saved === 'light') {
        document.documentElement.setAttribute("data-theme", "light");
    } else {
        document.documentElement.removeAttribute("data-theme");
    }
})();'''

if old_restore in c:
    c = c.replace(old_restore, new_restore, 1)
    print("1. Theme restore: OK")
else:
    print("1. Theme restore: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup")
