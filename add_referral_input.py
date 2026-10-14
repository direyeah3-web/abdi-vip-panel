# add_referral_input.py - Ku dar Referral Code Input form-ka

with open("public/index.html", "r") as f:
    content = f.read()

# ===== 1. KU DAR REFERRAL INPUT (ka hor Register button) =====
old_marker = '''<div class="form-group"><label>Full Name</label><div class="input-wrapper"><i class="fa-regular fa-id-card prefix"></i><input type="text" id="reg-fullname" placeholder="Enter full name"></div></div>'''

new_marker = '''<div class="form-group"><label>Full Name</label><div class="input-wrapper"><i class="fa-regular fa-id-card prefix"></i><input type="text" id="reg-fullname" placeholder="Enter full name"></div></div>
            <div class="form-group"><label>Referral Code <span style="color:var(--red);">*</span></label><div class="input-wrapper"><i class="fa-solid fa-key prefix"></i><input type="text" id="reg-referral" placeholder="Enter referral code" required></div></div>'''

if old_marker in content:
    content = content.replace(old_marker, new_marker)
    print("✅ Referral Input waa lagu daray form-ka!")
else:
    print("⚠️ Full Name input lama helin — isku day qaab kale")

# ===== 2. CUSBOONAYSI HANDLEREGISTER =====
old_register = "async function handleRegister(e){e.preventDefault();var u=document.getElementById('reg-username').value;var p=document.getElementById('reg-password').value;var f=document.getElementById('reg-fullname').value;var ref=prompt('Geli Referral Code-ka (waa loo baahan yahay ammaanka):');if(!ref||ref.trim()===''){showToast('Warning','Referral code waa loo baahan yahay!','info');return;}ref=ref.trim().toUpperCase();"

new_register = "async function handleRegister(e){e.preventDefault();var u=document.getElementById('reg-username').value;var p=document.getElementById('reg-password').value;var f=document.getElementById('reg-fullname').value;var ref=document.getElementById('reg-referral').value.trim().toUpperCase();if(!ref){showToast('Warning','Referral code waa loo baahan yahay!','info');return;}"

if old_register in content:
    content = content.replace(old_register, new_register)
    print("✅ handleRegister waa la cusboonaysiiyay!")
else:
    print("⚠️ handleRegister lama helin — isku day qaab kale")

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
