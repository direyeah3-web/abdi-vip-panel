# replace_all_alerts.py - Beddel dhammaan alert() oo hadhay

with open("public/index.html", "r") as f:
    content = f.read()

# Liiska beddellada
replacements = [
    # 1. handleRegister
    ("alert('Account created! Please login.');", "showToast('Success!', 'Account created! Please login.', 'success');"),
    ("alert('Registration failed: '+(d.error||'Unknown'));", "showToast('Error', d.error||'Registration failed', 'error');"),
    ("alert('Error: '+x.message);", "showToast('Error', x.message, 'error');"),
    
    # 2. addUser
    ("alert('Username and password required');", "showToast('Warning', 'Username and password required', 'info');"),
    ("alert('User created!');", "showToast('Success!', 'User cusub waa la abuuray!', 'success');"),
    ("alert('Error: '+(d.error||'Unknown'));", "showToast('Error', d.error||'Unknown error', 'error');"),
    ("alert('Error: '+e.message);", "showToast('Error', e.message, 'error');"),
    
    # 3. copyLicense
    ("alert('Copied: '+k);", "showToast('Copied!', 'License key: '+k, 'success');"),
    
    # 4. generateLicenses
    ("alert('Enter valid days');", "showToast('Warning', 'Fadlan geli tirada maalmood ee saxda ah', 'info');"),
    ("alert('Error: '+(data.error||'Unknown'));", "showToast('Error', data.error||'Unknown error', 'error');"),
    
    # 5. Notifications
    ("alert('Notifications:\\\\n\\\\n1. New user registered (2 min ago)\\\\n2. License generated (15 min ago)\\\\n3. System updated (3 hours ago)');", "showToast('Notifications', '1. New user registered (2 min ago) | 2. License generated (15 min ago) | 3. System updated (3 hours ago)', 'info');"),
    
    # 6. Worker URL
    ("alert('Enter Worker URL');", "showToast('Warning', 'Fadlan geli Worker URL', 'info');"),
    
    # 7. Role
    ("alert('Role-ku waa inuu noqdaa \"user\" ama \"admin\"');", "showToast('Warning', 'Role-ku waa inuu noqdaa user ama admin', 'info');"),
    
    # 8. Export
    ("alert('Error exporting: ' + e.message);", "showToast('Error', 'Export failed: ' + e.message, 'error');"),
    
    # 9. Quantity
    ("alert(qty + ' license(s) waa la abuuray!');", "showToast('Success!', qty + ' license(s) waa la abuuray!', 'success');"),
]

count = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        count += 1
        print("✅ La beddelay: " + old[:40] + "...")

# Beddel alert() kasta oo hadhay (fallback)
import re
remaining = re.findall(r"alert\([^)]+\)", content)
if remaining:
    print("⚠️ " + str(len(remaining)) + " alert() wali hadhay:")
    for r in remaining[:5]:
        print("   - " + r)

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ " + str(count) + " alert() waa la beddelay!")
print("🔥 Dhammaystiran!")
