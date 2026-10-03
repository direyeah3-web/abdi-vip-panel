# fix_mobile.py - Hagaaji mobile responsive

with open("public/index.html", "r") as f:
    content = f.read()

# Beddel media query-ga hore
old_media = '''@media(max-width:768px){.sidebar{width:70px;}.sidebar-brand,.nav-item span,.nav-section,.user-info{display:none;}.nav-item{justify-content:center;}.main{margin-left:70px;}.content-grid{grid-template-columns:1fr;}.search-bar{width:200px;}}'''

new_media = '''@media(max-width:768px){
    .sidebar{width:240px;transform:translateX(-100%);transition:transform .3s;z-index:200;}
    .sidebar.open{transform:translateX(0);}
    .sidebar-brand,.nav-item span,.nav-section,.user-info{display:block;}
    .nav-item{justify-content:flex-start;}
    .main{margin-left:0;}
    .content-grid{grid-template-columns:1fr;}
    .stats-grid{grid-template-columns:1fr 1fr;}
    .search-bar{width:100%;}
    .topnav{padding:12px 15px;flex-wrap:wrap;gap:10px;}
    .topnav .search-bar{width:100%;order:3;margin-top:5px;}
    .hero{padding:25px;}
    .hero h1{font-size:24px;}
    .hero p{font-size:14px;}
    .hero-buttons{flex-direction:column;}
    .hero-buttons button{width:100%;justify-content:center;}
    .page{padding:15px;}
    .panel{padding:18px;}
    .stat-value{font-size:26px;}
    .menu-toggle{display:flex !important;}
    .mobile-overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.5);z-index:150;}
    .mobile-overlay.show{display:block;}
    .status-badge{padding:6px 10px;font-size:11px;}
    .status-text{display:none;}
    .duration-grid{grid-template-columns:1fr 1fr;}
}
.menu-toggle{display:none;background:var(--card);border:1px solid var(--border);color:var(--text);width:40px;height:40px;border-radius:10px;cursor:pointer;align-items:center;justify-content:center;font-size:16px;}'''

content = content.replace(old_media, new_media)

# Ku dar menu-toggle button gudaha topnav
old_topnav = '''<header class="topnav">
<div class="search-bar"><i class="fa-solid fa-search"></i><input type="text" placeholder="Search apps, workflows, agents..."></div>
<div style="display:flex;align-items:center;gap:15px;">
<div class="status-badge"><div class="status-dot"></div> All Systems Active</div>
<button class="submit-btn" style="width:auto;padding:10px 14px;margin:0;" onclick="handleLogout()"><i class="fa-solid fa-right-from-bracket"></i></button>
</div>
</header>'''

new_topnav = '''<header class="topnav">
<button class="menu-toggle" onclick="toggleSidebar()"><i class="fa-solid fa-bars"></i></button>
<div class="search-bar"><i class="fa-solid fa-search"></i><input type="text" placeholder="Search..."></div>
<div style="display:flex;align-items:center;gap:10px;">
<div class="status-badge"><div class="status-dot"></div><span class="status-text">All Systems Active</span></div>
<button class="submit-btn" style="width:auto;padding:10px 14px;margin:0;" onclick="handleLogout()"><i class="fa-solid fa-right-from-bracket"></i></button>
</div>
</header>'''

content = content.replace(old_topnav, new_topnav)

# Ku dar overlay ka hor sidebar
content = content.replace(
    '<aside class="sidebar">',
    '<div class="mobile-overlay" id="mobile-overlay" onclick="toggleSidebar()"></div>\n<aside class="sidebar" id="sidebar">'
)

# Ku dar toggleSidebar function
toggle_func = '''
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
    document.getElementById('mobile-overlay').classList.toggle('show');
}
'''
content = content.replace(
    'function handleLogout()',
    toggle_func + '\nfunction handleLogout()'
)

with open("public/index.html", "w") as f:
    f.write(content)

print("✅ Mobile responsive waa la hagaajiyay!")
