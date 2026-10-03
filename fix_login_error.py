# Faylkan wuxuu hagaajinayaa dhibaatada "Login failed: undefined"
# Wuxuu bedelaa data.message oo u beddelaa data.message || data.error

import re

# Akhri faylka index.html
with open("public/index.html", "r") as f:
    content = f.read()

# Beddelka 1: Hagaaji fariinta login-ka
old_login = "alert('Login failed: ' + data.message);"
new_login = "alert('Login failed: ' + (data.message || data.error || 'Invalid credentials'));"

if old_login in content:
    content = content.replace(old_login, new_login)
    print("✅ Login error message fixed!")
else:
    print("⚠️ Login error message not found (maybe already fixed)")

# Beddelka 2: Hagaaji fariinta register-ka
old_reg = "alert('Registration failed: ' + data.message);"
new_reg = "alert('Registration failed: ' + (data.message || data.error || 'Registration failed'));"

if old_reg in content:
    content = content.replace(old_reg, new_reg)
    print("✅ Register error message fixed!")
else:
    print("⚠️ Register error message not found (maybe already fixed)")

# Qor faylka
with open("public/index.html", "w") as f:
    f.write(content)

print("✅ Faylka 'public/index.html' si guul leh ayaa loo cusboonaysiiyay!")
