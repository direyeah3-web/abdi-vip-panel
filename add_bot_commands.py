import shutil

shutil.copy('server.js', 'server.js.backup')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. polling: false → polling: true
old_poll = "bot = new TelegramBot(TELEGRAM_BOT_TOKEN, { polling: false });"
new_poll = "bot = new TelegramBot(TELEGRAM_BOT_TOKEN, { polling: true });"
if old_poll in c:
    c = c.replace(old_poll, new_poll, 1)
    print("1. Polling: OK")
else:
    print("1. Polling: LAMA HELIN")

# 2. Bot commands — ka dib sendTelegramNotification function
old_marker = """// Function: Ogeysiin admin-ka
function sendTelegramNotification(message) {"""
new_marker = """// Function: Admin check
function isAdmin(chatId) {
    return String(chatId) === String(TELEGRAM_ADMIN_CHAT_ID);
}

// Function: Abuur license key
function generateLicenseKey(duration) {
    const key = 'ABDI-' + Math.random().toString(36).substring(2, 8).toUpperCase() +
                Math.random().toString(36).substring(2, 8).toUpperCase();
    const expires = new Date();
    if (duration === '1d') expires.setDate(expires.getDate() + 1);
    else if (duration === '7d') expires.setDate(expires.getDate() + 7);
    else if (duration === '30d') expires.setDate(expires.getDate() + 30);
    else if (duration === '90d') expires.setDate(expires.getDate() + 90);
    else if (duration === '1y') expires.setFullYear(expires.getFullYear() + 1);
    else expires.setDate(expires.getDate() + 30);
    
    try {
        db.run('INSERT INTO licenses (license_key, duration, expires_at, status) VALUES (?, ?, ?, ?)',
            [key, duration, expires.toISOString(), 'available']);
        saveDB();
        return { key, expires: expires.toISOString(), duration };
    } catch (err) {
        console.error('License error:', err);
        return null;
    }
}

// Function: Ogeysiin admin-ka
function sendTelegramNotification(message) {"""
if old_marker in c:
    c = c.replace(old_marker, new_marker, 1)
    print("2. Functions: OK")
else:
    print("2. Functions: LAMA HELIN")

# 3. Bot handlers — ka hor app.listen
old_listen = "app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"
new_listen = """// ===== TELEGRAM BOT HANDLERS =====
if (bot) {
    // /start
    bot.onText(/\\/start/, (msg) => {
        const chatId = msg.chat.id;
        if (isAdmin(chatId)) {
            bot.sendMessage(chatId,
                '👋 <b>Welcome Admin!</b>\\n\\n' +
                '📋 <b>Commands-ka la heli karo:</b>\\n\\n' +
                '/gen &lt;duration&gt; — Abuur license key\\n' +
                '   • 1d = 1 maalin\\n' +
                '   • 7d = 7 maalin\\n' +
                '   • 30d = 30 maalin\\n' +
                '   • 90d = 90 maalin\\n' +
                '   • 1y = 1 sano\\n\\n' +
                '/stats — Xogta panel-ka\\n' +
                '/help — Caawimaad',
                { parse_mode: 'HTML' }
            );
        } else {
            bot.sendMessage(chatId, '⛔ Kaliya admin-ka ayaa isticmaali kara bot-kan.');
        }
    });

    // /help
    bot.onText(/\\/help/, (msg) => {
        const chatId = msg.chat.id;
        if (!isAdmin(chatId)) {
            bot.sendMessage(chatId, '⛔ Kaliya admin-ka.');
            return;
        }
        bot.sendMessage(chatId,
            '📋 <b>License Generator Commands:</b>\\n\\n' +
            '<code>/gen 1d</code> — 1 maalin\\n' +
            '<code>/gen 7d</code> — 7 maalin\\n' +
            '<code>/gen 30d</code> — 30 maalin\\n' +
            '<code>/gen 90d</code> — 90 maalin\\n' +
            '<code>/gen 1y</code> — 1 sano\\n\\n' +
            '/stats — Xogta panel-ka',
            { parse_mode: 'HTML' }
        );
    });

    // /stats
    bot.onText(/\\/stats/, (msg) => {
        const chatId = msg.chat.id;
        if (!isAdmin(chatId)) {
            bot.sendMessage(chatId, '⛔ Kaliya admin-ka.');
            return;
        }
        try {
            const users = queryOne('SELECT COUNT(*) as c FROM users');
            const licenses = queryOne('SELECT COUNT(*) as c FROM licenses');
            const available = queryOne("SELECT COUNT(*) as c FROM licenses WHERE status = 'available'");
            const referrals = queryOne('SELECT COUNT(*) as c FROM referrals');
            bot.sendMessage(chatId,
                '📊 <b>ABDI VIP PANEL — Stats</b>\\n\\n' +
                '👥 Users: <b>' + (users ? users.c : 0) + '</b>\\n' +
                '🔑 Licenses: <b>' + (licenses ? licenses.c : 0) + '</b>\\n' +
                '✅ Available: <b>' + (available ? available.c : 0) + '</b>\\n' +
                '🎯 Referrals: <b>' + (referrals ? referrals.c : 0) + '</b>',
                { parse_mode: 'HTML' }
            );
        } catch (err) {
            bot.sendMessage(chatId, '❌ Error: ' + err.message);
        }
    });

    // /gen
    bot.onText(/\\/gen(?:\\s+(.+))?/, (msg, match) => {
        const chatId = msg.chat.id;
        if (!isAdmin(chatId)) {
            bot.sendMessage(chatId, '⛔ Kaliya admin-ka ayaa license abuuri kara.');
            return;
        }
        const duration = (match[1] || '30d').trim().toLowerCase();
        const validDurations = ['1d', '7d', '30d', '90d', '1y'];
        if (!validDurations.includes(duration)) {
            bot.sendMessage(chatId,
                '⚠️ Duration khaldan!\\n\\nIsticmaal: <code>/gen 30d</code>\\n\\n' +
                'Doorashooyin: 1d, 7d, 30d, 90d, 1y',
                { parse_mode: 'HTML' }
            );
            return;
        }
        const result = generateLicenseKey(duration);
        if (result) {
            bot.sendMessage(chatId,
                '✅ <b>License Key la abuuray!</b>\\n\\n' +
                '🔑 <code>' + result.key + '</code>\\n' +
                '⏱️ Duration: <b>' + result.duration + '</b>\\n' +
                '📅 Expires: <b>' + new Date(result.expires).toLocaleString() + '</b>',
                { parse_mode: 'HTML' }
            );
        } else {
            bot.sendMessage(chatId, '❌ License abuurista waa guuldareysatay.');
        }
    });

    console.log('🤖 Telegram Bot: handlers la diyaariyay');
}

app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"""
if old_listen in c:
    c = c.replace(old_listen, new_listen, 1)
    print("3. Bot handlers: OK")
else:
    print("3. Bot handlers: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup")
