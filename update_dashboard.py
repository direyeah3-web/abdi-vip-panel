import os

# Qoraalka HTML-ka oo dhamaystiran (Login + Dashboard)
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ABDI VIP PANEL</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-color: #0d0d12;
            --card-bg: #16161e;
            --text-color: #ffffff;
            --text-muted: #8b8b9e;
            --primary-color: #8b5cf6;
            --primary-hover: #7c3aed;
            --input-bg: #1e1e28;
            --border-color: #2a2a35;
        }
        [data-theme="light"] {
            --bg-color: #f3f4f6;
            --card-bg: #ffffff;
            --text-color: #1f2937;
            --text-muted: #6b7280;
            --input-bg: #f9fafb;
            --border-color: #e5e7eb;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-color); display: flex; justify-content: center; align-items: center; min-height: 100vh; transition: 0.3s; }
        
        /* Login Card */
        .login-card { background-color: var(--card-bg); width: 100%; max-width: 420px; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid var(--border-color); position: relative; }
        .logo-section { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 25px; }
        .logo-box { width: 60px; height: 60px; background: linear-gradient(135deg, #1e1e28, #2a2a35); border-radius: 15px; display: flex; justify-content: center; align-items: center; border: 1px solid var(--border-color); box-shadow: 0 0 15px rgba(139, 92, 246, 0.2); }
        .logo-box i { font-size: 24px; color: var(--primary-color); }
        .theme-switcher { display: flex; background: var(--input-bg); padding: 5px; border-radius: 10px; border: 1px solid var(--border-color); gap: 5px; }
        .theme-btn { background: transparent; border: none; color: var(--text-muted); padding: 8px 10px; cursor: pointer; border-radius: 6px; transition: 0.2s; }
        .theme-btn.active { background: var(--card-bg); color: var(--text-color); box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
        
        /* Tabs */
        .tabs { display: flex; background: var(--input-bg); padding: 5px; border-radius: 12px; margin-bottom: 25px; }
        .tab { flex: 1; padding: 12px; text-align: center; cursor: pointer; border-radius: 8px; font-weight: 600; color: var(--text-muted); transition: 0.3s; }
        .tab.active { background: var(--primary-color); color: white; }
        
        /* Form */
        .form-group { margin-bottom: 18px; }
        .form-group label { display: block; margin-bottom: 8px; font-size: 14px; font-weight: 500; }
        .input-wrapper { position: relative; display: flex; align-items: center; }
        .input-wrapper i.prefix-icon { position: absolute; left: 15px; color: var(--text-muted); font-size: 16px; }
        .input-wrapper input { width: 100%; padding: 14px 15px 14px 45px; background: var(--input-bg); border: 1px solid var(--border-color); border-radius: 12px; color: var(--text-color); font-size: 15px; outline: none; transition: 0.2s; }
        .input-wrapper input:focus { border-color: var(--primary-color); box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1); }
        .eye-icon { position: absolute; right: 15px; color: var(--text-muted); cursor: pointer; font-size: 16px; }
        .checkbox-group { display: flex; align-items: center; gap: 10px; margin-bottom: 25px; }
        .checkbox-group input[type="checkbox"] { accent-color: var(--primary-color); width: 18px; height: 18px; cursor: pointer; }
        .checkbox-group label { font-size: 14px; cursor: pointer; }
        .submit-btn { width: 100%; padding: 15px; background: var(--primary-color); color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; display: flex; justify-content: center; align-items: center; gap: 10px; transition: 0.3s; }
        .submit-btn:hover { background: var(--primary-hover); transform: translateY(-2px); }
        .register-fields { display: none; }
        .register-fields.active { display: block; }
        .login-fields.hidden { display: none; }
        
        /* Dashboard */
        #dashboard-container { display: none; width: 100vw; height: 100vh; background-color: var(--bg-color); color: var(--text-color); overflow: hidden; position: fixed; top: 0; left: 0; z-index: 1000; }
        .sidebar { width: 260px; background-color: var(--card-bg); border-right: 1px solid var(--border-color); display: flex; flex-direction: column; padding: 20px 0; transition: 0.3s; }
        .sidebar-header { display: flex; align-items: center; gap: 12px; padding: 0 20px 30px; font-size: 20px; font-weight: 700; color: var(--primary-color); }
        .sidebar-nav { flex: 1; display: flex; flex-direction: column; gap: 5px; }
        .nav-item { display: flex; align-items: center; gap: 15px; padding: 12px 20px; color: var(--text-muted); text-decoration: none; font-weight: 500; transition: 0.2s; border-left: 3px solid transparent; }
        .nav-item:hover, .nav-item.active { background-color: rgba(139, 92, 246, 0.1); color: var(--primary-color); border-left-color: var(--primary-color); }
        .sidebar-footer { border-top: 1px solid var(--border-color); padding-top: 15px; }
        .main-content { flex: 1; display: flex; flex-direction: column; overflow-y: auto; }
        .top-nav { display: flex; justify-content: space-between; align-items: center; padding: 15px 30px; background-color: var(--card-bg); border-bottom: 1px solid var(--border-color); }
        .search-bar { display: flex; align-items: center; background: var(--input-bg); padding: 10px 15px; border-radius: 10px; width: 300px; border: 1px solid var(--border-color); }
        .search-bar i { color: var(--text-muted); margin-right: 10px; }
        .search-bar input { background: transparent; border: none; color: var(--text-color); outline: none; width: 100%; }
        .top-nav-right { display: flex; align-items: center; gap: 20px; }
        .icon-btn { background: var(--input-bg); border: 1px solid var(--border-color); color: var(--text-color); width: 40px; height: 40px; border-radius: 10px; cursor: pointer; transition: 0.2s; }
        .icon-btn:hover { background: var(--primary-color); color: white; }
        .user-profile { display: flex; align-items: center; gap: 10px; font-weight: 600; }
        .user-profile img { width: 40px; height: 40px; border-radius: 50%; border: 2px solid var(--primary-color); }
        .page-content { padding: 30px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: var(--card-bg); padding: 20px; border-radius: 15px; border: 1px solid var(--border-color); display: flex; flex-direction: column; gap: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .stat-card .title { font-size: 14px; color: var(--text-muted); }
        .stat-card .value { font-size: 28px; font-weight: 700; }
        .stat-card .trend { font-size: 12px; color: #10b981; }
        .charts-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 30px; }
        .chart-box { background: var(--card-bg); padding: 20px; border-radius: 15px; border: 1px solid var(--border-color); }
        .chart-box h3 { margin-bottom: 15px; font-size: 16px; }
        @media (max-width: 768px) { .sidebar { width: 70px; } .sidebar-header span, .nav-item span { display: none; } .nav-item { justify-content: center; padding: 15px; } .charts-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>

<div class="login-card" id="login-card">
    <div class="logo-section">
        <div class="logo-box"><i class="fa-solid fa-gem"></i></div>
        <div class="theme-switcher">
            <button class="theme-btn" onclick="setTheme('dark')"><i class="fa-solid fa-moon"></i></button>
            <button class="theme-btn" onclick="setTheme('light')"><i class="fa-solid fa-sun"></i></button>
            <button class="theme-btn" onclick="setTheme('auto')"><i class="fa-solid fa-desktop"></i></button>
        </div>
    </div>
    <div class="tabs">
        <div class="tab active" id="tab-login" onclick="switchTab('login')">Login</div>
        <div class="tab" id="tab-register" onclick="switchTab('register')">Register</div>
    </div>
    <form id="login-form" class="login-fields" onsubmit="handleLogin(event)">
        <div class="form-group"><label>Username</label><div class="input-wrapper"><i class="fa-regular fa-user prefix-icon"></i><input type="text" id="login-username" placeholder="Enter username" required></div></div>
        <div class="form-group"><label>Password</label><div class="input-wrapper"><i class="fa-solid fa-lock prefix-icon"></i><input type="password" id="login-password" placeholder="Enter password" required><i class="fa-regular fa-eye eye-icon" onclick="togglePassword('login-password', this)"></i></div></div>
        <div class="checkbox-group"><input type="checkbox" id="remember"><label for="remember">Remember this browser</label></div>
        <button type="submit" class="submit-btn"><i class="fa-solid fa-chevron-right"></i> Enter console</button>
    </form>
    <form id="register-form" class="register-fields" onsubmit="handleRegister(event)">
        <div class="form-group"><label>Username</label><div class="input-wrapper"><i class="fa-regular fa-user prefix-icon"></i><input type="text" id="reg-username" placeholder="Choose username" required></div></div>
        <div class="form-group"><label>Password</label><div class="input-wrapper"><i class="fa-solid fa-lock prefix-icon"></i><input type="password" id="reg-password" placeholder="Create password" required><i class="fa-regular fa-eye eye-icon" onclick="togglePassword('reg-password', this)"></i></div></div>
        <div class="form-group"><label>Referral token (Optional)</label><div class="input-wrapper"><i class="fa-solid fa-key prefix-icon"></i><input type="text" id="reg-referral" placeholder="Enter referral code"></div></div>
        <button type="submit" class="submit-btn"><i class="fa-solid fa-chevron-right"></i> Create account</button>
    </form>
</div>

<div id="dashboard-container">
    <aside class="sidebar">
        <div class="sidebar-header"><i class="fa-solid fa-gem"></i><span>ABDI VIP</span></div>
        <nav class="sidebar-nav">
            <a href="#" class="nav-item active" onclick="loadPage('dashboard', this)"><i class="fa-solid fa-chart-pie"></i> <span>Dashboard</span></a>
            <a href="#" class="nav-item" onclick="loadPage('users', this)"><i class="fa-solid fa-users"></i> <span>Users</span></a>
            <a href="#" class="nav-item" onclick="loadPage('licenses', this)"><i class="fa-solid fa-key"></i> <span>Licenses</span></a>
            <a href="#" class="nav-item" onclick="loadPage('referrals', this)"><i class="fa-solid fa-share-nodes"></i> <span>Referrals</span></a>
            <a href="#" class="nav-item" onclick="loadPage('settings', this)"><i class="fa-solid fa-gear"></i> <span>Settings</span></a>
        </nav>
        <div class="sidebar-footer"><a href="#" class="nav-item" onclick="handleLogout()"><i class="fa-solid fa-right-from-bracket"></i> <span>Logout</span></a></div>
    </aside>
    <main class="main-content">
        <header class="top-nav">
            <div class="search-bar"><i class="fa-solid fa-search"></i><input type="text" placeholder="Search users, licenses..."></div>
            <div class="top-nav-right">
                <button class="icon-btn"><i class="fa-regular fa-bell"></i></button>
                <div class="user-profile"><img src="https://ui-avatars.com/api/?name=Abdi&background=8b5cf6&color=fff" alt="User"><span id="nav-username">Abdi</span></div>
            </div>
        </header>
        <div id="page-content" class="page-content"></div>
    </main>
</div>

<script>
    function switchTab(tab) {
        const loginForm = document.getElementById('login-form');
        const registerForm = document.getElementById('register-form');
        const tabLogin = document.getElementById('tab-login');
        const tabRegister = document.getElementById('tab-register');
        if (tab === 'login') {
            loginForm.classList.remove('hidden'); registerForm.classList.remove('active');
            tabLogin.classList.add('active'); tabRegister.classList.remove('active');
        } else {
            loginForm.classList.add('hidden'); registerForm.classList.add('active');
            tabLogin.classList.remove('active'); tabRegister.classList.add('active');
        }
    }
    function togglePassword(inputId, icon) {
        const input = document.getElementById(inputId);
        if (input.type === 'password') { input.type = 'text'; icon.classList.remove('fa-eye'); icon.classList.add('fa-eye-slash'); }
        else { input.type = 'password'; icon.classList.remove('fa-eye-slash'); icon.classList.add('fa-eye'); }
    }
    function setTheme(theme) {
        const root = document.documentElement;
        const buttons = document.querySelectorAll('.theme-btn');
        buttons.forEach(btn => btn.classList.remove('active'));
        if (theme === 'light') { root.setAttribute('data-theme', 'light'); buttons[1].classList.add('active'); }
        else if (theme === 'dark') { root.removeAttribute('data-theme'); buttons[0].classList.add('active'); }
        else { if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) { root.setAttribute('data-theme', 'light'); } else { root.removeAttribute('data-theme'); } buttons[2].classList.add('active'); }
    }
    async function handleLogin(event) {
        event.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        const btn = event.target.querySelector('button');
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Signing in...'; btn.disabled = true;
        try {
            const response = await fetch('/api/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username, password }) });
            const data = await response.json();
            if (data.success) { localStorage.setItem('token', data.token); showDashboard(); }
            else { alert('Login failed: ' + data.message); btn.innerHTML = '<i class="fa-solid fa-chevron-right"></i> Enter console'; btn.disabled = false; }
        } catch (error) { alert('Server error.'); btn.innerHTML = '<i class="fa-solid fa-chevron-right"></i> Enter console'; btn.disabled = false; }
    }
    async function handleRegister(event) {
        event.preventDefault();
        const username = document.getElementById('reg-username').value;
        const password = document.getElementById('reg-password').value;
        const referral = document.getElementById('reg-referral').value;
        const btn = event.target.querySelector('button');
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Creating...'; btn.disabled = true;
        try {
            const response = await fetch('/api/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username, password, referral }) });
            const data = await response.json();
            if (data.success) { alert('Account created! Please login.'); switchTab('login'); btn.innerHTML = '<i class="fa-solid fa-chevron-right"></i> Create account'; btn.disabled = false; }
            else { alert('Registration failed: ' + data.message); btn.innerHTML = '<i class="fa-solid fa-chevron-right"></i> Create account'; btn.disabled = false; }
        } catch (error) { alert('Server error.'); btn.innerHTML = '<i class="fa-solid fa-chevron-right"></i> Create account'; btn.disabled = false; }
    }
    function showDashboard() {
        document.getElementById('login-card').style.display = 'none';
        document.getElementById('dashboard-container').style.display = 'flex';
        loadPage('dashboard');
    }
    async function loadPage(pageName, element = null) {
        if (element) { document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active')); element.classList.add('active'); }
        const contentArea = document.getElementById('page-content');
        if (pageName === 'dashboard') {
            contentArea.innerHTML = `
                <h1 style="margin-bottom: 20px;">Dashboard Overview</h1>
                <div class="stats-grid" id="stats-grid"><div class="stat-card"><span class="title">Loading...</span></div></div>
                <div class="charts-grid">
                    <div class="chart-box"><h3>Analytics Overview</h3><canvas id="analyticsChart"></canvas></div>
                    <div class="chart-box"><h3>License Status</h3><canvas id="licenseChart"></canvas></div>
                </div>`;
            await fetchStats();
        } else if (pageName === 'users') { contentArea.innerHTML = `<h1>Users Management</h1><p>Liiska isticmaalayaasha halkan ayaa soo baxaya.</p>`; }
        else { contentArea.innerHTML = `<h1>${pageName.charAt(0).toUpperCase() + pageName.slice(1)}</h1><p>Qaybtaan wali lama dhisin.</p>`; }
    }
    async function fetchStats() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/stats', { headers: { 'Authorization': `Bearer ${token}` } });
            const data = await response.json();
            const statsGrid = document.getElementById('stats-grid');
            statsGrid.innerHTML = `
                <div class="stat-card"><span class="title">Total Users</span><span class="value">${data.totalUsers || 0}</span><span class="trend"><i class="fa-solid fa-arrow-up"></i> Live</span></div>
                <div class="stat-card"><span class="title">Total Licenses</span><span class="value">${data.totalLicenses || 0}</span><span class="trend"><i class="fa-solid fa-arrow-up"></i> Live</span></div>
                <div class="stat-card"><span class="title">Used Licenses</span><span class="value">${data.usedLicenses || 0}</span><span class="trend"><i class="fa-solid fa-arrow-up"></i> Live</span></div>
                <div class="stat-card"><span class="title">Referrals</span><span class="value">${data.referrals || 0}</span><span class="trend"><i class="fa-solid fa-arrow-up"></i> Live</span></div>`;
            renderCharts(data);
        } catch (error) { console.error('Error fetching stats:', error); }
    }
    function renderCharts(data) {
        const ctx1 = document.getElementById('analyticsChart').getContext('2d');
        new Chart(ctx1, { type: 'line', data: { labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], datasets: [{ label: 'Active Users', data: [12, 19, 3, 5, 2, 3, 10], borderColor: '#8b5cf6', backgroundColor: 'rgba(139, 92, 246, 0.1)', tension: 0.4, fill: true }] }, options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, grid: { color: '#2a2a35' } }, x: { grid: { display: false } } } } });
        const ctx2 = document.getElementById('licenseChart').getContext('2d');
        new Chart(ctx2, { type: 'doughnut', data: { labels: ['Active', 'Expired', 'Used'], datasets: [{ data: [data.activeLicenses || 10, data.expiredLicenses || 5, data.usedLicenses || 3], backgroundColor: ['#10b981', '#ef4444', '#f59e0b'], borderWidth: 0 }] }, options: { responsive: true, plugins: { legend: { position: 'bottom', labels: { color: '#8b8b9e' } } }, cutout: '70%' } });
    }
    function handleLogout() { localStorage.removeItem('token'); location.reload(); }
    if (localStorage.getItem('token')) { showDashboard(); }
</script>
</body>
</html>"""

# Qor faylka
with open("public/index.html", "w") as f:
    f.write(html_content)

print("✅ Faylka 'public/index.html' si guul leh ayaa loo cusboonaysiiyay!")
