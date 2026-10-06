# add_edit_button.py - Ku dar botton Edit qaybta Users

with open("public/index.html", "r") as f:
    content = f.read()

# Beddel loadUsers function si uu u muujiyo botton Edit
old_code = """'<td style="padding: 12px; white-space: nowrap;">' +
                        '<button onclick="deleteUser(' + u.id + ')" style="background: #ef4444; border: none; color: white; padding: 6px 10px; border-radius: 6px; cursor: pointer;">' +
                            '<i class="fa-solid fa-trash"></i>' +
                        '</button>' +
                    '</td>'"""

new_code = """'<td style="padding: 12px; white-space: nowrap;">' +
                        '<button onclick="editUserRole(' + u.id + ', \\'' + u.role + '\\')" style="background: #8b5cf6; border: none; color: white; padding: 6px 10px; border-radius: 6px; cursor: pointer; margin-right: 5px;">' +
                            '<i class="fa-solid fa-pen"></i>' +
                        '</button>' +
                        '<button onclick="deleteUser(' + u.id + ')" style="background: #ef4444; border: none; color: white; padding: 6px 10px; border-radius: 6px; cursor: pointer;">' +
                            '<i class="fa-solid fa-trash"></i>' +
                        '</button>' +
                    '</td>'"""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("✅ Botton Edit waa lagu daray!")
else:
    print("⚠️ Botton Edit lama helin (waa la beddelay horey)")

with open("public/index.html", "w") as f:
    f.write(content)
