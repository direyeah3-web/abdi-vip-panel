import shutil

shutil.copy('server.js', 'server.js.backup2')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Beddel endpoint-ka /api/worker/code — nadiifi boundary lines
old_code = """app.get('/api/worker/code', auth, adminOnly, async (req, res) => {
    try {
        const token = process.env.CLOUDFLARE_API_TOKEN;
        const accountId = process.env.CLOUDFLARE_ACCOUNT_ID;
        const workerName = process.env.CLOUDFLARE_WORKER_NAME || 'a';
        if (!token || !accountId) {
            return res.status(400).json({ success: false, error: 'Cloudflare credentials ma jiro' });
        }
        const url = CF_API + '/accounts/' + accountId + '/workers/scripts/' + workerName;
        const r = await fetch(url, {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        const text = await r.text();
        if (r.ok) {
            res.json({ success: true, code: text, worker: workerName });
        } else {
            res.status(r.status).json({ success: false, error: text });
        }
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});"""

new_code = """app.get('/api/worker/code', auth, adminOnly, async (req, res) => {
    try {
        const token = process.env.CLOUDFLARE_API_TOKEN;
        const accountId = process.env.CLOUDFLARE_ACCOUNT_ID;
        const workerName = process.env.CLOUDFLARE_WORKER_NAME || 'a';
        if (!token || !accountId) {
            return res.status(400).json({ success: false, error: 'Cloudflare credentials ma jiro' });
        }
        const url = CF_API + '/accounts/' + accountId + '/workers/scripts/' + workerName;
        const r = await fetch(url, {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        const text = await r.text();
        if (r.ok) {
            // Nadiifi boundary lines — kaliya code-ka
            let cleanCode = text;
            const exportIdx = cleanCode.indexOf('export default');
            if (exportIdx > 0) {
                cleanCode = cleanCode.substring(exportIdx);
            }
            // Ka saar boundary line-ka ugu dambeeya (--boundary--)
            const lastBoundary = cleanCode.lastIndexOf('\\n--');
            if (lastBoundary > 0) {
                cleanCode = cleanCode.substring(0, lastBoundary);
            }
            cleanCode = cleanCode.trim();
            res.json({ success: true, code: cleanCode, worker: workerName });
        } else {
            res.status(r.status).json({ success: false, error: text });
        }
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});"""

if old_code in c:
    c = c.replace(old_code, new_code, 1)
    print("1. Worker code endpoint: OK")
else:
    print("1. Worker code endpoint: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup2")
