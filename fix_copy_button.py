import shutil

shutil.copy('server.js', 'server.js.backup')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Fariinta /gen — ku dar inline keyboard COPY CODE
old_msg = """bot.sendMessage(chatId,
                '<b>╔══════════════════════════╗</b>\\n' +
                '<b>║   ✅ LICENSE KEY LA ABUURAY   ║</b>\\n' +
                '<b>╚══════════════════════════╝</b>\\n\\n' +
                '🔑 <b>License Key:</b>\\n' +
                '<code>' + result.key + '</code>\\n\\n' +
                '⏱️ <b>Duration:</b> ' + result.duration + '\\n' +
                '📅 <b>Expires:</b> ' + new Date(result.expires).toLocaleString() + '\\n' +
                '📊 <b>Status:</b> Available\\n\\n' +
                '<i>👆 Taabo code-ka si aad u koobiyo</i>\\n\\n' +
                '<b>━━━━━━━━━━━━━━━━━━━━━━</b>\\n' +
                '<b>🛡️ ABDI VIP PANEL</b>',
                { parse_mode: 'HTML' }
            );"""

new_msg = """const keyboard = {
                reply_markup: {
                    inline_keyboard: [
                        [{ text: '📋 COPY CODE', callback_data: 'copy_' + result.key }],
                        [{ text: '📊 STATS', callback_data: 'stats' }]
                    ]
                }
            };
            bot.sendMessage(chatId,
                '<b>╔══════════════════════════╗</b>\\n' +
                '<b>║   ✅ LICENSE KEY LA ABUURAY   ║</b>\\n' +
                '<b>╚══════════════════════════╝</b>\\n\\n' +
                '🔑 <b>License Key:</b>\\n' +
                '<code>' + result.key + '</code>\\n\\n' +
                '⏱️ <b>Duration:</b> ' + result.duration + '\\n' +
                '📅 <b>Expires:</b> ' + new Date(result.expires).toLocaleString() + '\\n' +
                '📊 <b>Status:</b> Available\\n\\n' +
                '<b>━━━━━━━━━━━━━━━━━━━━━━</b>\\n' +
                '<b>🛡️ ABDI VIP PANEL</b>',
                Object.assign({ parse_mode: 'HTML' }, keyboard)
            );"""

if old_msg in c:
    c = c.replace(old_msg, new_msg, 1)
    print("1. Fariinta /gen + keyboard: OK")
else:
    print("1. Fariinta /gen: LAMA HELIN")

# 2. Callback query handler — COPY CODE iyo STATS
old_handlers = "    console.log('🤖 Telegram Bot: handlers la diyaariyay');"
new_handlers = """    // Callback query handler (COPY CODE, STATS)
    bot.on('callback_query', (query) => {
        const chatId = query.message.chat.id;
        const data = query.data;
        if (!isAdmin(chatId)) {
            bot.answerCallbackQuery(query.id, { text: '⛔ Kaliya admin-ka.' });
            return;
        }
        if (data.startsWith('copy_')) {
            const key = data.replace('copy_', '');
            bot.answerCallbackQuery(query.id, { text: '✅ Copied: ' + key, show_alert: false });
            bot.sendMessage(chatId, '📋 <b>License Key:</b>\\n<code>' + key + '</code>\\n\\n<i>Taabo code-ka si aad u koobiyo</i>', { parse_mode: 'HTML' });
        } else if (data === 'stats') {
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
        }
        bot.answerCallbackQuery(query.id);
    });

    console.log('🤖 Telegram Bot: handlers la diyaariyay');"""

if old_handlers in c:
    c = c.replace(old_handlers, new_handlers, 1)
    print("2. Callback handler: OK")
else:
    print("2. Callback handler: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup")
