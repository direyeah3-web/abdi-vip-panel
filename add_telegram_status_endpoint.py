import shutil

shutil.copy('server.js', 'server.js.backup')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Ku dar endpoint-ka cusub — ka hor /api/telegram/test
old_test = "app.post('/api/telegram/test', auth, adminOnly, async (req, res) => {"
new_endpoint = """// Telegram — Status endpoint
app.get('/api/telegram/status', auth, adminOnly, async (req, res) => {
    try {
        if (!bot) {
            return res.json({ 
                success: true, 
                online: false, 
                error: 'Bot ma jiro — .env hubi' 
            });
        }
        if (!TELEGRAM_BOT_TOKEN) {
            return res.json({ 
                success: true, 
                online: false, 
                error: 'Token ma jiro' 
            });
        }
        // Hubi bot-ka getMe
        const https = require('https');
        const botInfo = await new Promise((resolve, reject) => {
            https.get('https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/getMe', (r) => {
                let data = '';
                r.on('data', chunk => data += chunk);
                r.on('end', () => {
                    try { resolve(JSON.parse(data)); } 
                    catch(e) { reject(e); }
                });
            }).on('error', reject);
        });
        
        if (botInfo && botInfo.ok) {
            res.json({
                success: true,
                online: true,
                username: botInfo.result.username,
                name: botInfo.result.first_name,
                polling: true,
                version: '3.0.0',
                node: process.version,
                uptime: Math.floor(process.uptime()),
                chat_id: TELEGRAM_ADMIN_CHAT_ID
            });
        } else {
            res.json({
                success: true,
                online: false,
                error: botInfo.description || 'Bot ma shaqeynayo'
            });
        }
    } catch (err) {
        res.json({ 
            success: true, 
            online: false, 
            error: err.message 
        });
    }
});

app.post('/api/telegram/test', auth, adminOnly, async (req, res) => {"""

if old_test in c:
    c = c.replace(old_test, new_endpoint, 1)
    print("1. Endpoint /api/telegram/status: OK")
else:
    print("1. Endpoint: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup")
