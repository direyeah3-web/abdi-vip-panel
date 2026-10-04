# update_version.py - Cusboonaysii appVersion u beddel 4.6.0

with open("server.js", "r") as f:
    content = f.read()

# Beddel appVersion oo dhan
content = content.replace("const appVersion = '4.5';", "const appVersion = '4.6.0';")
content = content.replace("'4.5'", "'4.6.0'")
content = content.replace('"4.5"', '"4.6.0"')

# Beddel version-ka kale
content = content.replace("'7.51.0'", "'4.6.0'")
content = content.replace('"7.51.0"', '"4.6.0"')

with open("server.js", "w") as f:
    f.write(content)

print("✅ appVersion waa la cusboonaysiiyay u beddel 4.6.0!")
