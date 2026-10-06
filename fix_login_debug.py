# fix_login_debug.py - Ku dar fariin cad login-ka

with open("public/index.html", "r") as f:
    content = f.read()

# Beddelka handleLogin si uu u muujiyo response-ka
old_code = "if(d.success||d.token){localStorage.setItem('token',d.token);localStorage.setItem('user',JSON.stringify(d.user||{}));showDashboard();}else{alert('Login failed: '+(d.message||d.error||'Invalid'));"

new_code = "alert('Response: '+JSON.stringify(d));if(d.success||d.token){localStorage.setItem('token',d.token);localStorage.setItem('user',JSON.stringify(d.user||{}));showDashboard();}else{alert('Login failed: '+(d.message||d.error||'Invalid'));"

if old_code in content:
    content = content.replace(old_code, new_code)
    with open("public/index.html", "w") as f:
        f.write(content)
    print("✅ Debug-ka login-ka waa lagu daray!")
else:
    print("⚠️ Code-ka lama helin — isku day qaab kale")
