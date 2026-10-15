import shutil

shutil.copy('server.js', 'server.js.backup_remote_endpoints')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

old = "app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"

new = """// ===== LOADER REMOTE CONFIG ENDPOINTS =====

// GET /api/loader/remote-config — loader-ka wuu wacaa marka la furo
app.get('/api/loader/remote-config', async (req, res) => {
    try {
        const rows = queryAll('SELECT config_key, config_value, config_type FROM loader_remote_config') || [];
        const config = {};
        rows.forEach(r => {
            let val = r.config_value;
            if (r.config_type === 'boolean') val = val === 'true' || val === '1';
            if (r.config_type === 'number') val = parseFloat(val);
            if (r.config_type === 'json') {
                try { val = JSON.parse(val); } catch (e) { val = []; }
            }
            config[r.config_key] = val;
        });

        // Hubi ban list
        const clientSerial = req.query.serial || '';
        const clientKey = req.query.key || '';
        const banList = config.ban_list || [];
        const isBanned = banList.some(b => b.serial === clientSerial || b.key === clientKey);

        res.json({
            success: true,
            config: config,
            banned: isBanned,
            ban_message: isBanned ? 'Akoonkaaga waa la joojiyay. La xidhiidh admin-ka.' : ''
        });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

// POST /api/loader/remote-config — admin-ka wuu beddelaa
app.post('/api/loader/remote-config', auth, adminOnly, (req, res) => {
    try {
        const { updates } = req.body;
        if (!updates || typeof updates !== 'object') {
            return res.status(400).json({ success: false, error: 'Updates waa loo baahan yahay' });
        }
        for (const [key, value] of Object.entries(updates)) {
            let val = value;
            if (typeof value === 'boolean') val = value ? 'true' : 'false';
            if (typeof value === 'object') val = JSON.stringify(value);
            db.run('UPDATE loader_remote_config SET config_value = ?, updated_at = CURRENT_TIMESTAMP WHERE config_key = ?',
                [String(val), key]);
        }
        saveDB();
        const rows = queryAll('SELECT config_key, config_value, config_type FROM loader_remote_config') || [];
        const config = {};
        rows.forEach(r => {
            let val = r.config_value;
            if (r.config_type === 'boolean') val = val === 'true';
            if (r.config_type === 'number') val = parseFloat(val);
            if (r.config_type === 'json') {
                try { val = JSON.parse(val); } catch (e) { val = []; }
            }
            config[r.config_key] = val;
        });
        res.json({ success: true, config: config });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

// POST /api/loader/ban — admin-ku wuu ban-gareeyaa user
app.post('/api/loader/ban', auth, adminOnly, (req, res) => {
    try {
        const { serial, key, reason } = req.body;
        if (!serial && !key) return res.status(400).json({ success: false, error: 'serial ama key waa loo baahan yahay' });
        const banRow = queryOne('SELECT config_value FROM loader_remote_config WHERE config_key = ?', ['ban_list']);
        let banList = [];
        try { banList = JSON.parse(banRow.config_value || '[]'); } catch (e) { banList = []; }
        banList.push({ serial: serial || '', key: key || '', reason: reason || '', banned_at: new Date().toISOString() });
        db.run('UPDATE loader_remote_config SET config_value = ?, updated_at = CURRENT_TIMESTAMP WHERE config_key = ?',
            [JSON.stringify(banList), 'ban_list']);
        saveDB();
        res.json({ success: true, ban_list: banList });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

// POST /api/loader/unban — admin-ku wuu unban-gareeyaa user
app.post('/api/loader/unban', auth, adminOnly, (req, res) => {
    try {
        const { serial, key } = req.body;
        const banRow = queryOne('SELECT config_value FROM loader_remote_config WHERE config_key = ?', ['ban_list']);
        let banList = [];
        try { banList = JSON.parse(banRow.config_value || '[]'); } catch (e) { banList = []; }
        banList = banList.filter(b => b.serial !== serial && b.key !== key);
        db.run('UPDATE loader_remote_config SET config_value = ?, updated_at = CURRENT_TIMESTAMP WHERE config_key = ?',
            [JSON.stringify(banList), 'ban_list']);
        saveDB();
        res.json({ success: true, ban_list: banList });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"""

if old in c:
    c = c.replace(old, new, 1)
    print("1. Remote config endpoints: OK")
else:
    print("1. Remote config endpoints: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_remote_endpoints")
