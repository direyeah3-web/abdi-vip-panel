const fs = require('fs');
let code = fs.readFileSync('server.js', 'utf8');

// Hubi haddii Venus endpoint uu jiro
if (!code.includes('/jnative/binder')) {
  const venusEndpoint = `

// ===== VENUS HAX ENDPOINT =====
app.post('/jnative/binder', (req, res) => {
  try {
    const body = req.body || {};
    const userKey = String(body.user_key || body.license_key || body.key || '').trim();
    const serial = String(body.serial || body.device_id || '').trim();
    console.log('[VENUS]', { user_key: userKey, serial });
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    if (!userKey || userKey.length < 5) {
      return res.json({ status: 'error', success: false, is_valid: false, message: 'Invalid key' });
    }
    const expDate = '2026-11-01';
    res.json({
      status: 'success',
      success: true,
      is_valid: true,
      valid: true,
      state: 'online',
      message: 'License valid',
      expires: expDate,
      exdate: expDate,
      expire: expDate,
      token: 'ABDI-VIP-TOKEN-' + Date.now(),
      session: 'ABDI-VIP-SESSION-' + Date.now(),
      user_key: userKey,
      serial: serial,
      appstatus: true
    });
  } catch (e) {
    res.json({ status: 'error', success: false, is_valid: false, message: e.message });
  }
});
`;
  const listenPattern = /app\.listen\(PORT[^;]*\);/;
  if (listenPattern.test(code)) {
    code = code.replace(listenPattern, venusEndpoint + '\n$&');
    fs.writeFileSync('server.js', code);
    console.log('VENUS ENDPOINT ADDED');
  } else {
    console.log('LISTEN NOT FOUND');
  }
} else {
  console.log('VENUS ENDPOINT ALREADY EXISTS');
}
