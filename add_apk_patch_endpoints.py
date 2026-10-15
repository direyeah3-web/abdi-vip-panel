#!/usr/bin/env python3
import shutil, os, sys, re

SERVER = os.path.expanduser('~/abdi-panel/server.js')
BACKUP = SERVER + '.backup_before_patch_endpoints'

if not os.path.exists(SERVER):
    print("LAMA HELIN: server.js")
    sys.exit(1)

shutil.copy(SERVER, BACKUP)
print(f"Backup: {BACKUP}")

with open(SERVER, 'r', encoding='utf-8') as f:
    content = f.read()

# Hubi haddii horey loo daray
if 'api/apk/patch-callback' in content:
    print("HOREY AYAA LA DARAY")
    sys.exit(0)

# Soo raadi meesha APK analyze-ka ku dhammaado (app.post('/api/apk/analyze'...)
marker = "app.post('/api/apk/analyze'"
idx = content.find(marker)
if idx == -1:
    print("LAMA HELIN: apk/analyze endpoint")
    sys.exit(1)

# Soo raadi .end method ee analyze-ka — tan waa adag
# Isticmaal marker kale: raadi `app.post('/api/apk/` dhamaadka
# Tusaale: ku dar endpoints-ka ka dib analyze function
# Waxaan u baahanahay in aan helo meesha analyze-ku dhammaado

# Soo raadi dhammaadka app.post('/api/apk/analyze' function
# Wuxuu bilaabmaa idx, wuxuu dhammaadaa `});` kadib
search_from = idx
depth = 0
found_start = False
end_idx = -1
i = search_from
while i < len(content):
    if content[i] == '{':
        depth += 1
        found_start = True
    elif content[i] == '}':
        depth -= 1
        if found_start and depth == 0:
            # Soo raadi `);` ka dib
            j = i
            while j < len(content) and content[j] != ';':
                j += 1
            if j < len(content):
                end_idx = j + 1
            break
    i += 1

if end_idx == -1:
    print("LAMA HELIN: analyze function dhammaad")
    sys.exit(1)

new_code = '''

// ============================================================
// APK PATCH ENDPOINTS — la daray
// ============================================================

// GET /api/apk/raw/:filename — APK soo dejiso (GitHub Actions)
app.get('/api/apk/raw/:filename', (req, res) => {
  const filename = req.params.filename.replace(/[^a-zA-Z0-9_.-]/g, '');
  const paths = [
    '/tmp/' + filename,
    '/tmp/apk_' + filename,
    path.join(os.tmpdir(), filename),
  ];
  for (const p of paths) {
    if (fs.existsSync(p)) {
      return res.sendFile(p);
    }
  }
  res.status(404).json({ success: false, error: 'APK ma jiro' });
});

// POST /api/apk/patch — GitHub Actions trigger
app.post('/api/apk/patch', auth, adminOnly, async (req, res) => {
  try {
    const { apkPath, options } = req.body;
    if (!apkPath) return res.status(400).json({ success: false, error: 'apkPath waa loo baahan yahay' });
    if (!fs.existsSync(apkPath)) return res.status(400).json({ success: false, error: 'APK ma jiro' });

    const jobId = 'j_' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
    const filename = path.basename(apkPath);

    // Job keydi
    if (!global.patchJobs) global.patchJobs = new Map();
    global.patchJobs.set(jobId, {
      status: 'queued',
      apkPath,
      filename,
      options: options || {},
      createdAt: Date.now(),
    });

    // GitHub API trigger
    const ghRepo = process.env.GH_REPO || 'direyeah3-web/abdi-patcher';
    const ghToken = process.env.GH_TOKEN;
    if (!ghToken) return res.status(500).json({ success: false, error: 'GH_TOKEN ma jiro' });

    const ghRes = await fetch(`https://api.github.com/repos/${ghRepo}/actions/workflows/patch.yml/dispatches`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${ghToken}`,
        'Accept': 'application/vnd.github+json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ref: 'main',
        inputs: {
          apk_url: `${process.env.PANEL_URL || 'https://abdi-vip-panel-production.up.railway.app'}/api/apk/raw/${filename}`,
          job_id: jobId,
          patch_options: JSON.stringify(options || {}),
        },
      }),
    });

    if (!ghRes.ok) {
      const errText = await ghRes.text();
      return res.status(500).json({ success: false, error: 'GitHub trigger failed: ' + errText });
    }

    res.json({ success: true, jobId });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/apk/patch-callback — GitHub webhook
app.post('/api/apk/patch-callback', (req, res) => {
  const secret = req.headers['x-webhook-secret'];
  if (secret !== process.env.PANEL_WEBHOOK_SECRET) {
    return res.status(401).json({ success: false, error: 'unauthorized' });
  }
  const { job_id, status, run_id } = req.body;
  if (!global.patchJobs) global.patchJobs = new Map();
  const job = global.patchJobs.get(job_id);
  if (job) {
    job.status = status === 'success' ? 'patched' : 'failed';
    job.runId = run_id;
    job.updatedAt = Date.now();
  }
  res.json({ ok: true });
});

// GET /api/apk/status/:jobId
app.get('/api/apk/status/:jobId', auth, adminOnly, (req, res) => {
  if (!global.patchJobs) global.patchJobs = new Map();
  const job = global.patchJobs.get(req.params.jobId);
  if (!job) return res.status(404).json({ success: false, error: 'Job ma jiro' });
  res.json({ success: true, ...job });
});

// GET /api/apk/download/:jobId — APK patched soo deji
app.get('/api/apk/download/:jobId', auth, adminOnly, (req, res) => {
  if (!global.patchJobs) global.patchJobs = new Map();
  const job = global.patchJobs.get(req.params.jobId);
  if (!job || !job.artifactPath) {
    return res.status(404).json({ success: false, error: 'APK diyaar ma aha' });
  }
  if (!fs.existsSync(job.artifactPath)) {
    return res.status(404).json({ success: false, error: 'APK ma jiro disk-ga' });
  }
  res.download(job.artifactPath, `patched_${req.params.jobId}.apk`);
});

// POST /api/apk/artifact-upload — GitHub Actions wuxuu APK-ga soo dirayaa
app.post('/api/apk/artifact-upload/:jobId', (req, res) => {
  const secret = req.headers['x-webhook-secret'];
  if (secret !== process.env.PANEL_WEBHOOK_SECRET) {
    return res.status(401).json({ success: false });
  }
  const jobId = req.params.jobId;
  const chunks = [];
  req.on('data', c => chunks.push(c));
  req.on('end', () => {
    const buf = Buffer.concat(chunks);
    const outPath = path.join('/tmp', `patched_${jobId}.apk`);
    fs.writeFileSync(outPath, buf);
    if (!global.patchJobs) global.patchJobs = new Map();
    const job = global.patchJobs.get(jobId) || {};
    job.artifactPath = outPath;
    job.status = 'ready';
    job.updatedAt = Date.now();
    global.patchJobs.set(jobId, job);
    res.json({ ok: true, path: outPath });
  });
});

// ============================================================
// DHAMMAAD APK PATCH ENDPOINTS
// ============================================================

'''

# Ku dar endpoints-ka ka dib analyze function
new_content = content[:end_idx] + new_code + content[end_idx:]

with open(SERVER, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("OK: endpoints la daray")
print(f"Backup: {BACKUP}")
