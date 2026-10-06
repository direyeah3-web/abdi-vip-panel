# add_edit_button_final.py - Ku dar botton Edit si sax ah

with open("public/index.html", "r") as f:
    content = f.read()

# Beddelka: Ku dar botton Edit ka hor botton Delete
old_code = """'<td><button onclick="deleteUser('+x.id+')""""
new_code = """'<td><button onclick="editUserRole('+x.id+', \\''+x.role+'\\')" style="background:#8b5cf6;border:none;color:white;padding:6px 12px;border-radius:8px;cursor:pointer;margin-right:5px;"><i class="fa-solid fa-pen"></i></button><button onclick="deleteUser('+x.id+')""""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("✅ Botton Edit waa lagu daray!")
else:
    print("⚠️ Botton Edit lama helin — isku day qaab kale")

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
