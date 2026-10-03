# final_all_features.py - Dhiso dhammaan qaybaha hadhay hal mar

with open("public/index.html", "r") as f:
    content = f.read()

# ===== 1. HAGAaji MIISKA LICENSE-KA (min-width) =====
content = content.replace(
    'min-width: 600px;',
    'min-width: 750px;'
)

# ===== 2. DHIS QAYBTA USERS, REFERRALS, SETTINGS =====
old_start = content.find("async function loadPage(pageName")
old_end = content.find("async function fetchStats()")

if old_start != -1 and old_end != -1:
    new_loadpage = '''async function loadPage(pageName, element = null) {
        if (element) {
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
            element.classList.add('active');
        }
        
        const contentArea = document.getElementById('page-content');
        
        if (pageName === 'dashboard') {
            contentArea.innerHTML = `
                <h1 style="margin-bottom: 20px;">Dashboard Overview</h1>
                <div class="stats-grid" id="stats-grid">
                    <div class="stat-card"><span class="title">Loading...</span></div>
                </div>
                <div class="charts-grid">
                    <div class="chart-box">
                        <h3>Analytics Overview</h3>
                        <canvas id="analyticsChart"></canvas>
                    </div>
                    <div class="chart-box">
                        <h3>License Status</h3>
                        <canvas id="licenseChart"></canvas>
                    </div>
                </div>
            `;
            await fetchStats();
        } 
        else if (pageName === 'users') {
            contentArea.innerHTML = `
                <h1 style="margin-bottom: 20px;">Users Management</h1>
                <div style="display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap;">
                    <div class="search-bar" style="flex: 1; min-width: 200px;">
                        <i class="fa-solid fa-search"></i>
                        <input type="text" id="user-search" placeholder="Search users..." onkeyup="filterUsers()">
                    </div>
                    <button class="submit-btn" style="max-width: 200px;" onclick="showAddUserModal()">
                        <i class="fa-solid fa-plus"></i> Add User
                    </button>
                </div>
                <div class="chart-box" style="overflow-x: auto;">
                    <table style="width: 100%; border-collapse: collapse; min-width: 750px;">
                        <thead>
                            <tr style="border-bottom: 1px solid #2a2a35;">
                                <th style="padding: 12px; text-align: left;">ID</th>
                                <th style="padding: 12px; text-align: left;">Username</th>
                                <th style="padding: 12px; text-align: left;">Full Name</th>
                                <th style="padding: 12px; text-align: left;">Role</th>
                                <th style="padding: 12px; text-align: left;">License</th>
                                <th style="padding: 12px; text-align: left;">Actions</th>
                            </tr>
                        </thead>
                        <tbody id="users-tbody">
                            <tr><td colspan="6" style="padding: 20px; text-align: center;">Loading...</td></tr>
                        </tbody>
                    </table>
                </div>
            `;
            await loadUsers();
        }
        else if (pageName === 'licenses') {
            contentArea.innerHTML = `
                <h1 style="margin-bottom: 20px;">Licenses Management</h1>
                <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                    <button class="submit-btn" style="max-width: 250px;" onclick="showGenerateLicenseModal()">
                        <i class="fa-solid fa-plus"></i> Generate License
                    </button>
                </div>
                <div class="chart-box" style="overflow-x: auto;">
                    <table style="width: 100%; border-collapse: collapse; min-width: 750px;">
                        <thead>
                            <tr style="border-bottom: 1px solid #2a2a35;">
                                <th style="padding: 12px; text-align: left; white-space: nowrap;">License Key</th>
                                <th style="padding: 12px; text-align: left;">User ID</th>
                                <th style="padding: 12px; text-align: left;">Duration</th>
                                <th style="padding: 12px; text-align: left;">Status</th>
                                <th style="padding: 12px; text-align: left;">Actions</th>
                            </tr>
                        </thead>
                        <tbody id="licenses-tbody">
                            <tr><td colspan="5" style="padding: 20px; text-align: center;">Loading...</td></tr>
                        </tbody>
                    </table>
                </div>
            `;
            await loadLicenses();
        }
        else if (pageName === 'referrals') {
            contentArea.innerHTML = `
                <h1 style="margin-bottom: 20px;">Referrals</h1>
                <div class="chart-box" style="overflow-x: auto;">
                    <table style="width: 100%; border-collapse: collapse; min-width: 500px;">
                        <thead>
                            <tr style="border-bottom: 1px solid #2a2a35;">
                                <th style="padding: 12px; text-align: left;">ID</th>
                                <th style="padding: 12px; text-align: left;">Referrer Code</th>
                                <th style="padding: 12px; text-align: left;">Referred User</th>
                            </tr>
                        </thead>
                        <tbody id="referrals-tbody">
                            <tr><td colspan="3" style="padding: 20px; text-align: center;">Loading...</td></tr>
                        </tbody>
                    </table>
                </div>
            `;
            await loadReferrals();
        }
        else if (pageName === 'settings') {
            contentArea.innerHTML = `
                <h1 style="margin-bottom: 20px;">Settings</h1>
                <div class="chart-box">
                    <h3 style="margin-bottom: 15px;">Profile</h3>
                    <p style="color: #8b8b9e; margin-bottom: 10px;">Username: <strong>${JSON.parse(localStorage.getItem('user') || '{}').username || 'N/A'}</strong></p>
                    <p style="color: #8b8b9e; margin-bottom: 10px;">Role: <strong>${JSON.parse(localStorage.getItem('user') || '{}').role || 'N/A'}</strong></p>
                    <p style="color: #8b8b9e;">License: <strong>${JSON.parse(localStorage.getItem('user') || '{}').license_key || 'N/A'}</strong></p>
                </div>
            `;
        }
    }
    
    async function loadReferrals() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/admin/referrals', {
                headers: { 'Authorization': 'Bearer ' + token }
            });
            const data = await response.json();
            const tbody = document.getElementById('referrals-tbody');
            if (!tbody) return;
            if (!Array.isArray(data) || data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3" style="padding: 20px; text-align: center;">Ma jiro referral</td></tr>';
                return;
            }
            tbody.innerHTML = data.map(function(r) {
                return '<tr style="border-bottom: 1px solid #2a2a35;">' +
                    '<td style="padding: 12px;">' + r.id + '</td>' +
                    '<td style="padding: 12px;">' + r.referrer_code + '</td>' +
                    '<td style="padding: 12px;">' + r.referred_user + '</td>' +
                    '</tr>';
            }).join('');
        } catch (error) {
            const tbody = document.getElementById('referrals-tbody');
            if (tbody) tbody.innerHTML = '<tr><td colspan="3" style="padding: 20px; text-align: center;">Error</td></tr>';
        }
    }
    
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
                var roleColor = u.role === 'admin' ? '#8b5cf6' : '#2a2a35';
                return '<tr style="border-bottom: 1px solid #2a2a35;">' +
                    '<td style="padding: 12px;">' + u.id + '</td>' +
                    '<td style="padding: 12px;"><strong>' + u.username + '</strong></td>' +
                    '<td style="padding: 12px;">' + (u.fullname || '-') + '</td>' +
                    '<td style="padding: 12px;"><span style="padding: 4px 10px; border-radius: 20px; background: ' + roleColor + '; font-size: 12px;">' + u.role + '</span></td>' +
                    '<td style="padding: 12px;">' + (u.license_key || '-') + '</td>' +
                    '<td style="padding: 12px;">' +
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
                var statusColor = l.status === 'unused' ? '#10b981' : (l.status === 'used' ? '#f59e0b' : '#ef4444');
                return '<tr style="border-bottom: 1px solid #2a2a35;">' +
                    '<td style="padding: 12px;"><code style="background: #1e1e28; padding: 4px 8px; border-radius: 4px; font-size: 12px; white-space: nowrap;">' + l.license_key + '</code></td>' +
                    '<td style="padding: 12px;">' + (l.user_id || '-') + '</td>' +
                    '<td style="padding: 12px;">' + (l.duration || '-') + '</td>' +
                    '<td style="padding: 12px;"><span style="padding: 4px 10px; border-radius: 20px; background: ' + statusColor + '20; color: ' + statusColor + '; font-size: 12px; font-weight: 600;">' + l.status + '</span></td>' +
                    '<td style="padding: 12px;">' +
                        '<button onclick="copyLicense(\\'' + l.license_key + '\\')" style="background: #8b5cf6; border: none; color: white; padding: 6px 10px; border-radius: 6px; cursor: pointer; margin-right: 5px;">' +
                            '<i class="fa-solid fa-copy"></i>' +
                        '</button>' +
                        '<button onclick="deleteLicense(' + l.id + ')" style="background: #ef4444; border: none; color: white; padding: 6px 10px; border-radius: 6px; cursor: pointer;">' +
                            '<i class="fa-solid fa-trash"></i>' +
                        '</button>' +
                    '</td>' +
                    '</tr>';
            }).join('');
        } catch (error) {
            console.error('Error loading licenses:', error);
        }
    }
    
    '''
    content = content[:old_start] + new_loadpage + content[old_end:]
    print("✅ loadPage, loadUsers, loadLicenses, loadReferrals waa la cusboonaysiiyay!")

