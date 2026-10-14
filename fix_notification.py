import shutil

shutil.copy('server.js', 'server.js.backup')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Meesha saxda ah: ka dib INSERT users, ka hor saveDB
old_code = """[username, hashed, fullname || username, 'user', myRef, validReferral.username]);
        saveDB();"""

new_code = """[username, hashed, fullname || username, 'user', myRef, validReferral.username]);
        saveDB();
        
        // Telegram notification — user cusub
        sendTelegramNotification(
            '🆕 <b>User Cusub!</b>\\n\\n' +
            '👤 Username: <b>' + username + '</b>\\n' +
            '🔑 Referral Code: <code>' + (refCode || 'N/A') + '</code>\\n' +
            '👥 Referred By: <b>' + (validReferral ? validReferral.username : 'N/A') + '</b>\\n' +
            '🕐 Waqti: ' + new Date().toLocaleString()
        );"""

if old_code in c:
    c = c.replace(old_code, new_code, 1)
    print("1. Notification: OK")
else:
    print("1. Notification: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup")
