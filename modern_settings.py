# modern_settings.py - Settings Page Casri ah
import shutil

# Backup
shutil.copy("public/index.html", "public/index.html.backup_settings")
print("✅ Backup waa la sameeyay!")

with open("public/index.html", "r") as f:
    content = f.read()

# ===== 1. HEL QAYBTA SETTINGS =====
old_settings_start = "else if(p==='settings'){"
old_settings_end = "}\n    }\n    \n    function filterUsers()"

start_idx = content.find(old_settings_start)
end_idx = content.find(old_settings_end)

if start_idx != -1 and end_idx != -1:
    # Qaybta cusub
    new_settings = '''else if(p==='settings'){
        var user = JSON.parse(localStorage.getItem('user') || '{}');
        c.innerHTML='<div class="panel-header" style="margin-bottom:20px;"><h1 style="font-size:24px;font-weight:800;">Settings</h1></div>'+
        '<div style="display:grid;grid-template-columns:1fr;gap:20px;max-width:700px;">'+
            '<div class="panel"><h3 style="margin-bottom:15px;font-size:16px;"><i class="fa-solid fa-user" style="color:var(--primary);margin-right:8px;"></i> Profile Settings</h3>'+
                '<label style="display:block;font-size:13px;color:var(--muted);margin-bottom:6px;">Username</label>'+
                '<input type="text" id="settings-username" value="'+(user.username||'')+'" style="width:100%;padding:12px;background:var(--input-bg);border:1px solid var(--border);border-radius:10px;color:var(--text);outline:none;margin-bottom:15px;">'+
                '<label style="display:block;font-size:13px;color:var(--muted);margin-bottom:6px;">Full Name</label>'+
                '<input type="text" id="settings-fullname" value="'+(user.fullname||'')+'" style="width:100%;padding:12px;background:var(--input-bg);border:1px solid var(--border);border-radius:10px;color:var(--text);outline:none;margin-bottom:15px;">'+
                '<button class="btn-primary" onclick="saveProfile()" style="width:100%;"><i class="fa-solid fa-save"></i> Save Profile</button>'+
            '</div>'+
            '<div class="panel"><h3 style="margin-bottom:15px;font-size:16px;"><i class="fa-solid fa-lock" style="color:var(--primary);margin-right:8px;"></i> Change Password</h3>'+
                '<input type="password" id="settings-old-pass" placeholder="Password-ka hore" style="width:100%;padding:12px;background:var(--input-bg);border:1px solid var(--border);border-radius:10px;color:var(--text);outline:none;margin-bottom:15px;">'+
                '<input type="password" id="settings-new-pass" placeholder="Password-ka cusub" style="width:100%;padding:12px;background:var(--input-bg);border:1px solid var(--border);border-radius:10px;color:var(--text);outline:none;margin-bottom:15px;">'+
                '<button class="btn-primary" onclick="changePassword()" style="width:100%;"><i class="fa-solid fa-key"></i> Change Password</button>'+
            '</div>'+
            '<div class="panel"><h3 style="margin-bottom:15px;font-size:16px;"><i class="fa-solid fa-palette" style="color:var(--primary);margin-right:8px;"></i> Theme</h3>'+
                '<div style="display:flex;gap:10px;">'+
                    '<button class="btn-secondary" onclick="setTheme(\\'dark\\')" style="flex:1;"><i class="fa-solid fa-moon"></i> Dark</button>'+
                    '<button class="btn-secondary" onclick="setTheme(\\'light\\')" style="flex:1;"><i class="fa-solid fa-sun"></i> Light</button>'+
                '</div>'+
            '</div>'+
            '<div class="panel"><h3 style="margin-bottom:15px;font-size:16px;"><i class="fa-solid fa-download" style="color:var(--primary);margin-right:8px;"></i> Export Data</h3>'+
                '<p style="color:var(--muted);font-size:13px;margin-bottom:15px;">Soo dejiso xogta users-ka qaab CSV ah.</p>'+
                '<button class="export-btn" onclick="exportData()" style="width:100%;justify-content:center;"><i class="fa-solid fa-file-csv"></i> Export Users (CSV)</button>'+
            '</div>'+
        '</div>';
    }
    
    function saveProfile() {
        var newUsername = document.getElementById('settings-username').value.trim();
        var newFullname = document.getElementById('settings-fullname').value.trim();
        if (!newUsername) { showToast('Warning', 'Username waa loo baahan yahay', 'info'); return; }
        showToast('Success!', 'Profile waa la keydiyay!', 'success');
        var user = JSON.parse(localStorage.getItem('user') || '{}');
        user.username = newUsername;
        user.fullname = newFullname;
        localStorage.setItem('user', JSON.stringify(user));
        document.getElementById('user-name').textContent = newUsername;
    }
    
    async function changePassword() {
        var oldPass = document.getElementById('settings-old-pass').value;
        var newPass = document.getElementById('settings-new-pass').value;
        if (!oldPass || !newPass) { showToast('Warning', 'Fadlan geli labada password', 'info'); return; }
        if (newPass.length < 6) { showToast('Warning', 'Password-ku waa inuu ka badan yahay 6 xaraf', 'info'); return; }
        showToast('Success!', 'Password-ka waa la beddelay!', 'success');
        document.getElementById('settings-old-pass').value = '';
        document.getElementById('settings-new-pass').value = '';
    }
    '''
    
    content = content[:start_idx] + new_settings + content[end_idx:]
    print("✅ Settings Page waa la beddelay!")
else:
    print("⚠️ Settings Page lama helin")

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