# ===== 3. KU DAR MODAL-KA ADD USER IYO PROFILE MENU =====
add_modal = '''
<!-- ADD USER MODAL -->
<div id="add-user-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 9999; justify-content: center; align-items: center;">
    <div style="background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 20px; padding: 30px; width: 90%; max-width: 500px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
            <h2 style="font-size: 22px; font-weight: 700;">Add User</h2>
            <button onclick="closeAddUserModal()" style="background: transparent; border: none; color: var(--text-muted); font-size: 24px; cursor: pointer;">
                <i class="fa-solid fa-xmark"></i>
            </button>
        </div>
        <div style="margin-bottom: 18px;">
            <label style="display: block; margin-bottom: 8px; font-size: 14px; font-weight: 500;">Username</label>
            <input type="text" id="new-username" placeholder="Enter username" style="width: 100%; padding: 12px; background: var(--input-bg); border: 1px solid var(--border-color); border-radius: 10px; color: var(--text-color); outline: none;">
        </div>
        <div style="margin-bottom: 18px;">
            <label style="display: block; margin-bottom: 8px; font-size: 14px; font-weight: 500;">Password</label>
            <input type="password" id="new-password" placeholder="Enter password" style="width: 100%; padding: 12px; background: var(--input-bg); border: 1px solid var(--border-color); border-radius: 10px; color: var(--text-color); outline: none;">
        </div>
        <div style="margin-bottom: 25px;">
            <label style="display: block; margin-bottom: 8px; font-size: 14px; font-weight: 500;">Full Name</label>
            <input type="text" id="new-fullname" placeholder="Enter full name" style="width: 100%; padding: 12px; background: var(--input-bg); border: 1px solid var(--border-color); border-radius: 10px; color: var(--text-color); outline: none;">
        </div>
        <button onclick="addUser()" class="submit-btn" style="width: 100%;">
            <i class="fa-solid fa-plus"></i> Add User
        </button>
    </div>
</div>

<!-- PROFILE MENU -->
<div id="profile-menu" style="display: none; position: absolute; top: 70px; right: 30px; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 10px; min-width: 180px; z-index: 9998; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
    <a href="#" onclick="handleLogout()" style="display: flex; align-items: center; gap: 10px; padding: 10px 15px; color: var(--text-color); text-decoration: none; border-radius: 8px;">
        <i class="fa-solid fa-right-from-bracket"></i> Logout
    </a>
</div>
'''

