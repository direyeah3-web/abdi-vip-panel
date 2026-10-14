import shutil

shutil.copy('server.js', 'server.js.backup')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Fariinta /gen — qaab heer caalami
old_msg = """bot.sendMessage(chatId,
                '✅ <b>License Key la abuuray!</b>\\n\\n' +
                '🔑 <code>' + result.key + '</code>\\n' +
                '⏱️ Duration: <b>' + result.duration + '</b>\\n' +
                '📅 Expires: <b>' + new Date(result.expires).toLocaleString() + '</b>',
                { parse_mode: 'HTML' }
            );"""

new_msg = """bot.sendMessage(chatId,
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

if old_msg in c:
    c = c.replace(old_msg, new_msg, 1)
    print("1. Fariinta /gen: OK")
else:
    print("1. Fariinta /gen: LAMA HELIN")

# 2. Haddii fariinta kale ee /gen (version kale) jirto — isla beddel
old_msg2 = """bot.sendMessage(chatId,
                '✅ <b>License Key la abuuray!</b>\\n\\n' +
                '🔑 <code>' + result.key + '</code>\\n' +
                '⏱️ Duration: <b>' + result.duration + '</b>\\n' +
                '📅 Expires: <b>' + new Date(result.expires).toLocaleString() + '</b>',
                { parse_mode: 'HTML' }
            );"""

# 3. Beddel /start message-ka sidoo kale qaab fiican
old_start = """'👋 <b>Welcome Admin!</b>\\n\\n' +
                '📋 <b>Commands-ka la heli karo:</b>\\n\\n' +
                '/gen &lt;duration&gt; — Abuur license key\\n' +
                '   • 1d = 1 maalin\\n' +
                '   • 7d = 7 maalin\\n' +
                '   • 30d = 30 maalin\\n' +
                '   • 90d = 90 maalin\\n' +
                '   • 1y = 1 sano\\n\\n' +
                '/stats — Xogta panel-ka\\n' +
                '/help — Caawimaad'"""

new_start = """'<b>╔══════════════════════════╗</b>\\n' +
                '<b>║   👋 WELCOME ADMIN   ║</b>\\n' +
                '<b>╚══════════════════════════╝</b>\\n\\n' +
                '📋 <b>Commands-ka la heli karo:</b>\\n\\n' +
                '<b>🔑 LICENSE GENERATOR:</b>\\n' +
                '<code>/gen 1d</code>  — 1 maalin\\n' +
                '<code>/gen 7d</code>  — 7 maalin\\n' +
                '<code>/gen 30d</code> — 30 maalin\\n' +
                '<code>/gen 90d</code> — 90 maalin\\n' +
                '<code>/gen 1y</code>  — 1 sano\\n\\n' +
                '<b>📊 XOGTA:</b>\\n' +
                '<code>/stats</code> — Xogta panel-ka\\n' +
                '<code>/help</code>  — Caawimaad\\n\\n' +
                '<b>━━━━━━━━━━━━━━━━━━━━━━</b>\\n' +
                '<b>🛡️ ABDI VIP PANEL</b>'"""

if old_start in c:
    c = c.replace(old_start, new_start, 1)
    print("2. Fariinta /start: OK")
else:
    print("2. Fariinta /start: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup")
