# add_edit_user.py - Ku dar editUserRole function

with open("public/index.html", "r") as f:
    content = f.read()

if "function editUserRole(" in content:
    print("⚠️ editUserRole horey ayuu u jiray!")
else:
    edit_func = '''
    async function editUserRole(id, currentRole) {
        var newRole = prompt('Geli role-ka cusub (user ama admin):', currentRole);
        if (!newRole) return;
        if (newRole !== 'user' && newRole !== 'admin') {
            alert('Role-ku waa inuu noqdaa "user" ama "admin"');
            return;
        }
        try {
            var token = localStorage.getItem('token');
            var res = await fetch('/api/admin/users/' + id, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                },
                body: JSON.stringify({ role: newRole })
            });
            if (res.ok) {
                alert('Role-ka waa la beddelay!');
                loadUsers();
            } else {
                alert('Error changing role');
            }
        } catch (e) {
            alert('Error: ' + e.message);
        }
    }
    
'''
    target = "function handleLogout()"
    pos = content.find(target)
    if pos != -1:
        content = content[:pos] + edit_func + content[pos:]
        with open("public/index.html", "w") as f:
            f.write(content)
        print("✅ editUserRole waa lagu daray!")
    else:
        print("❌ Ma helin handleLogout")
