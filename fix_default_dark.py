import shutil

shutil.copy('public/index.html', 'public/index.html.backup')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Beddel localStorage keydinta — haddii 'light' uu keydsan yahay, tirtir
#    Si default-ku Dark noqdo
old_check = "if(localStorage.getItem('theme')==='light'){"
if old_check in c:
    c = c.replace(old_check, "if(false){", 1)
    print("1. Light check: OK (default Dark)")
else:
    print("1. Light check: LAMA HELIN")

# 2. Hubi — keydinta theme-ka oo dhan
#    Waxaan raadinayaa localStorage.setItem('theme', ...) 
import re
count = len(re.findall(r"localStorage\.setItem\('theme'", c))
print(f"2. localStorage.setItem('theme') meelaha: {count}")

# 3. Haddii uu keydiyo 'light' — u beddel 'dark'
old_save = "localStorage.setItem('theme','light')"
if old_save in c:
    c = c.replace(old_save, "localStorage.setItem('theme','dark')", 1)
    print("3. Save light→dark: OK")
else:
    print("3. Save light: LAMA HELIN")

old_save2 = 'localStorage.setItem("theme","light")'
if old_save2 in c:
    c = c.replace(old_save2, 'localStorage.setItem("theme","dark")', 1)
    print("4. Save light→dark (double quotes): OK")
else:
    print("4. Save light (double): LAMA HELIN")

# 4. Qor
with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup")
print("Hadda panel-ka fur — Dark ayaa default noqon doona")
