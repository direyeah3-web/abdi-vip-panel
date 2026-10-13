# add_logo.py - Ku dar logo-ga sawirkaaga

with open("public/index.html", "r") as f:
    content = f.read()

# 1. Beddel logo-ga Login-ka
old_login_logo = '<div class="login-logo"><i class="fa-solid fa-shield-halved"></i></div>'
new_login_logo = '<div class="login-logo"><img src="/logo.png" alt="Logo" style="width:100%;height:100%;object-fit:cover;border-radius:18px;"></div>'

if old_login_logo in content:
    content = content.replace(old_login_logo, new_login_logo)
    print("✅ Logo-ga Login-ka waa la beddelay!")
else:
    print("⚠️ Logo-ga Login-ka lama helin")

# 2. Beddel logo-ga Sidebar
old_sidebar_logo = '<div class="sidebar-logo">AV</div>'
new_sidebar_logo = '<div class="sidebar-logo"><img src="/logo.png" alt="Logo" style="width:100%;height:100%;object-fit:cover;border-radius:10px;"></div>'

if old_sidebar_logo in content:
    content = content.replace(old_sidebar_logo, new_sidebar_logo)
    print("✅ Logo-ga Sidebar waa la beddelay!")
else:
    print("⚠️ Logo-ga Sidebar lama helin")

# 3. Beddel magaca Panel-ka
old_brand = '<div class="sidebar-brand">ABDI VIP<small>Autonomous Panel</small></div>'
new_brand = '<div class="sidebar-brand">ABDI VIP<small>Autonomous Panel</small></div>'

if old_brand in content:
    content = content.replace(old_brand, new_brand)
    print("✅ Magaca Panel-ka wuu saxan yahay!")

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
