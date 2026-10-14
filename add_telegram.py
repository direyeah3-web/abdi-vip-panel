import shutil

shutil.copy('server.js', 'server.js.backup')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Top — dotenv + telegram + https
old_top = "const express = require('express');"
new_top = """require('dotenv').config();
const express = require('express');
const https = require('https');
const TelegramBot = require('node-telegram-bot-api');"""
if old_top in c:
    c = c.replace(old_top, new_top, 1)
    print("1. Top requires: OK")
else:
    print("1. Top: LAMA HELIN")

# 2. Bot bilow — ka dib DB_FILE
old_db = "const DB_FILE = './abdi.db';"
new_db = """const DB_FILE = './abdi.db';
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_ADMIN_CHAT_ID = process.env.TELEGRAM_ADMIN_CHAT_ID;

// Telegram Bot
let bot = null;
if (TELEGRAM_BOT_TOKEN) {
    bot = new TelegramBot(TELEGRAM_BOT_TOKEN, { polling: false });
    console.log('🤖 Telegram Bot: la diyaariyay');
} else {
    console.log('⚠️  Telegram Bot: TOKEN ma jiro (.env)');
}

// Function: Ogeysiin admin-ka
function sendTelegramNotification(message) {
    if (!bot || !TELEGRAM_ADMIN_CHAT_ID) {
        console.log('⚠️  Telegram: ma dirin (bot ama chat_id ma jiro)');
        return;
    }
    bot.sendMessage(TELEGRAM_ADMIN_CHAT_ID, message, { parse_mode: 'HTML' })
        .then(() => console.log('✅ Telegram: notification la diray'))
        .catch(err => console.error('❌ Telegram error:', err.message));
}"""
if old_db in c:
    c = c.replace(old_db, new_db, 1)
    print("2. Bot bilow: OK")
else:
    print("2. Bot: LAMA HELIN")

# 3. Marka user cusub la abuuro — notification
#    Raadi meesha INSERT users ee register-ka
old_insert = "res.json({ success: true, token, user: {"
if old_insert in c:
    # Ku dar notification ka hor response-ka
    notification = """// Telegram notification — user cusub
        sendTelegramNotification(
            '🆕 <b>User Cusub!</b>\\n\\n' +
            '👤 Username: <b>' + username + '</b>\\n' +
            '🔑 Referral Code: <code>' + (myRef || 'N/A') + '</code>\\n' +
            '👥 Referred By: <b>' + (validReferral ? validReferral.username : 'N/A') + '</b>\\n' +
            '🕐 Waqti: ' + new Date().toLocaleString()
        );
        
        res.json({ success: true, token, user: {"""
    c = c.replace(old_insert, notification, 1)
    print("3. Register notification: OK")
else:
    print("3. Register notification: LAMA HELIN")

# 4. Endpoint cusub — Test Bot
old_listen = "app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"
new_listen = """// Telegram — Test endpoint
app.post('/api/telegram/test', auth, adminOnly, async (req, res) => {
    try {
        if (!bot) {
            return res.status(400).json({ success: false, error: 'Bot ma jiro — .env hubi' });
        }
        if (!TELEGRAM_ADMIN_CHAT_ID) {
            return res.status(400).json({ success: false, error: 'Chat ID ma jiro' });
        }
        const testMsg = '🧪 <b>Test Message</b>\\n\\n✅ Telegram Bot wuu shaqaynayaa!\\n🕐 ' + new Date().toLocaleString();
        await bot.sendMessage(TELEGRAM_ADMIN_CHAT_ID, testMsg, { parse_mode: 'HTML' });
        res.json({ success: true, message: 'Test message la diray!' });
    } catch (err) {
        console.error('Telegram test error:', err);
        res.status(500).json({ success: false, error: err.message });
    }
});

app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"""
if old_listen in c:
    c = c.replace(old_listen, new_listen, 1)
    print("4. Test endpoint: OK")
else:
    print("4. Test endpoint: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup")
