const fs = require('fs');
let code = fs.readFileSync('server.js', 'utf8');

if (code.includes('/ObsidianAuth/api.php')) {
  console.log('ALREADY EXISTS');
  process.exit(0);
}

const obsidianEndpoint = `

// ===== OBSIDIAN AUTH ENDPOINT =====
app.post('/ObsidianAuth/api.php', (req, res) => {
  try {
    const body = req.body || {};
    const licenseKey = String(body.license_key || body.user_key || body.key || body.license || '').trim();
    const serial = String(body.serial || body.device_id || '').trim();
    const game = String(body.game || '').trim();

    console.log('[OBSIDIAN]', { license_key: licenseKey, serial, game });

    res.setHeader('Content-Type', 'application/json; charset=utf-8');

    if (!licenseKey || licenseKey.length < 5) {
      return res.json({
        status: false,
        data: { EXP: '' },
        reason: 'INVALID'
      });
    }

    const expDate = '2026-11-01';

    res.json({
      status: true,
      data: {
        EXP: expDate,
        expires: expDate,
        remaining_seconds: 31536000,
        version: '4.6.0',
        latest_version: '4.6.0',
        appstatus: true,
        server_status: true
      },
      apk: {
        version: '4.6.0',
        required: false
      },
      latest_file: {
        apk: {
          version: '4.6.0',
          required: false
        }
      },
      app_update_required: false,
      update_required: false,
      appstatus: true,
      server_status: true,
      message: 'License valid',
      latest_apk_version: '4.6.0'
    });
  } catch (e) {
    console.log('[OBSIDIAN ERROR]', e.message);
    res.json({ status: false, data: { EXP: '' }, reason: 'FAILED' });
  }
});

app.get('/ObsidianAuth/api.php', (req, res) => {
  if (req.query.action === 'release_manifest') {
    return res.json({
      status: true,
      latest_apk_version: '4.6.0',
      client_apk_version: req.query.client_apk_version
    });
  }
  res.json({ status: true });
});

// ===== API LOADER ENDPOINT (for in-app) =====
app.post('/api/loader', (req, res) => {
  try {
    const body = req.body || {};
    const licenseKey = String(body.license_key || body.user_key || body.key || '').trim();

    if (!licenseKey) {
      return res.json({ status: false, data: { EXP: '' }, reason: 'INVALID' });
    }

    const expDate = '2026-11-01';
    res.json({
      status: true,
      data: {
        EXP: expDate,
        expires: expDate,
        remaining_seconds: 31536000,
        version: '4.6.0',
        latest_version: '4.6.0',
        appstatus: true,
        server_status: true
      },
      apk: { version: '4.6.0', required: false },
      latest_file: { apk: { version: '4.6.0', required: false } },
      app_update_required: false,
      update_required: false,
      appstatus: true,
      server_status: true,
      message: 'License valid',
      latest_apk_version: '4.6.0'
    });
  } catch (e) {
    res.json({ status: false, data: { EXP: '' }, reason: 'FAILED' });
  }
});
`;

const listenPattern = /app\.listen\(PORT[^;]*\);/;
if (!listenPattern.test(code)) {
  console.log('LISTEN NOT FOUND');
  process.exit(1);
}

code = code.replace(listenPattern, obsidianEndpoint + '\n$&');
fs.writeFileSync('server.js', code);
console.log('PATCHED');
