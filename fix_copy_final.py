import shutil

shutil.copy('server.js', 'server.js.backup')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Beddel keyboard-ka — license key laftiisa button ahaan
old_kb = """const keyboard = {
                reply_markup: {
                    inline_keyboard: [
                        [{ text: '📋 COPY CODE', callback_data: 'copy_' + result.key }],
                        [{ text: '📊 STATS', callback_data: 'stats' }]
                    ]
                }
            };"""

new_kb = """const keyboard = {
                reply_markup: {
                    inline_keyboard: [
                        [{ text: '📋 COPY CODE', callback_data: 'copy_' + result.key }]
                    ]
                }
            };"""

if old_kb in c:
    c = c.replace(old_kb, new_kb, 1)
    print("1. Keyboard: OK")
else:
    print("1. Keyboard: LAMA HELIN")

# 2. Beddel callback handler — COPY CODE oo aan fariin cusub soo dirin
old_cb = """if (data.startsWith('copy_')) {
            const key = data.replace('copy_', '');
            bot.answerCallbackQuery(query.id, { text: '✅ Copied: ' + key, show_alert: false });
            bot.sendMessage(chatId, '📋 <b>License Key:</b>\\n<code>' + key + '</code>\\n\\n<i>Taabo code-ka si aad u koobiyo</i>', { parse_mode: 'HTML' });
        } else if (data === 'stats') {"""

new_cb = """if (data.startsWith('copy_')) {
            const key = data.replace('copy_', '');
            bot.answerCallbackQuery(query.id, { text: '✅ ' + key + ' waa la koobiyay!', show_alert: false });
        } else if (data === 'stats') {"""

if old_cb in c:
    c = c.replace(old_cb, new_cb, 1)
    print("2. Callback: OK")
else:
    print("2. Callback: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup")
