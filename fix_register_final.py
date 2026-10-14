# fix_register_final.py - Hagaaji f is not defined

with open("public/index.html", "r") as f:
    content = f.read()

# Calaamadda saxda ah
old_code = "async function handleRegister(e){e.preventDefault();var u=document.getElementById('reg-username').value;var p=document.getElementById('reg-password').value;var ref=document.getElementById('reg-referral').value.trim().toUpperCase();if(!ref){showToast('Warning', 'Referral code waa loo baahan yahay!', 'info');return;}try{var r=await fetch('/api/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p,full_name:f,referral_code:ref})});var d=await r.json();if(d.success||d.token){showToast('Success!', 'Account created! Please login.', 'success');switchTab('login');}else{showToast('Error', d.error||'Registration failed', 'error');}}catch(x){showToast('Error', x.message, 'error');}}"

new_code = "async function handleRegister(e){e.preventDefault();var u=document.getElementById('reg-username').value;var p=document.getElementById('reg-password').value;var ref=document.getElementById('reg-referral').value.trim().toUpperCase();if(!ref){showToast('Warning', 'Referral code waa loo baahan yahay!', 'info');return;}try{var r=await fetch('/api/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p,referral_code:ref})});var d=await r.json();if(d.success||d.token){showToast('Success!', 'Account created! Please login.', 'success');switchTab('login');}else{showToast('Error', d.error||'Registration failed', 'error');}}catch(x){showToast('Error', x.message, 'error');}}"

if old_code in content:
    content = content.replace(old_code, new_code)
    with open("public/index.html", "w") as f:
        f.write(content)
    print("✅ handleRegister waa la hagaajiyay (full_name: f waa la tirtiray)!")
else:
    print("⚠️ Code-ka lama helin — isku day qaab kale")
