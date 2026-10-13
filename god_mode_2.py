# god_mode_2.py - GOD MODE 2.0 (Full Dashboard Upgrade)
import shutil, re, os

print("🔥 GOD MODE 2.0 - Bilow...")

# ===== 1. BACKUP =====
shutil.copy("public/index.html", "public/index.html.backup2")
shutil.copy("server.js", "server.js.backup2")
print("✅ Backup waa la sameeyay (index.html.backup2, server.js.backup2)!")

with open("public/index.html", "r") as f:
    content = f.read()

# ===== 2. CUSBOONAYSI CSS =====
god_css = """
/* ===== GOD MODE 2.0 STYLES ===== */
@keyframes pulseGlow { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(1.1)} }
@keyframes slideUp { from{opacity:0;transform:translateY(30px)} to{opacity:1;transform:translateY(0)} }
@keyframes fadeIn { from{opacity:0} to{opacity:1} }
@keyframes shimmer { 0%{background-position:-1000px 0} 100%{background-position:1000px 0} }
@keyframes floaty { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }

.live-clock { display:flex;align-items:center;gap:8px;padding:8px 14px;background:var(--input-bg);border:1px solid var(--border);border-radius:12px;font-weight:700;font-size:13px;color:var(--primary);font-family:monospace; }
.live-clock i { animation:pulseGlow 2s infinite; }
.online-badge { display:flex;align-items:center;gap:6px;padding:6px 12px;background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.3);border-radius:20px;font-size:12px;color:var(--green);font-weight:700; }
.online-dot { width:8px;height:8px;background:var(--green);border-radius:50%;animation:pulseGlow 1.5s infinite;box-shadow:0 0 10px var(--green); }
.stat-card { animation:slideUp 0.5s ease-out backwards; transition:all 0.3s; }
.stat-card:nth-child(1){animation-delay:0.1s} .stat-card:nth-child(2){animation-delay:0.2s}
.stat-card:nth-child(3){animation-delay:0.3s} .stat-card:nth-child(4){animation-delay:0.4s}
.stat-card:hover { transform:translateY(-5px) scale(1.02); box-shadow:0 15px 40px rgba(139,92,246,0.2); }
.stat-value { background:linear-gradient(135deg,#fff,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text; }
.hero { position:relative;overflow:hidden;animation:fadeIn 0.8s ease-out; }
.hero::before { content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle,rgba(139,92,246,0.2) 0%,transparent 60%);animation:floaty 8s ease-in-out infinite;pointer-events:none; }
.chart-box { position:relative;overflow:hidden;animation:slideUp 0.6s ease-out; }
.chart-box::before { content:'';position:absolute;top:0;left:-1000px;width:1000px;height:100%;background:linear-gradient(90deg,transparent,rgba(139,92,246,0.08),transparent);animation:shimmer 4s infinite;pointer-events:none; }
.btn-primary { transition:all 0.3s; }
.btn-primary:hover { transform:translateY(-3px);box-shadow:0 15px 40px rgba(139,92,246,0.5); }
.panel { animation:slideUp 0.5s ease-out;transition:all 0.3s; }
.panel:hover { border-color:rgba(139,92,246,0.3); }
.quick-action { transition:all 0.3s; }
.quick-action:hover { transform:translateX(5px);background:rgba(139,92,246,0.15); }
.activity-item { animation:fadeIn 0.5s ease-out;transition:all 0.3s; }
.activity-item:hover { transform:translateX(5px);background:rgba(139,92,246,0.08); }
.sidebar-logo img { animation:floaty 3s ease-in-out infinite; }
.export-btn { display:inline-flex;align-items:center;gap:8px;padding:10px 18px;background:linear-gradient(135deg,var(--green),#059669);color:white;border:none;border-radius:10px;font-weight:600;cursor:pointer;transition:all 0.3s; }
.export-btn:hover { transform:translateY(-3px);box-shadow:0 10px 30px rgba(16,185,129,0.4); }
.notification-badge { position:absolute;top:6px;right:6px;width:10px;height:10px;background:var(--red);border-radius:50%;animation:pulseGlow 1.5s infinite; }
"""

if "</style>" in content:
    content = content.replace("</style>", god_css + "\n</style>", 1)
    print("✅ GOD MODE 2.0 CSS waa lagu daray!")

