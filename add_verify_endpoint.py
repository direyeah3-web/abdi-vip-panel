import shutil

shutil.copy('server.js', 'server.js.backup_verify')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

old = "app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"

new = """// ===== /api/verify — Loader-ka license verification =====
app.post('/api/verify', async (req, res) => {
    try {
        // Hubi token-ka (haddii loo baahdo)
        const panelToken = req.headers['x-panel-token'];
        if (process.env.PANEL_TOKEN && panelToken !== process.env.PANEL_TOKEN) {
            return res.json({ valid: false, expire: '', message: 'Unauthorized' });
        }

        const { key, serial } = req.body || {};
        if (!key) {
            return res.json({ valid: false, expire: '', message: 'Key ma jiro' });
        }

        // Soo qaado license-ka database-ka
        const license = queryOne('SELECT * FROM licenses WHERE license_key = ?', [key]);
        if (!license) {
            return res.json({ valid: false, expire: '', message: 'License ma jiro' });
        }

        // Hubi haddii uu dhamaaday
        if (license.expires_at) {
            const expireDate = new Date(license.expires_at);
            if (expireDate < new Date()) {
                return res.json({ valid: false, expire: license.expires_at, message: 'License dhamaaday' });
            }
        }

        // Hubi device_id (haddii serial la soo diray)
        if (serial && license.device_id && license.device_id !== serial) {
            return res.json({ valid: false, expire: license.expires_at, message: 'Device kale' });
        }

        // Haddii device_id aan la keydin, keydi serial-ka
        if (serial && !license.device_id) {
            db.run('UPDATE licenses SET device_id = ?, status = ? WHERE id = ?',
                [serial, 'active', license.id]);
            saveDB();
        }

        // License waa sax
        res.json({
            valid: true,
            expire: license.expires_at || '2099-12-31',
            duration: license.duration || '',
            message: ''
        });
    } catch (err) {
        console.error('Verify error:', err);
        res.json({ valid: false, expire: '', message: err.message });
    }
});

app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"""

if old in c:
    c = c.replace(old, new, 1)
    print("1. /api/verify: OK")
else:
    print("1. /api/verify: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_verify")
