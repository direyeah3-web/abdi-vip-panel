import shutil

shutil.copy('public/index.html', 'public/index.html.backup')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Beddel referral_code:ref → referral_code:'ABD2026'
old_code = "body:JSON.stringify({username:u,password:p,referral_code:ref})"
new_code = "body:JSON.stringify({username:u,password:p,fullname:f,referral_code:'ABD2026'})"
if old_code in c:
    c = c.replace(old_code, new_code, 1)
    print("1. addUser referral_code: OK")
else:
    print("1. addUser referral_code: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup")
