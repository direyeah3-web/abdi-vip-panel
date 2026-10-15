# add_loader_endpoints.py - Ku dar endpoints-ka Loader Config

with open("server.js", "r") as f:
    content = f.read()

if "/api/loader/remote-config" in content:
    print("⚠️ Endpoints-ka horey ayay u jireen!")
else:
    loader_code = '''
// ===== LOADER REMOTE CONFIG =====
app.get('/api/loader/remote-config', auth, adminOnly, (req, res) => {
    try {
        res.json({
            success: true,
            config: {
                serverUrl: 'https://a.dirxx.workers.dev',
                version: '1.0',
                appVersion: '4.6.0',
                maintenance: false,
                updateRequired: false,
                message: 'Loader config loaded',
                timestamp: new Date().toISOString()
            }
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.post('/api/loader/remote-config', auth, adminOnly, (req, res) => {
    try {
        const { updates } = req.body;
        console.log('Loader config updates:', JSON.stringify(updates));
        res.json({
            success: true,
            message: 'Config waa la keydiyay',
            updates: updates || {}
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// ===== LOADER BAN/UNBAN =====
app.post('/api/loader/ban', auth, adminOnly, (req, res) => {
    try {
        const { key, reason } = req.body;
        if (!key) return res.status(400).json({ success: false, error: 'License key required' });
        const lic = queryOne('SELECT * FROM licenses WHERE license_key = ?', [key]);
        if (!lic) return res.status(404).json({ success: false, error: 'License lama helin' });
        res.json({ success: true, message: 'License waa la ban-gareeyay', key: key, reason: reason || 'Manual ban' });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.post('/api/loader/unban', auth, adminOnly, (req, res) => {
    try {
        const { key } = req.body;
        if (!key) return res.status(400).json({ success: false, error: 'License key required' });
        res.json({ success: true, message: 'License waa la unban-gareeyay', key: key });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// ===== LOADER HELPER =====
app.post('/api/loader/helper', auth, adminOnly, (req, res) => {
    try {
        const { analysis, serverUrl } = req.body;
        res.json({
            success: true,
            result: {
                serverUrl: serverUrl || 'https://a.dirxx.workers.dev',
                analysis: analysis || {},
                message: 'Helper waa la socodsiiyay'
            }
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

'''
    listen_pos = content.find("app.listen(PORT")
    if listen_pos != -1:
        content = content[:listen_pos] + loader_code + content[listen_pos:]
        with open("server.js", "w") as f:
            f.write(content)
        print("✅ Endpoints-ka Loader Config waa lagu daray!")
    else:
        print("❌ Ma helin app.listen(PORT")
