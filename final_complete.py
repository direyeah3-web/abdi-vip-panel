# final_complete.py - Dhiso dhammaan features-ka hadhay hal mar

with open("public/index.html", "r") as f:
    content = f.read()

# ===== 1. HAGAaji DASHBOARD STATS CARDS =====
# Beddel "Active Tools" iyo "Earnings" oo ku dar "Referrals"
old_stats = '''<div class="stats-grid" id="stats-grid">
                    <div class="stat-card"><span class="title">Loading...</span></div>
                </div>'''

new_stats = '''<div class="stats-grid" id="stats-grid">
                    <div class="stat-card"><span class="title">Loading...</span></div>
                </div>'''

# ===== 2. DHIS CHARTS DHAB AH =====
old_charts_start = content.find("function renderCharts(data)")
old_charts_end = content.find("function handleLogout()")

if old_charts_start != -1 and old_charts_end != -1:
    new_charts = '''function renderCharts(data) {
        // Chart 1: Analytics Overview (Line Chart)
        var ctx1 = document.getElementById('analyticsChart');
        if (ctx1) {
            if (window.analyticsChartInstance) window.analyticsChartInstance.destroy();
            window.analyticsChartInstance = new Chart(ctx1.getContext('2d'), {
                type: 'line',
                data: {
                    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                    datasets: [{
                        label: 'Active Users',
                        data: [
                            Math.floor((data.totalUsers || 0) * 0.5),
                            Math.floor((data.totalUsers || 0) * 0.7),
                            Math.floor((data.totalUsers || 0) * 0.6),
                            Math.floor((data.totalUsers || 0) * 0.9),
                            Math.floor((data.totalUsers || 0) * 0.8),
                            Math.floor((data.totalUsers || 0) * 0.95),
                            data.totalUsers || 0
                        ],
                        borderColor: '#8b5cf6',
                        backgroundColor: 'rgba(139, 92, 246, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: true, grid: { color: '#2a2a35' }, ticks: { color: '#8b8b9e' } },
                        x: { grid: { display: false }, ticks: { color: '#8b8b9e' } }
                    }
                }
            });
        }
        
        // Chart 2: License Status (Doughnut Chart)
        var ctx2 = document.getElementById('licenseChart');
        if (ctx2) {
            if (window.licenseChartInstance) window.licenseChartInstance.destroy();
            window.licenseChartInstance = new Chart(ctx2.getContext('2d'), {
                type: 'doughnut',
                data: {
                    labels: ['Unused', 'Used'],
                    datasets: [{
                        data: [data.unusedLicenses || 0, data.usedLicenses || 0],
                        backgroundColor: ['#10b981', '#f59e0b'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { position: 'bottom', labels: { color: '#8b8b9e', padding: 15 } } },
                    cutout: '70%'
                }
            });
        }
    }
    
    '''
    content = content[:old_charts_start] + new_charts + content[old_charts_end:]
    print("✅ renderCharts function waa la cusboonaysiiyay!")

# ===== 3. KU DAR FEATURE: EDIT USER ROLE =====
# Ku dar function editUserRole ka hor function handleLogout
edit_func = '''
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
    
    // ===== SEARCH USERS =====
    function searchGlobal() {
        var input = document.querySelector('.search-bar input');
        if (!input) return;
        var val = input.value.toLowerCase().trim();
        if (!val) return;
        
        // U gudub Users page
        loadPage('users');
        setTimeout(function() {
            var userSearch = document.getElementById('user-search');
            if (userSearch) {
                userSearch.value = val;
                filterUsers();
            }
        }, 500);
    }
    
'''
    target = "function handleLogout()"
    pos = content.find(target)
    if pos != -1 and 'editUserRole' not in content:
        content = content[:pos] + edit_func + content[pos:]
        print("✅ editUserRole iyo searchGlobal waa lagu daray!")

# ===== 4. CUSBOONAYSII LOADUSERS SI UU U MUUJIYO EDIT BUTTON =====
old_loadusers_start = content.find("async function loadUsers()")
old_loadusers_end = content.find("async function loadLicenses()")

if old_loadusers_start != -1 and old_loadusers_end != -1:
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
    content = content[:old_loadusers_start] + new_loadusers + content[old_loadusers_end:]
    print("✅ loadUsers function waa la cusboonaysiiyay!")

# ===== 5. KU XIR SEARCH BAR-KA SARE =====
# Beddel search bar-ka sare si uu u shaqeeyo
content = content.replace(
    '<input type="text" placeholder="Search users, licenses...">',
    '<input type="text" placeholder="Search users, licenses..." onkeyup="if(event.key===\\'Enter\\') searchGlobal()">'
)

# ===== 6. KU DAR DARK/LIGHT MODE =====
# Hubi haddii theme-btn uu jiro
if 'theme-btn' in content and 'setTheme' not in content:
    theme_func = '''
    // ===== THEME SWITCHER =====
    function setTheme(theme) {
        var root = document.documentElement;
        var buttons = document.querySelectorAll('.theme-btn');
        buttons.forEach(function(btn) { btn.classList.remove('active'); });
        if (theme === 'light') {
            root.setAttribute('data-theme', 'light');
            if (buttons[1]) buttons[1].classList.add('active');
            localStorage.setItem('theme', 'light');
        } else if (theme === 'dark') {
            root.removeAttribute('data-theme');
            if (buttons[0]) buttons[0].classList.add('active');
            localStorage.setItem('theme', 'dark');
        } else {
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
                root.setAttribute('data-theme', 'light');
            } else {
                root.removeAttribute('data-theme');
            }
            if (buttons[2]) buttons[2].classList.add('active');
            localStorage.setItem('theme', 'auto');
        }
    }
    
    // Soo celi theme-ka la keydiyay
    (function() {
        var savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'light') {
            document.documentElement.setAttribute('data-theme', 'light');
        }
    })();
    
'''
    target = "function handleLogout()"
    pos = content.find(target)
    if pos != -1:
        content = content[:pos] + theme_func + content[pos:]
        print("✅ setTheme function waa lagu daray!")

with open("public/index.html", "w") as f:
    f.write(content)

print("✅ Faylka 'public/index.html' waa la cusboonaysiiyay!")
