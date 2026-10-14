import shutil

shutil.copy('public/index.html', 'public/index.html.backup')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Modal-ka — Full Name ka saar, Referral Code ku dar, Password eye icon
old_modal = '''<label>Username</label><input type="text" id="new-username" placeholder="Enter username">
<label>Password</label><input type="password" id="new-password" placeholder="Enter password">
<label>Full Name</label><input type="text" id="new-fullname" placeholder="Enter full name">
<button class="submit-btn" onclick="addUser()"><i class="fa-solid fa-plus"></i> Add User</button>'''

new_modal = '''<label>Username</label><input type="text" id="new-username" placeholder="Enter username">
<label>Password</label>
<div style="position:relative;">
<input type="password" id="new-password" placeholder="Enter password" style="padding-right:45px;">
<i class="fa-solid fa-eye" onclick="togglePassword('new-password', this)" style="position:absolute;right:15px;top:50%;transform:translateY(-50%);cursor:pointer;color:var(--muted);"></i>
</div>
<label>Referral Code</label><input type="text" id="new-referral" placeholder="Enter referral code (tusaale: ABD2026)">
<button class="submit-btn" onclick="addUser()"><i class="fa-solid fa-plus"></i> Add User</button>'''

if old_modal in c:
    c = c.replace(old_modal, new_modal, 1)
    print("1. Modal: OK")
else:
    print("1. Modal: LAMA HELIN")

# 2. addUser() function-ka — fullname ka saar, referral_code laga soo qaato input-ka
old_func = "async function addUser(){var u=document.getElementById('new-username').value.trim();var p=document.getElementById('new-password').value.trim();var f=document.getElementById('new-fullname').value.trim();if(!u||!p){showToast('Warning', 'Username and password required', 'info');return;}try{var r=await fetch('/api/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p,referral_code:ref})});var d=await r.json();if(d.success||d.token){closeAddUserModal();showToast('Success!', 'User cusub waa la abuuray!', 'success');loadUsers();}else{showToast('Error', d.error||'Unknown error', 'error');}}catch(e){showToast('Error', e.message, 'error');}}"

new_func = "async function addUser(){var u=document.getElementById('new-username').value.trim();var p=document.getElementById('new-password').value.trim();var ref=document.getElementById('new-referral').value.trim().toUpperCase();if(!u||!p){showToast('Warning', 'Username and password required', 'info');return;}if(!ref){showToast('Warning', 'Referral code waa loo baahan yahay', 'info');return;}try{var r=await fetch('/api/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p,referral_code:ref})});var d=await r.json();if(d.success||d.token){closeAddUserModal();showToast('Success!', 'User cusub waa la abuuray!', 'success');loadUsers();}else{showToast('Error', d.error||'Unknown error', 'error');}}catch(e){showToast('Error', e.message, 'error');}}"

if old_func in c:
    c = c.replace(old_func, new_func, 1)
    print("2. addUser: OK")
else:
    print("2. addUser: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup")
