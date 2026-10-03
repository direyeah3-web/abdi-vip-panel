# final_11_10.py - Dhiso 11/10 dashboard

with open("public/index.html", "r") as f:
    content = f.read()

# ===== 1. KU DAR LIGHT MODE (Soft Blue-Grey) =====
old_root = ''':root{--bg:#0a0a0f;--sidebar:#0d0d14;--card:#12121a;--card-hover:#1a1a24;--text:#fff;--muted:#6b6b7e;--primary:#00d4ff;--purple:#8b5cf6;--green:#10b981;--yellow:#f59e0b;--red:#ef4444;--border:#1e1e2a;}'''

new_root = ''':root{--bg:#0a0a0f;--sidebar:#0d0d14;--card:#12121a;--card-hover:#1a1a24;--text:#fff;--muted:#6b6b7e;--primary:#00d4ff;--purple:#8b5cf6;--green:#10b981;--yellow:#f59e0b;--red:#ef4444;--border:#1e1e2a;}
[data-theme="light"]{--bg:#eef2f7;--sidebar:#ffffff;--card:#f8fafc;--card-hover:#e8eef5;--text:#1a2332;--muted:#64748b;--primary:#0ea5e9;--purple:#7c3aed;--green:#059669;--yellow:#d97706;--red:#dc2626;--border:#d1dbe8;box-shadow:0 1px 3px rgba(0,0,0,.05);}
[data-theme="light"] body{background:linear-gradient(135deg,#eef2f7 0%,#e0e7ff 100%);}
[data-theme="light"] .sidebar{background:#ffffff;border-right:1px solid var(--border);}
[data-theme="light"] .card,[data-theme="light"] .stat-card,[data-theme="light"] .panel,[data-theme="light"] .hero{background:#ffffff;border:1px solid var(--border);}
[data-theme="light"] input,[data-theme="light"] select{background:#ffffff;border:1px solid var(--border);color:var(--text);}
[data-theme="light"] .quick-action{background:#f1f5f9;}
[data-theme="light"] .quick-action:hover{background:#e2e8f0;}
[data-theme="light"] .tab{color:var(--muted);}
[data-theme="light"] .topnav{background:#ffffff;border-bottom:1px solid var(--border);}
[data-theme="light"] .sidebar-logo,[data-theme="light"] .login-logo{background:linear-gradient(135deg,#0ea5e9,#7c3aed);}'''

content = content.replace(old_root, new_root)

# ===== 2. KU DAR THEME TOGGLE BUTTON =====
old_topnav = '''<header class="topnav">
<button class="menu-toggle" onclick="toggleSidebar()"><i class="fa-solid fa-bars"></i></button>
<div class="search-bar"><i class="fa-solid fa-search"></i><input type="text" placeholder="Search..."></div>
<div style="display:flex;align-items:center;gap:10px;">
<div class="status-badge"><div class="status-dot"></div><span class="status-text">All Systems Active</span></div>
<button class="submit-btn" style="width:auto;padding:10px 14px;margin:0;" onclick="handleLogout()"><i class="fa-solid fa-right-from-bracket"></i></button>
</div>
</header>'''

new_topnav = '''<header class="topnav">
<button class="menu-toggle" onclick="toggleSidebar()"><i class="fa-solid fa-bars"></i></button>
<div class="search-bar"><i class="fa-solid fa-search"></i><input type="text" placeholder="Search..."></div>
<div style="display:flex;align-items:center;gap:8px;">
<div class="status-badge"><div class="status-dot"></div><span class="status-text">All Systems Active</span></div>
<button class="icon-btn" onclick="toggleTheme()" title="Toggle Theme"><i class="fa-solid fa-sun" id="theme-icon"></i></button>
<button class="icon-btn" onclick="showNotifications()" title="Notifications" style="position:relative;"><i class="fa-regular fa-bell"></i><span style="position:absolute;top:6px;right:6px;width:8px;height:8px;background:var(--red);border-radius:50%;"></span></button>
<button class="submit-btn" style="width:auto;padding:10px 14px;margin:0;" onclick="handleLogout()"><i class="fa-solid fa-right-from-bracket"></i></button>
</div>
</header>'''

content = content.replace(old_topnav, new_topnav)

# ===== 3. KU DAR THEME FUNCTION =====
theme_func = '''
function toggleTheme() {
    var root = document.documentElement;
    var icon = document.getElementById('theme-icon');
    if (root.getAttribute('data-theme') === 'light') {
        root.removeAttribute('data-theme');
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
        localStorage.setItem('theme', 'dark');
    } else {
        root.setAttribute('data-theme', 'light');
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
        localStorage.setItem('theme', 'light');
    }
}

function showNotifications() {
    alert('Notifications:\\n\\n1. New user registered (2 min ago)\\n2. License generated (15 min ago)\\n3. System updated (3 hours ago)');
}

(function() {
    var saved = localStorage.getItem('theme');
    if (saved === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
        setTimeout(function() {
            var icon = document.getElementById('theme-icon');
            if (icon) { icon.classList.remove('fa-sun'); icon.classList.add('fa-moon'); }
        }, 100);
    }
})();
'''
content = content.replace('function handleLogout()', theme_func + '\nfunction handleLogout()')

