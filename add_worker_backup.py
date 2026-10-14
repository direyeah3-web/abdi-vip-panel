import shutil

shutil.copy('server.js', 'server.js.backup5')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

old = "app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"

new = """// POST /api/worker/backup — keydi code-ka worker-ka
app.post('/api/worker/backup', auth, adminOnly, async (req, res) => {
    try {
        const { code } = req.body;
        if (!code) {
            return res.status(400).json({ success: false, error: 'Code ma jiro' });
        }
        const fs = require('fs');
        const backupFile = './worker.js.backup';
        fs.writeFileSync(backupFile, code, 'utf-8');
        res.json({ success: true, message: 'Backup la keydiyay', file: backupFile, size: code.length });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"""

if old in c:
    c = c.replace(old, new, 1)
    print("1. Backup endpoint: OK")
else:
    print("1. Backup endpoint: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup5")
