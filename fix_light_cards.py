import shutil

shutil.copy('public/index.html', 'public/index.html.backup')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Cards-ka light — transparent si sawirka uga muuqdo
old_cards = '[data-theme="light"] .card,[data-theme="light"] .stat-card,[data-theme="light"] .panel,[data-theme="light"] .hero{background:linear-gradient(135deg,#142a42,#0f2236) !important;border:1px solid #1e3a5f !important;box-shadow:0 4px 20px rgba(0,212,255,0.1) !important;}'
new_cards = '[data-theme="light"] .card,[data-theme="light"] .stat-card,[data-theme="light"] .panel,[data-theme="light"] .hero{background:rgba(0,0,0,0.55) !important;border:1px solid rgba(255,255,255,0.15) !important;box-shadow:0 4px 20px rgba(0,0,0,0.3) !important;backdrop-filter:blur(12px);}'
if old_cards in c:
    c = c.replace(old_cards, new_cards, 1)
    print("1. Cards: OK")
else:
    print("1. Cards: LAMA HELIN")

# Inputs-ka light — transparent
old_inputs = '[data-theme="light"] input,[data-theme="light"] select{background:#0d1b2a !important;border:1px solid #1e3a5f !important;color:#e6f1ff !important;}'
new_inputs = '[data-theme="light"] input,[data-theme="light"] select{background:rgba(0,0,0,0.5) !important;border:1px solid rgba(255,255,255,0.15) !important;color:#fff !important;backdrop-filter:blur(8px);}'
if old_inputs in c:
    c = c.replace(old_inputs, new_inputs, 1)
    print("2. Inputs: OK")
else:
    print("2. Inputs: LAMA HELIN")

# Chart box light — transparent
old_chart = '[data-theme="light"] .chart-box{background:linear-gradient(135deg,#142a42,#0f2236) !important;}'
new_chart = '[data-theme="light"] .chart-box{background:rgba(0,0,0,0.5) !important;backdrop-filter:blur(12px);}'
if old_chart in c:
    c = c.replace(old_chart, new_chart, 1)
    print("3. Chart: OK")
else:
    print("3. Chart: LAMA HELIN")

# Toast light — transparent
old_toast = '[data-theme="light"] .toast{background:linear-gradient(135deg,#142a42,#0f2236) !important;border:1px solid #1e3a5f !important;}'
new_toast = '[data-theme="light"] .toast{background:rgba(0,0,0,0.75) !important;border:1px solid rgba(255,255,255,0.15) !important;backdrop-filter:blur(15px);}'
if old_toast in c:
    c = c.replace(old_toast, new_toast, 1)
    print("4. Toast: OK")
else:
    print("4. Toast: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup")
