# add_edit_function.py - Ku dar editUserRole iyo botton Edit

with open("public/index.html", "r") as f:
    content = f.read()

# 1. Ku dar editUserRole function ka hor handleLogout
edit_func = """
    // ===== EDIT USER ROLE =====
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
"""

if "function editUserRole" not in content:
    content = content.replace("function handleLogout()", edit_func + "\n    function handleLogout()")
    print("✅ editUserRole function waa lagu daray!")
else:
    print("⚠️ editUserRole horey ayuu u jiray!")

# 2. Ku dar botton Edit miiska users
old_td = """'<td style="padding: 12px;">' +
                    '<button onclick="deleteUser(' + u.id + ')" style="background: #ef4444; border: none; color: white; padding: 6px 10px; border-radius: 6px; cursor: pointer;">' +
                        '<i class="fa-solid fa-trash"></i>' +
                    '</button>' +
                '</td>'"""

new_td = """'<td style="padding: 12px; white-space: nowrap;">' +
                    '<button onclick="editUserRole(' + u.id + ', \\'' + u.role + '\\')" style="background: #8b5cf6; border: none; color: white; padding: 6px 10px; border-radius: 6px; cursor: pointer; margin-right: 5px;">' +
                        '<i class="fa-solid fa-pen"></i>' +
                    '</button>' +
                    '<button onclick="deleteUser(' + u.id + ')" style="background: #ef4444; border: none; color: white; padding: 6px 10px; border-radius: 6px; cursor: pointer;">' +
                        '<i class="fa-solid fa-trash"></i>' +
                    '</button>' +
                '</td>'"""

if old_td in content:
    content = content.replace(old_td, new_td)
    print("✅ Botton Edit miiska waa lagu daray!")
else:
    print("⚠️ Botton Edit lama helin (waa in aan gacanta ku beddelnaa)")

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
