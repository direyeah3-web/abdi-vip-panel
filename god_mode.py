# god_mode.py - GOD MODE Dashboard Upgrade (Safe Version)
import shutil, re, os

# 1. BACKUP - Horey u keydi
shutil.copy("public/index.html", "public/index.html.backup")
shutil.copy("server.js", "server.js.backup")
print("✅ Backup waa la sameeyay!")

with open("public/index.html", "r") as f:
    content = f.read()

# 2. KU DAR CSS CUSUB (ka hor </style>)
god_css = """
@keyframes pulse-glow { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.6;transform:scale(1.05)} }
@keyframes slide-up { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
@keyframes shimmer { 0%{background-position:-500px 0} 100%{background-position:500px 0} }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-5px)} }
.live-clock { display:flex; align-items:center; gap:10px; padding:8px 16px; background:var(--input-bg); border:1px solid var(--border); border-radius:12px; font-weight:600; font-size:14px; }
.live-clock i { color:var(--primary); animation:pulse-glow 2s infinite; }
.online-badge { display:flex; align-items:center; gap:6px; padding:6px 12px; background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.3); border-radius:20px; font-size:12px; color:var(--green); font-weight:600; }
.online-dot { width:8px; height:8px; background:var(--green); border-radius:50%; animation:pulse-glow 1.5s infinite; }
.stat-card-animated { animation:slide-up 0.5s ease-out; }
.hero { position:relative; overflow:hidden; }
.hero::before { content:''; position:absolute; top:-50%; left:-50%; width:200%; height:200%; background:radial-gradient(circle,rgba(139,92,246,0.15) 0%,transparent 70%); animation:float 6s ease-in-out infinite; pointer-events:none; }
.icon-btn { position:relative; }
.icon-btn .badge { position:absolute; top:5px; right:5px; width:8px; height:8px; background:var(--red); border-radius:50%; animation:pulse-glow 1s infinite; }
.chart-box { position:relative; overflow:hidden; }
.chart-box::after { content:''; position:absolute; top:0; left:-500px; width:500px; height:100%; background:linear-gradient(90deg,transparent,rgba(139,92,246,0.1),transparent); animation:shimmer 3s infinite; }
"""

content = content.replace("</style>", god_css + "\n</style>")

# 3. KU DAR LIVE CLOCK IYO ONLINE BADGE (ka hor status-badge)
old_topnav_right = '<div class="status-badge"><div class="status-dot"></div><span class="status-text">All Systems Active</span></div>'
new_topnav_right = '''<div class="live-clock"><i class="fa-solid fa-clock"></i><span id="live-clock-text">--:--:--</span></div>
                <div class="online-badge"><div class="online-dot"></div><span id="online-count">0 Online</span></div>
                <div class="status-badge"><div class="status-dot"></div><span class="status-text">All Systems Active</span></div>'''

if old_topnav_right in content:
    content = content.replace(old_topnav_right, new_topnav_right)
    print("✅ Live Clock iyo Online Badge waa lagu daray!")
else:
    print("⚠️ Top Nav lama helin - isku day qaab kale")

# 4. KU DAR GOD MODE FUNCTIONS (ka hor function handleLogout)
god_js = """
    // ===== GOD MODE FEATURES =====
    function startLiveClock() {
        function update() {
            var el = document.getElementById('live-clock-text');
            if (el) {
                var now = new Date();
                var h = String(now.getHours()).padStart(2,'0');
                var m = String(now.getMinutes()).padStart(2,'0');
                var s = String(now.getSeconds()).padStart(2,'0');
                el.textContent = h + ':' + m + ':' + s;
            }
        }
        update();
        setInterval(update, 1000);
    }
    
    async function updateOnlineCount() {
        try {
            var token = localStorage.getItem('token');
            var r = await fetch('/api/stats', { headers: { 'Authorization': 'Bearer ' + token } });
            var d = await r.json();
            var el = document.getElementById('online-count');
            if (el) el.textContent = (d.totalUsers || 0) + ' Online';
        } catch(e) {}
    }
    
    function animateNumber(el, target) {
        var current = 0;
        var step = Math.max(1, Math.ceil(target / 30));
        var timer = setInterval(function() {
            current += step;
            if (current >= target) { current = target; clearInterval(timer); }
            el.textContent = current;
        }, 30);
    }
    
    startLiveClock();
    setInterval(updateOnlineCount, 30000);
    updateOnlineCount();
"""

if "function handleLogout()" in content:
    content = content.replace("function handleLogout()", god_js + "\n    function handleLogout()")
    print("✅ GOD MODE Functions waa lagu daray!")
else:
    print("⚠️ handleLogout lama helin")

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay! GOD MODE waa diyaar!")
