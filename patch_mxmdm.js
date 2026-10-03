const fs = require('fs');
let code = fs.readFileSync('server.js', 'utf8');

if (code.includes('/connect')) {
  console.log('MXMDM ENDPOINTS ALREADY EXIST');
  process.exit(0);
}

const mxmdmEndpoints = `

// ===== MXMDM / MEEMO ENDPOINTS =====
app.post('/1.1/account/verify_credentials.json', (req, res) => {
  try {
    const body = req.body || {};
    const keysArray = body.keysArray || [];
    const userKey = Array.isArray(keysArray) ? keysArray[0] : (body.user_key || body.key || '');
    console.log('[MXMDM-VERIFY]', { keysArray, userKey });
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    if (!userKey || userKey.length < 5) {
      return res.json({ code: 1, msg: 'Key not found', result: 0, status: 0 });
    }
    const expDate = '2026-10-26 11:51:41';
    res.json({
      code: 0,
      msg: 'success',
      result: 1,
      status: 1,
      data: {
        valid: true,
        expire: expDate,
        licenseCount: 999
      },
      kv: {
        license: userKey,
        expire: expDate,
        status: 'active',
        licenseCount: 999
      }
    });
  } catch (e) {
    res.json({ code: 1, msg: e.message, result: 0, status: 0 });
  }
});

app.post('/connect', (req, res) => {
  try {
    const body = req.body || {};
    const userKey = String(body.user_key || body.key || body.license || '').trim();
    const serial = String(body.serial || body.device_id || '').trim();
    const game = String(body.game || '').trim();
    console.log('[MXMDM-CONNECT]', { user_key: userKey, serial, game });
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    if (!userKey || userKey.length < 5) {
      return res.json({ code: 1, msg: 'Key not found', result: 0, status: 0 });
    }
    const expDate = '2026-10-26 11:51:41';
    res.json({
      code: 0,
      msg: 'success',
      result: 1,
      status: 1,
      data: {
        valid: true,
        expire: expDate,
        licenseCount: 999
      },
      kv: {
        license: userKey,
        expire: expDate,
        status: 'active',
        licenseCount: 999
      }
    });
  } catch (e) {
    res.json({ code: 1, msg: e.message, result: 0, status: 0 });
  }
});

app.post('/config.Config/GetByKeys', (req, res) => {
  try {
    const body = req.body || {};
    const userKey = String(body.user_key || body.key || body.license || '').trim();
    console.log('[MXMDM-GETBYKEYS]', { user_key: userKey });
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.json({
      code: 0,
      msg: 'success',
      result: 1,
      status: 1,
      data: { valid: true, expire: '2026-10-26 11:51:41', licenseCount: 999 },
      kv: { license: userKey, expire: '2026-10-26 11:51:41', status: 'active', licenseCount: 999 }
    });
  } catch (e) {
    res.json({ code: 1, msg: e.message, result: 0, status: 0 });
  }
});

app.post('/config.Config/ClientKV', (req, res) => {
  try {
    const body = req.body || {};
    const userKey = String(body.user_key || body.key || body.license || '').trim();
    console.log('[MXMDM-CLIENTKV]', { user_key: userKey });
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.json({
      code: 0,
      msg: 'success',
      result: 1,
      status: 1,
      kv: { license: userKey, expire: '2026-10-26 11:51:41', status: 'active', licenseCount: 999 }
    });
  } catch (e) {
    res.json({ code: 1, msg: e.message, result: 0, status: 0 });
  }
});
`;

const listenPattern = /app\.listen\(PORT[^;]*\);/;
if (!listenPattern.test(code)) {
  console.log('LISTEN NOT FOUND');
  process.exit(1);
}
code = code.replace(listenPattern, mxmdmEndpoints + '\n$&');
fs.writeFileSync('server.js', code);
console.log('MXMDM ENDPOINTS ADDED');
