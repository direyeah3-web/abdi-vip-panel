import shutil

shutil.copy('public/index.html', 'public/index.html.safe13')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Beddel handleRegister — referral_code:'ABD2026' → referral_code:ref
old_code = "referral_code:'ABD2026'"
count = c.count(old_code)

if count > 0:
    c = c.replace(old_code, "referral_code:ref")
    print(f"1. handleRegister: OK ({count} meelood)")
else:
    print("1. handleRegister: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.safe13")
