import shutil

shutil.copy('server.js', 'server.js.backup')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Beddel keyboard — copy_text button
old_kb = """const keyboard = {
                reply_markup: {
                    inline_keyboard: [
                        [{ text: '📋 COPY CODE', callback_data: 'copy_' + result.key }]
                    ]
                }
            };"""

new_kb = """const keyboard = {
                reply_markup: {
                    inline_keyboard: [
                        [{ text: '📋 COPY CODE', copy_text: { text: result.key } }]
                    ]
                }
            };"""

if old_kb in c:
    c = c.replace(old_kb, new_kb, 1)
    print("1. Keyboard copy_text: OK")
else:
    print("1. Keyboard: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup")
