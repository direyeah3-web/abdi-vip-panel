import shutil

shutil.copy('public/index.html', 'public/index.html.safe11')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Beddel function-ka theme restore — ku dar else
old_code = """(function() {
            var saved = localStorage.getItem('abdi_theme');
            if (saved === 'light') {
                document.documentElement.setAttribute('data-theme', 'light');
            }
        })();"""

new_code = """(function() {
            var saved = localStorage.getItem('abdi_theme');
            if (saved === 'light') {
                document.documentElement.setAttribute('data-theme', 'light');
            } else {
                document.documentElement.removeAttribute('data-theme');
            }
        })();"""

if old_code in c:
    c = c.replace(old_code, new_code, 1)
    print("1. Theme restore + else: OK")
else:
    print("1. Theme restore: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.safe11")
