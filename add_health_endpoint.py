# add_health_endpoint.py - Ku dar endpoint-ka health check

with open("server.js", "r") as f:
    content = f.read()

if "/api/health" in content:
    print("⚠️ Endpoint-ka horey ayuu u jiray!")
else:
    health_code = """
// ===== HEALTH CHECK ENDPOINT =====
app.get('/api/health', (req, res) => {
    try {
        const userCount = queryOne('SELECT COUNT(*) as c FROM users')?.c || 0;
        const licenseCount = queryOne('SELECT COUNT(*) as c FROM licenses')?.c || 0;
        
        res.json({
            status: 'online',
            server: 'abdi-vip-panel',
            version: '3.0.0',
            timestamp: new Date().toISOString(),
            uptime: process.uptime(),
            database: {
                users: userCount,
                licenses: licenseCount,
                status: 'connected'
            },
            node_version: process.version,
            environment: process.env.NODE_ENV || 'production'
        });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});

// ===== WORKER CHECK ENDPOINT =====
app.get('/api/worker-check', async (req, res) => {
    try {
        const startTime = Date.now();
        const workerUrl = req.query.worker_url || 'https://a.dirxx.workers.dev';
        
        // Isku day inaad xiriirto Worker-ka
        try {
            const response = await fetch(workerUrl, { method: 'HEAD' });
            const responseTime = Date.now() - startTime;
            
            res.json({
                status: 'online',
                worker_url: workerUrl,
                response_time: responseTime + 'ms',
                http_status: response.status,
                reachable: true,
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

"""
    listen_pos = content.find("app.listen(PORT")
    if listen_pos != -1:
        new_content = content[:listen_pos] + health_code + content[listen_pos:]
        with open("server.js", "w") as f:
            f.write(new_content)
        print("✅ Endpoint-yada health iyo worker-check waa lagu daray!")
    else:
        print("❌ Ma helin app.listen(PORT")