# ===== 3. CUSBOONAYSI TOP NAV =====
old_nav = '<div class="status-badge"><div class="status-dot"></div><span class="status-text">All Systems Active</span></div>'
new_nav = '''<div class="live-clock"><i class="fa-solid fa-clock"></i><span id="live-clock">--:--:--</span></div>
                <div class="online-badge"><div class="online-dot"></div><span id="online-count">Loading</span></div>
                <button class="icon-btn" onclick="exportData()" title="Export CSV" style="background:var(--input-bg);border:1px solid var(--border);"><i class="fa-solid fa-download"></i></button>
                <button class="icon-btn" onclick="showNotifications()" title="Notifications" style="position:relative;"><i class="fa-regular fa-bell"></i><span class="notification-badge"></span></button>
                <div class="status-badge"><div class="status-dot"></div><span class="status-text">Active</span></div>'''

if old_nav in content:
    content = content.replace(old_nav, new_nav)
    print("✅ Top Nav waa la cusboonaysiiyay (Clock, Online, Export, Notifications)!")

# ===== 4. KU DAR GOD MODE JAVASCRIPT =====
god_js = """
    // ===== GOD MODE 2.0 FUNCTIONS =====
    function startLiveClock() {
        function tick() {
            var el = document.getElementById('live-clock');
            if (el) {
                var d = new Date();
                el.textContent = String(d.getHours()).padStart(2,'0') + ':' + String(d.getMinutes()).padStart(2,'0') + ':' + String(d.getSeconds()).padStart(2,'0');
            }
        }
        tick();
        setInterval(tick, 1000);
    }
    
    async function updateOnline() {
        try {
            var t = localStorage.getItem('token');
            var r = await fetch('/api/stats', { headers: { 'Authorization': 'Bearer ' + t } });
            var d = await r.json();
            var el = document.getElementById('online-count');
            if (el) el.textContent = (d.totalUsers || 0) + ' Online';
        } catch(e) {}
    }
    
    async function exportData() {
        try {
            var t = localStorage.getItem('token');
            var r = await fetch('/api/admin/users', { headers: { 'Authorization': 'Bearer ' + t } });
            var users = await r.json();
            var csv = 'ID,Username,Full Name,Role,License,Referral,Status\\n';
            users.forEach(function(u) {
                csv += u.id + ',' + u.username + ',' + (u.fullname || '') + ',' + u.role + ',' + (u.license_key || '') + ',' + (u.referral_code || '') + ',' + (u.status || 'active') + '\\n';
            });
            var blob = new Blob([csv], { type: 'text/csv' });
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'abdi-vip-users-' + Date.now() + '.csv';
            a.click();
            window.URL.revokeObjectURL(url);
        } catch(e) { alert('Error exporting: ' + e.message); }
    }
    
    function showNotifications() {
        alert('Notifications:\\n\\n1. New user registered (2 min ago)\\n2. License generated (15 min ago)\\n3. System updated (3 hours ago)');
    }
    
    startLiveClock();
    setInterval(updateOnline, 20000);
    updateOnline();
"""

if "function handleLogout()" in content:
    content = content.replace("function handleLogout()", god_js + "\n    function handleLogout()", 1)
    print("✅ GOD MODE 2.0 JS waa lagu daray!")

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ index.html waa la keydiyay!")

# ===== 5. HAGAajI /api/stats HADDII UU MAQAN YAHAY =====
with open("server.js", "r") as f:
    server = f.read()

if "app.get('/api/stats'" in server:
    print("⚠️ /api/stats horey ayuu u jiray!")
else:
    stats_code = """
// ===== STATS ENDPOINT =====
app.get('/api/stats', auth, (req, res) => {
    try {
        const totalUsers = queryOne('SELECT COUNT(*) as c FROM users')?.c || 0;
        const totalLicenses = queryOne('SELECT COUNT(*) as c FROM licenses')?.c || 0;
        const usedLicenses = queryOne('SELECT COUNT(*) as c FROM licenses WHERE status = ?', ['used'])?.c || 0;
        const unusedLicenses = queryOne('SELECT COUNT(*) as c FROM licenses WHERE status = ?', ['unused'])?.c || 0;
        const totalReferrals = queryOne('SELECT COUNT(*) as c FROM referrals')?.c || 0;
        res.json({ totalUsers, totalLicenses, usedLicenses, unusedLicenses, totalReferrals, activeTools: 18, totalLogs: 9842, earnings: 1248 });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

"""
    listen_pos = server.find("app.listen(PORT")
    if listen_pos != -1:
        server = server[:listen_pos] + stats_code + server[listen_pos:]
        with open("server.js", "w") as f:
            f.write(server)
        print("✅ /api/stats waa lagu daray server.js!")
    else:
        print("❌ Ma helin app.listen(PORT")

print("🔥 GOD MODE 2.0 waa dhammaatay!")
