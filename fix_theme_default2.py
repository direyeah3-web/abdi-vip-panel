import shutil
import re

shutil.copy('public/index.html', 'public/index.html.safe9')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Raadi function-ka theme restore (IIFE)
old_pattern = r"\(function\(\)\s*\{\s*var saved\s*=\s*localStorage\.getItem\('theme'\);\s*if\s*\(saved\s*===\s*'light'\)\s*\{\s*document\.documentElement\.setAttribute\('data-theme',\s*'light'\);\s*setTimeout\(function\(\)\s*\{[^}]*\},\s*100\);\s*\}\s*\}\)\(\);"

new_code = """(function() {
            // Soo celi theme-ka la keydiyay — DEFAULT: Dark
            var saved = localStorage.getItem('abdi_theme') || localStorage.getItem('theme');
            if (saved === 'light') {
                document.documentElement.setAttribute('data-theme', 'light');
                setTimeout(function() {
                    var icon = document.getElementById('theme-icon');
                    if (icon) { icon.classList.remove('fa-sun'); icon.classList.add('fa-moon'); }
                }, 100);
            } else {
                // Default: Dark
                document.documentElement.removeAttribute('data-theme');
                setTimeout(function() {
                    var icon = document.getElementById('theme-icon');
                    if (icon) { icon.classList.remove('fa-moon'); icon.classList.add('fa-sun'); }
                }, 100);
            }
        })();"""

match = re.search(old_pattern, c, re.DOTALL)
if match:
    c = c[:match.start()] + new_code + c[match.end():]
    print("1. Theme restore: OK")
else:
    print("1. Theme restore: LAMA HELIN")

# Beddel keydka 'theme' → 'abdi_theme' toggleTheme function-ka
c = c.replace("localStorage.setItem('theme', 'dark');", "localStorage.setItem('abdi_theme', 'dark');")
c = c.replace("localStorage.setItem('theme', 'light');", "localStorage.setItem('abdi_theme', 'light');")
print("2. toggleTheme keyd: OK")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.safe9")
