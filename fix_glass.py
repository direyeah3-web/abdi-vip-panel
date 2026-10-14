import shutil

shutil.copy('public/index.html', 'public/index.html.backup')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Cards — glass casri
old = '[data-theme="light"] .card,[data-theme="light"] .stat-card,[data-theme="light"] .panel,[data-theme="light"] .hero{background:rgba(0,0,0,0.55) !important;border:1px solid rgba(255,255,255,0.15) !important;box-shadow:0 4px 20px rgba(0,0,0,0.3) !important;backdrop-filter:blur(12px);}'
new = '[data-theme="light"] .card,[data-theme="light"] .stat-card,[data-theme="light"] .panel,[data-theme="light"] .hero{background:rgba(255,255,255,0.08) !important;border:1px solid rgba(255,255,255,0.18) !important;box-shadow:0 8px 32px rgba(0,0,0,0.35),inset 0 1px 0 rgba(255,255,255,0.1) !important;backdrop-filter:blur(20px) saturate(180%);-webkit-backdrop-filter:blur(20px) saturate(180%);}'
if old in c:
    c = c.replace(old, new, 1)
    print("1. Cards glass: OK")
else:
    print("1. Cards: LAMA HELIN")

# 2. Inputs — glass
old = '[data-theme="light"] input,[data-theme="light"] select{background:rgba(0,0,0,0.5) !important;border:1px solid rgba(255,255,255,0.15) !important;color:#fff !important;backdrop-filter:blur(8px);}'
new = '[data-theme="light"] input,[data-theme="light"] select{background:rgba(255,255,255,0.1) !important;border:1px solid rgba(255,255,255,0.2) !important;color:#fff !important;backdrop-filter:blur(10px);}'
if old in c:
    c = c.replace(old, new, 1)
    print("2. Inputs glass: OK")
else:
    print("2. Inputs: LAMA HELIN")

# 3. Quick action — glass
old = '[data-theme="light"] .quick-action{background:#0d1b2a !important;border:1px solid #1e3a5f;}'
new = '[data-theme="light"] .quick-action{background:rgba(255,255,255,0.08) !important;border:1px solid rgba(255,255,255,0.15);backdrop-filter:blur(15px);}'
if old in c:
    c = c.replace(old, new, 1)
    print("3. Quick action: OK")
else:
    print("3. Quick action: LAMA HELIN")

# 4. Quick action hover
old = '[data-theme="light"] .quick-action:hover{background:#1a3554 !important;border-color:#00d4ff !important;}'
new = '[data-theme="light"] .quick-action:hover{background:rgba(0,212,255,0.15) !important;border-color:#00d4ff !important;}'
if old in c:
    c = c.replace(old, new, 1)
    print("4. Quick hover: OK")
else:
    print("4. Quick hover: LAMA HELIN")

# 5. Chart box — glass
old = '[data-theme="light"] .chart-box{background:rgba(0,0,0,0.5) !important;backdrop-filter:blur(12px);}'
new = '[data-theme="light"] .chart-box{background:rgba(255,255,255,0.08) !important;backdrop-filter:blur(20px) saturate(180%);border:1px solid rgba(255,255,255,0.18) !important;}'
if old in c:
    c = c.replace(old, new, 1)
    print("5. Chart glass: OK")
else:
    print("5. Chart: LAMA HELIN")

# 6. Toast — glass
old = '[data-theme="light"] .toast{background:rgba(0,0,0,0.75) !important;border:1px solid rgba(255,255,255,0.15) !important;backdrop-filter:blur(15px);}'
new = '[data-theme="light"] .toast{background:rgba(255,255,255,0.12) !important;border:1px solid rgba(255,255,255,0.25) !important;backdrop-filter:blur(25px) saturate(180%);}'
if old in c:
    c = c.replace(old, new, 1)
    print("6. Toast glass: OK")
else:
    print("6. Toast: LAMA HELIN")

# 7. Sidebar — glass
old = '[data-theme="light"] .sidebar{background:rgba(15,34,54,0.75) !important;border-right:1px solid #1e3a5f;backdrop-filter:blur(15px);}'
new = '[data-theme="light"] .sidebar{background:rgba(255,255,255,0.06) !important;border-right:1px solid rgba(255,255,255,0.12);backdrop-filter:blur(25px) saturate(180%);}'
if old in c:
    c = c.replace(old, new, 1)
    print("7. Sidebar glass: OK")
else:
    print("7. Sidebar: LAMA HELIN")

# 8. Topnav — glass
old = '[data-theme="light"] .topnav{background:rgba(255,255,255,0.7) !important;border-bottom:1px solid var(--border);backdrop-filter:blur(15px);}'
new = '[data-theme="light"] .topnav{background:rgba(255,255,255,0.06) !important;border-bottom:1px solid rgba(255,255,255,0.12);backdrop-filter:blur(25px) saturate(180%);}'
if old in c:
    c = c.replace(old, new, 1)
    print("8. Topnav glass: OK")
else:
    print("8. Topnav: LAMA HELIN")

# 9. Nav-item hover/active — glass
old = '[data-theme="light"] .nav-item:hover,[data-theme="light"] .nav-item.active{background:linear-gradient(135deg,rgba(0,212,255,0.15),rgba(139,92,246,0.15)) !important;color:#00d4ff !important;}'
new = '[data-theme="light"] .nav-item:hover,[data-theme="light"] .nav-item.active{background:rgba(0,212,255,0.2) !important;color:#00d4ff !important;backdrop-filter:blur(10px);}'
if old in c:
    c = c.replace(old, new, 1)
    print("9. Nav glass: OK")
else:
    print("9. Nav: LAMA HELIN")

# 10. Theme-btn active — glass
old = '[data-theme="light"] .theme-btn.active{background:#00d4ff !important;color:#0d1b2a !important;}'
new = '[data-theme="light"] .theme-btn.active{background:rgba(0,212,255,0.8) !important;color:#0d1b2a !important;backdrop-filter:blur(10px);}'
if old in c:
    c = c.replace(old, new, 1)
    print("10. Theme-btn glass: OK")
else:
    print("10. Theme-btn: LAMA HELIN")

# 11. Icon-btn — glass
old = '[data-theme="light"] .icon-btn{background:#142a42 !important;border:1px solid #1e3a5f !important;color:#e6f1ff !important;}'
new = '[data-theme="light"] .icon-btn{background:rgba(255,255,255,0.1) !important;border:1px solid rgba(255,255,255,0.2) !important;color:#fff !important;backdrop-filter:blur(10px);}'
if old in c:
    c = c.replace(old, new, 1)
    print("11. Icon-btn glass: OK")
else:
    print("11. Icon-btn: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup")