# ===== 4. BUUXI DASHBOARD-KA (Revenue, Top Users, License Chart) =====
old_dashboard = '''if(p==='dashboard'){
        c.innerHTML='<div class="hero"><div class="hero-badge">Welcome Back</div><h1>Hello, <span>'+(u.username||'User')+'</span></h1><p>You are in control. Here is what is happening with your panel today.</p><div class="hero-buttons"><button class="btn-primary" onclick="loadPage(\\'licenses\\')"><i class="fa-solid fa-plus"></i> Generate License</button><button class="btn-secondary" onclick="loadPage(\\'users\\')"><i class="fa-solid fa-users"></i> Manage Users</button></div></div>'+
        '<div class="stats-grid" id="stats-grid"><div class="stat-card">Loading...</div></div>'+
        '<div class="content-grid">'+
            '<div class="panel"><div class="panel-header"><h3>Analytics Overview</h3></div><canvas id="analyticsChart" height="200"></canvas></div>'+
            '<div class="panel"><div class="panel-header"><h3>License Status</h3></div><canvas id="licenseChart" height="200"></canvas></div>'+
        '</div>'+
        '<div class="content-grid" style="margin-top:20px;">'+
            '<div class="panel"><div class="panel-header"><h3>Recent Activity</h3><a href="#">View All</a></div><div id="activity-list"><p style="color:var(--muted);text-align:center;padding:20px;">Loading...</p></div></div>'+
            '<div class="panel"><div class="panel-header"><h3>Quick Actions</h3></div>'+
                '<div class="quick-action" onclick="loadPage(\\'licenses\\')"><i class="fa-solid fa-key"></i><span>Generate License</span></div>'+
                '<div class="quick-action" onclick="loadPage(\\'users\\')"><i class="fa-solid fa-user-plus"></i><span>Add User</span></div>'+
                '<div class="quick-action" onclick="loadPage(\\'referrals\\')"><i class="fa-solid fa-share-nodes"></i><span>View Referrals</span></div>'+
                '<div class="quick-action" onclick="loadPage(\\'settings\\')"><i class="fa-solid fa-gear"></i><span>System Settings</span></div>'+
            '</div>'+
        '</div>';
        await fetchStats();
        loadActivity();
    }'''

new_dashboard = '''if(p==='dashboard'){
        c.innerHTML='<div class="hero"><div class="hero-badge">Welcome Back</div><h1>Hello, <span>'+(u.username||'User')+'</span></h1><p>You are in control. Here is what is happening with your panel today.</p><div class="hero-buttons"><button class="btn-primary" onclick="loadPage(\\'licenses\\')"><i class="fa-solid fa-plus"></i> Generate License</button><button class="btn-secondary" onclick="loadPage(\\'users\\')"><i class="fa-solid fa-users"></i> Manage Users</button></div></div>'+
        '<div class="stats-grid" id="stats-grid"><div class="stat-card">Loading...</div></div>'+
        '<div class="content-grid">'+
            '<div class="panel"><div class="panel-header"><h3>Analytics Overview</h3></div><canvas id="analyticsChart" height="220"></canvas></div>'+
            '<div class="panel"><div class="panel-header"><h3>License Status</h3></div><canvas id="licenseChart" height="220"></canvas></div>'+
        '</div>'+
        '<div class="content-grid" style="margin-top:20px;">'+
            '<div class="panel"><div class="panel-header"><h3>Revenue</h3><span style="color:var(--green);font-size:13px;font-weight:600;"><i class="fa-solid fa-arrow-up"></i> +12.5%</span></div>'+
                '<div style="display:flex;align-items:center;gap:20px;padding:10px 0;">'+
                    '<div style="width:60px;height:60px;background:linear-gradient(135deg,var(--primary),var(--purple));border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:24px;color:#fff;"><i class="fa-solid fa-dollar-sign"></i></div>'+
                    '<div><div style="font-size:36px;font-weight:800;">$2,500</div><div style="color:var(--muted);font-size:13px;">Total revenue this month</div></div>'+
                '</div>'+
            '</div>'+
            '<div class="panel"><div class="panel-header"><h3>Top Users</h3><a href="#">View All</a></div><div id="top-users"><p style="color:var(--muted);text-align:center;padding:20px;">Loading...</p></div></div>'+
        '</div>'+
        '<div class="content-grid" style="margin-top:20px;">'+
            '<div class="panel"><div class="panel-header"><h3>Recent Activity</h3><a href="#">View All</a></div><div id="activity-list"><p style="color:var(--muted);text-align:center;padding:20px;">Loading...</p></div></div>'+
            '<div class="panel"><div class="panel-header"><h3>Quick Actions</h3></div>'+
                '<div class="quick-action" onclick="loadPage(\\'licenses\\')"><i class="fa-solid fa-key"></i><span>Generate License</span></div>'+
                '<div class="quick-action" onclick="loadPage(\\'users\\')"><i class="fa-solid fa-user-plus"></i><span>Add User</span></div>'+
                '<div class="quick-action" onclick="loadPage(\\'referrals\\')"><i class="fa-solid fa-share-nodes"></i><span>View Referrals</span></div>'+
                '<div class="quick-action" onclick="loadPage(\\'settings\\')"><i class="fa-solid fa-gear"></i><span>System Settings</span></div>'+
            '</div>'+
        '</div>';
        await fetchStats();
        loadActivity();
        loadTopUsers();
    }'''

