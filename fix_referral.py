import shutil

shutil.copy('public/index.html', 'public/index.html.safe12')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Beddel referral_code:'ABD2026' → referral_code:ref
old_code = "body:JSON.stringify({username:u,password:p,referral_code:'ABD2026'})"
new_code = "body:JSON.stringify({username:u,password:p,referral_code:ref})"

if old_code in c:
    c = c.replace(old_code, new_code, 1)
    print("1. Referral code: OK")
else:
    print("1. Referral code: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.safe12")
