# fix_health_final.py - Hagaaji /api/health iyo /api/worker-check

with open("server.js", "r") as f:
    content = f.read()

import re

# ===== 1. BEDDEL /api/health =====
old_health = "app.get('/api/health', (req, res) => res.json({ status: 'ok', server: 'ABDI VIP PANEL', time: new Date() }));"

new_health = '''app.get('/api/health', (req, res) => {
    try {
        const userCount = queryOne('SELECT COUNT(*) as c FROM users')?.c || 0;
        const licCount = queryOne('SELECT COUNT(*) as c FROM licenses')?.c || 0;
        res.json({
            status: 'ok',
            server: 'ABDI VIP PANEL',
            version: '3.0.0',
            node_version: process.version,
            environment: process.env.NODE_ENV || 'production',
            uptime: Math.floor(process.uptime()),
            timestamp: new Date().toISOString(),
            database: {
                users: userCount,
                licenses: licCount,
                status: 'connected'
            }
        });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});'''

if old_health in content:
    content = content.replace(old_health, new_health)
    print("✅ /api/health waa la hagaajiyay!")
else:
    print("⚠️ /api/health lama helin — isku day qaab kale")

# ===== 2. KU DAR /api/worker-check (haddii uusan jirin) =====
if "/api/worker-check" in content:
    print("ℹ️ /api/worker-check horey ayuu u jiray!")
else:
    worker_check = '''
// ===== WORKER CHECK ENDPOINT =====
app.get('/api/worker-check', async (req, res) => {
    try {
        const startTime = Date.now();
        const workerUrl = req.query.worker_url || 'https://a.dirxx.workers.dev';
        try {
            const response = await fetch(workerUrl, { method: 'HEAD' });
            const responseTime = Date.now() - startTime;
            const contentType = response.headers.get('content-type') || '';
            const isJson = contentType.includes('application/json');
            const isProxied = response.headers.get('x-railway-edge') !== null;
            res.json({
                status: response.ok ? 'online' : 'error',
                worker_url: workerUrl,
                response_time: responseTime + 'ms',
                http_status: response.status,
                content_type: contentType,
                is_json: isJson,
                is_proxied: isProxied,
                reachable: response.ok,
                message: isProxied ? 'Worker-ku wuxuu u gudbiyaa Railway si guul leh!' : (isJson ? 'Worker-ku wuu shaqeynayaa (JSON)' : 'Worker-ku wuxuu soo celiyaa HTML'),
                timestamp: new Date().toISOString()
            });
        } catch (fetchError) {
            const responseTime = Date.now() - startTime;
            res.json({
                status: 'offline',
                worker_url: workerUrl,
                response_time: responseTime + 'ms',
                reachable: false,
                error: fetchError.message,
                timestamp: new Date().toISOString()
            });
        }
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});

'''
    listen_pos = content.find("app.listen(PORT")
    if listen_pos != -1:
        content = content[:listen_pos] + worker_check + content[listen_pos:]
        print("✅ /api/worker-check waa lagu daray!")
    else:
        print("❌ Ma helin app.listen(PORT")

with open("server.js", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
