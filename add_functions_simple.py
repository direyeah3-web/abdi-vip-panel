# add_functions_simple.py - Ku dar functions-ka dhabta ah (qaab fudud)

with open("public/index.html", "r") as f:
    content = f.read()

# Hubi haddii functions-ka horey u jiraan
if "async function loadUsers()" in content:
    print("⚠️ Functions-ka horey ayay u jiraan!")
else:
    # Qoraalka JavaScript-ka (indentation waa mid caadi ah)
    js_code = """
    // ===== LOAD USERS (REAL DATA) =====
    async function loadUsers() {
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
                return '<tr style="border-bottom: 1px solid #2a2a35;">' +
                    '<td style="padding: 12px;">' + u.id + '</td>' +
                    '<td style="padding: 12px;"><strong>' + u.username + '</strong></td>' +
                    '<td style="padding: 12px;">' + (u.fullname || '-') + '</td>' +
                    '<td style="padding: 12px;"><span style="padding: 4px 10px; border-radius: 20px; background: ' + (u.role === 'admin' ? '#8b5cf6' : '#2a2a35') + '; font-size: 12px;">' + u.role + '</span></td>' +
                    '<td style="padding: 12px;">' + (u.license_key || '-') + '</td>' +
                    '<td style="padding: 12px;"><button onclick="deleteUser(' + u.id + ')" style="background: #ef4444; border: none; color: white; padding: 6px 12px; border-radius: 6px; cursor: pointer;"><i class="fa-solid fa-trash"></i></button></td>' +
                    '</tr>';
            }).join('');
        } catch (error) {
            console.error('Error loading users:', error);
        }
    }
    
    function filterUsers() {
        const input = document.getElementById('user-search');
        if (!input) return;
        const val = input.value.toLowerCase();
        const rows = document.querySelectorAll('#users-tbody tr');
        rows.forEach(function(row) {
            row.style.display = row.textContent.toLowerCase().includes(val) ? '' : 'none';
        });
    }
    
    async function deleteUser(id) {
        if (!confirm('Ma hubtaa inaad tirtirto user-kan?')) return;
        try {
            const token = localStorage.getItem('token');
            const res = await fetch('/api/admin/users/' + id, {
                method: 'DELETE',
                headers: { 'Authorization': 'Bearer ' + token }
            });
            if (res.ok) loadUsers();
            else alert('Error deleting user');
        } catch (error) {
            alert('Error: ' + error.message);
        }
    }
    
    // ===== LOAD LICENSES (REAL DATA) =====
    async function loadLicenses() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/licenses', {
                headers: { 'Authorization': 'Bearer ' + token }
            });
            const licenses = await response.json();
            const tbody = document.getElementById('licenses-tbody');
            if (!tbody) return;
            if (!Array.isArray(licenses) || licenses.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" style="padding: 20px; text-align: center;">Ma jiro license</td></tr>';
                return;
            }
            tbody.innerHTML = licenses.map(function(l) {
                return '<tr style="border-bottom: 1px solid #2a2a35;">' +
                    '<td style="padding: 12px;"><code style="background: #1e1e28; padding: 4px 8px; border-radius: 4px;">' + l.license_key + '</code></td>' +
                    '<td style="padding: 12px;">' + (l.user_id || '-') + '</td>' +
                    '<td style="padding: 12px;">' + (l.duration || '-') + '</td>' +
                    '<td style="padding: 12px;"><span style="padding: 4px 10px; border-radius: 20px; background: ' + (l.status === 'unused' ? '#10b981' : '#f59e0b') + '; font-size: 12px;">' + l.status + '</span></td>' +
                    '<td style="padding: 12px;"><button onclick="deleteLicense(' + l.id + ')" style="background: #ef4444; border: none; color: white; padding: 6px 12px; border-radius: 6px; cursor: pointer;"><i class="fa-solid fa-trash"></i></button></td>' +
                    '</tr>';
            }).join('');
        } catch (error) {
            console.error('Error loading licenses:', error);
        }
    }
    
    async function deleteLicense(id) {
        if (!confirm('Ma hubtaa inaad tirtirto license-kan?')) return;
        try {
            const token = localStorage.getItem('token');
            const res = await fetch('/api/admin/licenses/' + id, {
                method: 'DELETE',
                headers: { 'Authorization': 'Bearer ' + token }
            });
            if (res.ok) loadLicenses();
            else alert('Error deleting license');
        } catch (error) {
            alert('Error: ' + error.message);
        }
    }
    
    function showGenerateLicenseModal() {
        const duration = prompt('Geli duration-ka license-ka:', '30 days');
        if (!duration) return;
        fetch('/api/licenses/generate', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body: JSON.stringify({ duration: duration })
        }).then(function(res) { return res.json(); })
        .then(function(data) {
            if (data.success) {
                alert('License cusub waa la abuuray: ' + data.license_key);
                loadLicenses();
            } else {
                alert('Error: ' + (data.error || 'Unknown'));
            }
        }).catch(function(e) { alert('Error: ' + e.message); });
    }
    
    function showAddUserModal() {
        alert('Add User feature wali lama dhisin.');
    }
    
    function toggleProfileMenu() {
        const menu = document.getElementById('profile-menu');
        if (menu) menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
    }
    """
    
    # Ku dar ka hor "function handleLogout()"
    target = "function handleLogout()"
    pos = content.find(target)
    
    if pos != -1:
        new_content = content[:pos] + js_code + "\n    " + content[pos:]
        with open("public/index.html", "w") as f:
            f.write(new_content)
        print("✅ Functions-ka waa lagu daray si guul leh!")
    else:
        print("❌ Ma helin handleLogout")
