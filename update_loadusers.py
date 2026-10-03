# update_loadusers.py - Cusboonaysii loadUsers si uu u muujiyo Edit button

with open("public/index.html", "r") as f:
    content = f.read()

start = content.find("async function loadUsers()")
end = content.find("async function loadLicenses()")

if start != -1 and end != -1:
    new_loadusers = '''async function loadUsers() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/admin/users', {
                headers: { 'Authorization': 'Bearer ' + token }
            });
            const users = await response.json();
            const tbody = document.getElementById('users-tbody');
            if (!tbody) return;
            if (!Array.isArray(users) || users.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" style="padding: 20px; text-align: center;">Ma jiro user</td></tr>';
                return;
            }
            tbody.innerHTML = users.map(function(u) {
                var roleColor = u.role === 'admin' ? '#8b5cf6' : '#2a2a35';
                return '<tr style="border-bottom: 1px solid #2a2a35;">' +
                    '<td style="padding: 12px;">' + u.id + '</td>' +
                    '<td style="padding: 12px;"><strong>' + u.username + '</strong></td>' +
                    '<td style="padding: 12px;">' + (u.fullname || '-') + '</td>' +
                    '<td style="padding: 12px;"><span style="padding: 4px 10px; border-radius: 20px; background: ' + roleColor + '; font-size: 12px;">' + u.role + '</span></td>' +
                    '<td style="padding: 12px;">' + (u.license_key || '-') + '</td>' +
                    '<td style="padding: 12px; white-space: nowrap;">' +
                        '<button onclick="editUserRole(' + u.id + ', \\'' + u.role + '\\')" style="background: #8b5cf6; border: none; color: white; padding: 6px 10px; border-radius: 6px; cursor: pointer; margin-right: 5px;">' +
                            '<i class="fa-solid fa-pen"></i>' +
                        '</button>' +
                        '<button onclick="deleteUser(' + u.id + ')" style="background: #ef4444; border: none; color: white; padding: 6px 10px; border-radius: 6px; cursor: pointer;">' +
                            '<i class="fa-solid fa-trash"></i>' +
                        '</button>' +
                    '</td>' +
                    '</tr>';
            }).join('');
        } catch (error) {
            console.error('Error loading users:', error);
        }
    }
    
    '''
    content = content[:start] + new_loadusers + content[end:]
    with open("public/index.html", "w") as f:
        f.write(content)
    print("✅ loadUsers waa la cusboonaysiiyay!")
else:
    print("❌ Ma helin loadUsers")
