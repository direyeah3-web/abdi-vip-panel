import shutil

# 1. Backup
shutil.copy('public/index.html', 'public/index.html.backup')

# 2. Akhri
with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 3. Line 565 — Saar register Full Name input
old_input = '<div class="form-group"><label>Full Name</label><div class="input-wrapper"><i class="fa-regular fa-id-card prefix"></i><input type="text" id="reg-fullname" placeholder="Enter full name"></div></div>'
if old_input in c:
    c = c.replace(old_input, '', 1)
    print("1. Form input: OK")
else:
    print("1. Form input: LAMA HELIN")

# 4. Line 641 — Saar variable-ka
old_var = "var f=document.getElementById('reg-fullname').value;"
if old_var in c:
    c = c.replace(old_var, '', 1)
    print("2. Variable: OK")
else:
    print("2. Variable: LAMA HELIN")

# 5. Line 641 — Saar body-ka
old_body = "fullname:f,"
if old_body in c:
    c = c.replace(old_body, '', 1)
    print("3. Body: OK")
else:
    print("3. Body: LAMA HELIN")

# 6. Qor
with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup")
