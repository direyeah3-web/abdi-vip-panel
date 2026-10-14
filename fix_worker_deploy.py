import shutil

shutil.copy('server.js', 'server.js.backup3')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Beddel POST /api/worker/code — multipart/form-data
old_deploy = """        const url = CF_API + '/accounts/' + accountId + '/workers/scripts/' + workerName;
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
        }"""

new_deploy = """        const url = CF_API + '/accounts/' + accountId + '/workers/scripts/' + workerName;
        // Isticmaal FormData (multipart) — Cloudflare API waa in uu helaa metadata + worker.js
        const FormData = require('form-data');
        const form = new FormData();
        form.append('metadata', JSON.stringify({
            main_module: 'worker.js',
            compatibility_date: '2024-01-01'
        }), { contentType: 'application/json' });
        form.append('worker.js', code, {
            filename: 'worker.js',
            contentType: 'application/javascript+module'
        });
        const r = await fetch(url, {
            method: 'PUT',
            headers: Object.assign({ 'Authorization': 'Bearer ' + token }, form.getHeaders()),
            body: form
        });
        const data = await r.json();
        if (r.ok && data.success) {
            res.json({ success: true, message: 'Worker la cusboonaysiiyay!', data: data.result });
        } else {
            res.status(r.status).json({ success: false, error: JSON.stringify(data.errors || data) });
        }"""

if old_deploy in c:
    c = c.replace(old_deploy, new_deploy, 1)
    print("1. Deploy endpoint: OK")
else:
    print("1. Deploy endpoint: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup3")