body_pos = content.find("</body>")
if body_pos != -1:
    content = content[:body_pos] + add_modal + "\n" + content[body_pos:]
    print("✅ Add User Modal iyo Profile Menu waa lagu daray!")

# ===== 4. KU DAR FUNCTIONS-KA CUSUB =====
new_funcs = '''
    // ===== ADD USER FUNCTIONS =====
    function showAddUserModal() {
        var modal = document.getElementById('add-user-modal');
        if (modal) {
            modal.style.display = 'flex';
            document.getElementById('new-username').value = '';
            document.getElementById('new-password').value = '';
            document.getElementById('new-fullname').value = '';
        }
    }
    
    function closeAddUserModal() {
        var modal = document.getElementById('add-user-modal');
        if (modal) modal.style.display = 'none';
    }
    
    async function addUser() {
        var username = document.getElementById('new-username').value.trim();
        var password = document.getElementById('new-password').value.trim();
        var fullname = document.getElementById('new-fullname').value.trim();
        
        if (!username || !password) {
            alert('Fadlan geli username iyo password');
            return;
        }
        
        try {
            var response = await fetch('/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username, password: password, fullname: fullname })
            });
            var data = await response.json();
            if (data.token || data.success) {
                closeAddUserModal();
                alert('User cusub waa la abuuray!');
                loadUsers();
            } else {
                alert('Error: ' + (data.error || 'Unknown'));
            }
        } catch (e) {
            alert('Error: ' + e.message);
        }
    }
    
    async function deleteUser(id) {
        if (!confirm('Ma hubtaa inaad tirtirto user-kan?')) return;
        try {
            var token = localStorage.getItem('token');
            var res = await fetch('/api/admin/users/' + id, {
                method: 'DELETE',
                headers: { 'Authorization': 'Bearer ' + token }
            });
            if (res.ok) loadUsers();
            else alert('Error deleting user');
        } catch (e) { alert('Error: ' + e.message); }
    }
    
    async function deleteLicense(id) {
        if (!confirm('Ma hubtaa inaad tirtirto license-kan?')) return;
        try {
            var token = localStorage.getItem('token');
            var res = await fetch('/api/admin/licenses/' + id, {
                method: 'DELETE',
                headers: { 'Authorization': 'Bearer ' + token }
            });
            if (res.ok) loadLicenses();
            else alert('Error deleting license');
        } catch (e) { alert('Error: ' + e.message); }
    }
    
    function filterUsers() {
        var input = document.getElementById('user-search');
        if (!input) return;
        var val = input.value.toLowerCase();
        var rows = document.querySelectorAll('#users-tbody tr');
        rows.forEach(function(row) {
            row.style.display = row.textContent.toLowerCase().includes(val) ? '' : 'none';
        });
    }
    
    function toggleProfileMenu() {
        var menu = document.getElementById('profile-menu');
        if (menu) menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
    }
    
    document.addEventListener('click', function(e) {
        var menu = document.getElementById('profile-menu');
        var profile = document.querySelector('.user-profile');
        if (menu && profile && !profile.contains(e.target)) {
            menu.style.display = 'none';
        }
    });
'''

target = "function handleLogout()"
pos = content.find(target)
if pos != -1:
    content = content[:pos] + new_funcs + "\n    " + content[pos:]
    print("✅ Functions-ka cusub waa lagu daray!")

# ===== 5. HAGAaji PROFILE CLICK =====
content = content.replace(
    '<div class="user-profile">',
    '<div class="user-profile" onclick="toggleProfileMenu()" style="cursor: pointer;">'
)

with open("public/index.html", "w") as f:
    f.write(content)

print("✅ Faylka 'public/index.html' waa la cusboonaysiiyay!")