content = content.replace(old_dashboard, new_dashboard)

# ===== 5. KU DAR LOADTOPUSERS FUNCTION =====
top_users_func = '''
async function loadTopUsers() {
    var list = document.getElementById('top-users');
    if (!list) return;
    try {
        var token = localStorage.getItem('token');
        var res = await fetch('/api/admin/users', { headers: { 'Authorization': 'Bearer ' + token } });
        var users = await res.json();
        if (!Array.isArray(users) || users.length === 0) {
            list.innerHTML = '<p style="color:var(--muted);text-align:center;padding:20px;">No users</p>';
            return;
        }
        list.innerHTML = users.slice(0, 4).map(function(u) {
            return '<div class="activity-item">' +
                '<div class="user-avatar" style="width:36px;height:36px;font-size:13px;">' + u.username.charAt(0).toUpperCase() + '</div>' +
                '<div style="flex:1;"><div style="font-size:14px;font-weight:600;">' + u.username + '</div><div style="font-size:12px;color:var(--muted);">' + (u.role === 'admin' ? 'Administrator' : 'User') + '</div></div>' +
                '<span style="padding:4px 10px;border-radius:20px;background:' + (u.role === 'admin' ? 'rgba(139,92,246,.2);color:#8b5cf6' : 'rgba(16,185,129,.2);color:#10b981') + ';font-size:11px;font-weight:600;">' + u.role + '</span>' +
            '</div>';
        }).join('');
    } catch(e) { list.innerHTML = '<p style="color:var(--muted);text-align:center;padding:20px;">Error</p>'; }
}
'''
content = content.replace('function handleLogout()', top_users_func + '\nfunction handleLogout()')

# ===== 6. HAGAaji LICENSE CHART (marka aan xog jirin) =====
old_chart = '''var c2=document.getElementById('licenseChart');
    if(c2){
        if(window.licenseChart)window.licenseChart.destroy();
        window.licenseChart=new Chart(c2.getContext('2d'),{
            type:'doughnut',
            data:{labels:['Available','Used'],datasets:[{data:[d.unusedLicenses||0,d.usedLicenses||0],backgroundColor:['#10b981','#f59e0b'],borderWidth:0}]},
            options:{responsive:true,plugins:{legend:{position:'bottom',labels:{color:'#6b6b7e',padding:15}}},cutout:'70%'}
        });
    }'''

new_chart = '''var c2=document.getElementById('licenseChart');
    if(c2){
        if(window.licenseChart)window.licenseChart.destroy();
        var unused = d.unusedLicenses || 0;
        var used = d.usedLicenses || 0;
        if (unused === 0 && used === 0) {
            c2.parentElement.innerHTML = '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:200px;color:var(--muted);"><i class="fa-solid fa-chart-pie" style="font-size:40px;margin-bottom:15px;opacity:0.3;"></i><p>No license data yet</p><p style="font-size:12px;margin-top:5px;">Generate licenses to see the chart</p></div>';
        } else {
            window.licenseChart=new Chart(c2.getContext('2d'),{
                type:'doughnut',
                data:{labels:['Available','Used'],datasets:[{data:[unused,used],backgroundColor:['#10b981','#f59e0b'],borderWidth:0}]},
                options:{responsive:true,plugins:{legend:{position:'bottom',labels:{color:'#6b6b7e',padding:15}}},cutout:'70%'}
            });
        }
    }'''

content = content.replace(old_chart, new_chart)

# ===== 7. KU DAR ICON-BTN CSS =====
css = '''
.icon-btn {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: var(--card);
    border: 1px solid var(--border);
    color: var(--text);
    cursor: pointer;
    transition: 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
}
.icon-btn:hover { background: var(--card-hover); border-color: var(--primary); }
'''
style_end = content.find("</style>")
if style_end != -1:
    content = content[:style_end] + css + content[style_end:]

with open("public/index.html", "w") as f:
    f.write(content)

print("✅ 11/10 Dashboard waa la dhisay!")
print("✅ Light Mode (Soft Blue-Grey) waa lagu daray!")
print("✅ Revenue Card, Top Users, Notifications waa lagu daray!")
