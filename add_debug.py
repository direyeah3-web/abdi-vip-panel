# add_debug.py - Ku dar debug showDashboard

with open("public/index.html", "r") as f:
    content = f.read()

old_code = "function showDashboard(){document.getElementById('login').style.display='none';document.getElementById('dashboard').style.display='block';"

new_code = "function showDashboard(){alert('showDashboard waa la wacay!');document.getElementById('login').style.display='none';document.getElementById('dashboard').style.display='block';"

if old_code in content:
    content = content.replace(old_code, new_code)
    with open("public/index.html", "w") as f:
        f.write(content)
    print("✅ Debug showDashboard waa lagu daray!")
else:
    print("⚠️ Code-ka lama helin")
