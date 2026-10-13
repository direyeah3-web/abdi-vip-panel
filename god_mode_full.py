# god_mode_full.py - GOD MODE Full Dashboard Upgrade
import shutil, re, os

print("🔥 GOD MODE - Bilow...")

# 1. BACKUP
shutil.copy("public/index.html", "public/index.html.backup")
shutil.copy("server.js", "server.js.backup")
print("✅ Backup waa la sameeyay!")

with open("public/index.html", "r") as f:
    content = f.read()

# 2. CUSBOONAYSI CSS (beddel </style> oo dhan)
god_css = """
/* ===== GOD MODE STYLES ===== */
@keyframes pulseGlow { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(1.1)} }
@keyframes slideUp { from{opacity:0;transform:translateY(30px)} to{opacity:1;transform:translateY(0)} }
@keyframes shimmer { 0%{background-position:-1000px 0} 100%{background-position:1000px 0} }
@keyframes floaty { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
@keyframes spin { from{transform:rotate(0)} to{transform:rotate(360deg)} }
@keyframes fadeIn { from{opacity:0} to{opacity:1} }

body { background: linear-gradient(135deg,#0a0a0f 0%,#12121a 50%,#0a0a0f 100%) !important; }

.live-clock { display:flex;align-items:center;gap:8px;padding:8px 14px;background:var(--input-bg);border:1px solid var(--border);border-radius:12px;font-weight:700;font-size:13px;color:var(--primary);font-family:monospace; }
.live-clock i { animation:pulseGlow 2s infinite; }
.online-badge { display:flex;align-items:center;gap:6px;padding:6px 12px;background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.3);border-radius:20px;font-size:12px;color:var(--green);font-weight:700; }
.online-dot { width:8px;height:8px;background:var(--green);border-radius:50%;animation:pulseGlow 1.5s infinite;box-shadow:0 0 10px var(--green); }
.stat-card { animation:slideUp 0.5s ease-out backwards; }
.stat-card:nth-child(1){animation-delay:0.1s} .stat-card:nth-child(2){animation-delay:0.2s}
.stat-card:nth-child(3){animation-delay:0.3s} .stat-card:nth-child(4){animation-delay:0.4s}
.stat-card:hover { transform:translateY(-5px) scale(1.02); box-shadow:0 15px 40px rgba(139,92,246,0.2); }
.stat-value { background:linear-gradient(135deg,#fff,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text; }
.hero { position:relative;overflow:hidden;animation:fadeIn 0.8s ease-out; }
.hero::before { content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle,rgba(139,92,246,0.2) 0%,transparent 60%);animation:floaty 8s ease-in-out infinite;pointer-events:none; }
.hero h1 { position:relative;z-index:1; }
.chart-box { position:relative;overflow:hidden;animation:slideUp 0.6s ease-out; }
.chart-box::before { content:'';position:absolute;top:0;left:-1000px;width:1000px;height:100%;background:linear-gradient(90deg,transparent,rgba(139,92,246,0.08),transparent);animation:shimmer 4s infinite;pointer-events:none; }
.btn-primary { position:relative;overflow:hidden;transition:all 0.3s; }
.btn-primary:hover { transform:translateY(-3px);box-shadow:0 15px 40px rgba(139,92,246,0.5); }
.panel { animation:slideUp 0.5s ease-out;transition:all 0.3s; }
.panel:hover { border-color:rgba(139,92,246,0.3); }
.quick-action { transition:all 0.3s; }
.quick-action:hover { transform:translateX(5px);background:rgba(139,92,246,0.15); }
.activity-item { animation:fadeIn 0.5s ease-out;transition:all 0.3s; }
.activity-item:hover { transform:translateX(5px);background:rgba(139,92,246,0.08); }
.sidebar-logo img { animation:floaty 3s ease-in-out infinite; }
"""

# Beddel CSS-ka hore (ka hor </style>)
if "</style>" in content:
    content = content.replace("</style>", god_css + "\n</style>", 1)
    print("✅ GOD MODE CSS waa lagu daray!")

# 3. CUSBOONAYSI TOP NAV (ku dar Live Clock iyo Online Badge)
old_nav = '<div class="status-badge"><div class="status-dot"></div><span class="status-text">All Systems Active</span></div>'
new_nav = '''<div class="live-clock"><i class="fa-solid fa-clock"></i><span id="live-clock">--:--:--</span></div>
                <div class="online-badge"><div class="online-dot"></div><span id="online-count">Loading</span></div>
                <div class="status-badge"><div class="status-dot"></div><span class="status-text">Active</span></div>'''

if old_nav in content:
    content = content.replace(old_nav, new_nav)
    print("✅ Live Clock iyo Online Badge waa lagu daray!")
else:
    print("⚠️ Top nav lama helin")

# 4. KU DAR GOD MODE JAVASCRIPT
god_js = """
    // ===== GOD MODE JAVASCRIPT =====
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
    
    function animateValue(el, target, duration) {
        if (!el) return;
        var start = 0, startTime = null;
        function step(ts) {
            if (!startTime) startTime = ts;
            var progress = Math.min((ts - startTime) / duration, 1);
            el.textContent = Math.floor(progress * (target - start) + start);
            if (progress < 1) requestAnimationFrame(step);
            else el.textContent = target;
        }
        requestAnimationFrame(step);
    }
    
    startLiveClock();
    setInterval(updateOnline, 20000);
    updateOnline();
"""

if "function handleLogout()" in content:
    content = content.replace("function handleLogout()", god_js + "\n    function handleLogout()", 1)
    print("✅ GOD MODE JS waa lagu daray!")
else:
    print("⚠️ handleLogout lama helin")

# 5. KEYDI
with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
print("🔥 GOD MODE waa dhammaatay!")
