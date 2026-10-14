import shutil

shutil.copy('server.js', 'server.js.backup')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Ku dar endpoints — ka hor app.listen(PORT, ...)
old_listen = "app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"

new_listen = """// ===== CLOUDFLARE WORKER ENDPOINTS =====
const CF_API = 'https://api.cloudflare.com/client/v4';

// GET /api/worker/code — soo qaato code-ka worker-ka
app.get('/api/worker/code', auth, adminOnly, async (req, res) => {
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
});

// POST /api/worker/code — cusboonaysii code-ka worker-ka
app.post('/api/worker/code', auth, adminOnly, async (req, res) => {
    try {
        const token = process.env.CLOUDFLARE_API_TOKEN;
        const accountId = process.env.CLOUDFLARE_ACCOUNT_ID;
        const workerName = process.env.CLOUDFLARE_WORKER_NAME || 'a';
        const { code } = req.body;
        if (!token || !accountId) {
            return res.status(400).json({ success: false, error: 'Cloudflare credentials ma jiro' });
        }
        if (!code) {
            return res.status(400).json({ success: false, error: 'Code ma jiro' });
        }
        const url = CF_API + '/accounts/' + accountId + '/workers/scripts/' + workerName;
        const r = await fetch(url, {
            method: 'PUT',
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/javascript'
            },
            body: code
        });
        const data = await r.json();
        if (r.ok && data.success) {
            res.json({ success: true, message: 'Worker la cusboonaysiiyay!', data: data.result });
        } else {
            res.status(r.status).json({ success: false, error: JSON.stringify(data.errors || data) });
        }
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

// GET /api/worker/status — xaaladda worker-ka
app.get('/api/worker/status', auth, adminOnly, async (req, res) => {
    try {
        const token = process.env.CLOUDFLARE_API_TOKEN;
        const accountId = process.env.CLOUDFLARE_ACCOUNT_ID;
        const workerName = process.env.CLOUDFLARE_WORKER_NAME || 'a';
        if (!token || !accountId) {
            return res.json({ success: true, online: false, error: 'Cloudflare credentials ma jiro' });
        }
        const url = CF_API + '/accounts/' + accountId + '/workers/scripts/' + workerName;
        const r = await fetch(url, {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        const text = await r.text();
        const workerUrl = 'https://a.dirxx.workers.dev';
        let workerOnline = false;
        let responseTime = 0;
        try {
            const start = Date.now();
            const wr = await fetch(workerUrl, { method: 'HEAD' });
            responseTime = Date.now() - start;
            workerOnline = wr.ok;
        } catch (e) {}
        if (r.ok) {
            res.json({
                success: true,
                online: true,
                worker_name: workerName,
                worker_url: workerUrl,
                worker_online: workerOnline,
                response_time: responseTime + 'ms',
                code_length: text.length,
                account_id: accountId
            });
        } else {
            res.json({ success: true, online: false, error: 'Worker code lama helin' });
        }
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"""

if old_listen in c:
    c = c.replace(old_listen, new_listen, 1)
    print("1. Worker endpoints: OK")
else:
    print("1. Worker endpoints: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup")
