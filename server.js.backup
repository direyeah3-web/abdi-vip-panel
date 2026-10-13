const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const initSqlJs = require('sql.js');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;
const SECRET = 'abdi_vip_secret_2026';
const DB_FILE = './abdi.db';

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

let db;

async function initDB() {
  const SQL = await initSqlJs();
  
// ===== RESET DATABASE (TEMPORARY) =====
if (process.env.RESET_DB === 'true') {
    try {
        if (fs.existsSync(DB_FILE)) {
            fs.unlinkSync(DB_FILE);
            console.log('🗑️ Database file deleted!');
        }
    } catch(e) {
        console.log('Reset error:', e.message);
    }
}

if (fs.existsSync(DB_FILE)) {
    db = new SQL.Database(fs.readFileSync(DB_FILE));
  } else {
    db = new SQL.Database();
  }
  db.run(`CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT,
    fullname TEXT, role TEXT DEFAULT 'user', license_key TEXT, referral_code TEXT,
    referred_by TEXT, status TEXT DEFAULT 'active', created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`);
  db.run(`CREATE TABLE IF NOT EXISTS licenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT, license_key TEXT UNIQUE, user_id INTEGER,
    device_id TEXT, duration TEXT, expires_at DATETIME, max_devices INTEGER DEFAULT 1,
    status TEXT DEFAULT 'unused', created_at DATETIME DEFAULT CURRENT_TIMESTAMP, used_at DATETIME
  )`);
  db.run(`CREATE TABLE IF NOT EXISTS referrals (
    id INTEGER PRIMARY KEY AUTOINCREMENT, referrer_code TEXT, referred_user TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`);
  saveDB();
}

function saveDB() { fs.writeFileSync(DB_FILE, Buffer.from(db.export())); }
function queryOne(sql, params = []) { const s = db.prepare(sql); s.bind(params); if (s.step()) { const r = s.getAsObject(); s.free(); return r; } s.free(); return null; }
function queryAll(sql, params = []) { const s = db.prepare(sql); s.bind(params); const rows = []; while (s.step()) rows.push(s.getAsObject()); s.free(); return rows; }
function genCode(p) { return p + '-' + Math.random().toString(36).substring(2, 10).toUpperCase(); }
function addDuration(d) {
  const now = new Date();
  const m = d.match(/^(\d+)\s*(hour|hours|day|days|month|months|year|years)$/i);
  if (!m) return null;
  const n = parseInt(m[1]); const u = m[2].toLowerCase();
  if (u.startsWith('hour')) now.setHours(now.getHours() + n);
  else if (u.startsWith('day')) now.setDate(now.getDate() + n);
  else if (u.startsWith('month')) now.setMonth(now.getMonth() + n);
  else if (u.startsWith('year')) now.setFullYear(now.getFullYear() + n);
  return now.toISOString();
}
function auth(req, res, next) {
    try {
        const authHeader = req.headers['authorization'];
        const token = authHeader && authHeader.split(' ')[1];
        
        if (!token) {
            return res.status(401).json({ error: 'No token provided' });
        }
        
        // Token-ka cusub wuxuu leeyahay qaab: token_ID_TIMESTAMP
        if (token.startsWith('token_')) {
            const parts = token.split('_');
            const userId = parts[1];
            
            // Raadi user-ka database-ka
            const user = queryOne('SELECT * FROM users WHERE id = ?', [userId]);
            
            if (!user) {
                return res.status(401).json({ error: 'User not found' });
            }
            
            req.user = user;
            return next();
        }
        
        // Haddii uu yahay JWT token (kii hore)
        try {
            const decoded = jwt.verify(token, SECRET);
            req.user = decoded;
            return next();
        } catch(e) {
            return res.status(401).json({ error: 'Invalid token' });
        }
    } catch (error) {
        return res.status(401).json({ error: error.message });
    }
}
function adminOnly(req, res, next) { if (req.user.role !== 'admin') return res.status(403).json({ error: 'Admin only' }); next(); }

function loaderAuth(req, res) {
  const { license_key, device_id, key, license } = req.body;
  const licKey = license_key || key || license;
  if (!licKey) return res.status(400).json({ isValid: false, valid: false, error: 'License required' });
  console.log('>>> QUERY licKey:', licKey);
        const lic = queryOne('SELECT * FROM licenses WHERE license_key = ?', [licKey]);
        console.log('>>> QUERY RESULT:', JSON.stringify(lic));
  if (!lic) return res.status(401).json({ isValid: false, valid: false, error: 'License not found' });
  if (lic.expires_at && new Date(lic.expires_at) < new Date()) return res.status(403).json({ isValid: false, valid: false, error: 'License expired' });
  if (lic.status === 'used' && lic.device_id && lic.device_id !== device_id) return res.status(403).json({ isValid: false, valid: false, error: 'License locked to another device' });
  if (lic.status === 'unused') { db.run('UPDATE licenses SET status = ?, device_id = ?, used_at = CURRENT_TIMESTAMP WHERE id = ?', ['used', device_id || null, lic.id]); saveDB(); }
  const token = jwt.sign({ license: licKey, device: device_id, expires: lic.expires_at }, SECRET, { expiresIn: '30d' });
  res.json({ isValid: true, valid: true, success: true, status: 'success',
      success: true,
      is_valid: true,
      state: 'online',
      message: 'License valid', token, expires_at: lic.expires_at, duration: lic.duration, message: 'Loader authenticated' });
}

app.post('/api/loader/auth', loaderAuth);
app.post('/c', loaderAuth);

app.post('/api/register', async (req, res) => {
  const { username, password, fullname, license_key, referral_code } = req.body;
  if (!username || !password) return res.status(400).json({ error: 'Missing fields' });
  if (queryOne('SELECT id FROM users WHERE username = ?', [username])) return res.status(400).json({ error: 'User exists' });
  let lic = null;
  if (license_key) { lic = queryOne('SELECT * FROM licenses WHERE license_key = ? AND status = ?', [license_key, 'unused']); if (!lic) return res.status(400).json({ error: 'Invalid or used license' }); }
  const hashed = await bcrypt.hash(password, 10);
  const myRef = genCode('ABDI');
  db.run('INSERT INTO users (username, password, fullname, license_key, referral_code, referred_by) VALUES (?, ?, ?, ?, ?, ?)', [username, hashed, fullname || username, license_key || null, myRef, referral_code || null]);
  saveDB();
  if (lic) { db.run('UPDATE licenses SET status = ?, user_id = ?, used_at = CURRENT_TIMESTAMP WHERE id = ?', ['used', lic.id, lic.id]); saveDB(); }
  if (referral_code) { db.run('INSERT INTO referrals (referrer_code, referred_user) VALUES (?, ?)', [referral_code, username]); saveDB(); }
  const user = queryOne('SELECT * FROM users WHERE username = ?', [username]);
  const token = jwt.sign({ id: user.id, username: user.username, role: user.role }, SECRET);
  res.json({ token, user: { username: user.username, fullname: user.fullname, role: user.role, referral_code: user.referral_code, license_key: user.license_key } });
});

app.post('/api/login', async (req, res) => {
    try {
        const { username, password } = req.body;
        
        // Xaqiiji xogta
        if (!username || !password) {
            return res.status(400).json({ success: false, message: 'Username iyo password waa loo baahan yahay' });
        }
        
        // Raadi user-ka
        const user = queryOne('SELECT * FROM users WHERE username = ?', [username]);
        
        if (!user) {
            return res.status(401).json({ success: false, message: 'User-ka lama helin' });
        }
        
        // Hubi password-ka (si fudud - ma isticmaalno bcrypt)
        // Haddii password-ka database-ku yahay mid bcrypt ah, isku day inaad isbarbardhigto
        let passwordMatch = false;
        
        // Hubi haddii password-ku yahay bcrypt hash (wuxuu bilaabmaa $2a$ ama $2b$)
        if (user.password && user.password.startsWith('$2')) {
            // Waa bcrypt hash - isticmaal bcrypt.compare
            const bcrypt = require('bcryptjs');
            passwordMatch = await bcrypt.compare(password, user.password);
        } else {
            // Waa password caadi ah - isbarbardhig toos ah
            passwordMatch = (password === user.password);
        }
        
        if (!passwordMatch) {
            return res.status(401).json({ success: false, message: 'Password-ka waa khaldan yahay' });
        }
        
        // Samee token fudud (ma isticmaalno JWT)
        const token = 'token_' + user.id + '_' + Date.now();
        
        // Keydi token-ka database-ka
        try {
            db.run("UPDATE users SET token = ? WHERE id = ?", [token, user.id]);
            saveDB();
        } catch(e) {
            // Haddii column-ka token uusan jirin, iska dhaaf
        }
        
        // Soo celi xogta user-ka
        res.json({
            success: true,
            token: token,
            user: {
                id: user.id,
                username: user.username,
                fullname: user.fullname,
                role: user.role,
                referral_code: user.referral_code,
                license_key: user.license_key
            }
        });
    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ success: false, message: 'Server error: ' + error.message });
    }
});

app.get('/api/me', auth, (req, res) => {
  const u = queryOne('SELECT username, fullname, role, license_key, referral_code, referred_by, created_at FROM users WHERE id = ?', [req.user.id]);
  if (!u) return res.status(404).json({ error: 'Not found' });
  const refCount = queryOne('SELECT COUNT(*) as c FROM referrals WHERE referrer_code = ?', [u.referral_code]).c;
  res.json({ ...u, referrals: refCount, earnings: (refCount * 2.5).toFixed(2) });
});

app.post('/api/licenses/generate', auth, adminOnly, (req, res) => {
  const { duration, max_devices, custom_key } = req.body;
  const dur = duration || (days ? days + ' days' : '30 days');
  const maxDev = parseInt(max_devices) || 1;
  const expires = addDuration(dur);
  if (!expires) return res.status(400).json({ error: 'Invalid duration' });
  const key = custom_key || genCode('ABDI-VIP');
  try { db.run('INSERT INTO licenses (license_key, duration, expires_at, max_devices) VALUES (?, ?, ?, ?)', [key, dur, expires, maxDev]); saveDB(); res.json({ license_key: key, duration: dur, expires_at: expires, max_devices: maxDev }); }
  catch (e) { res.status(400).json({ error: 'License key already exists' }); }
});

app.get('/api/licenses', auth, adminOnly, (req, res) => res.json(queryAll('SELECT * FROM licenses ORDER BY id DESC')));
app.get('/api/users', auth, adminOnly, (req, res) => res.json(queryAll('SELECT id, username, fullname, role, license_key, referral_code, status, created_at FROM users ORDER BY id DESC')));
app.get('/api/referrals', auth, (req, res) => { const u = queryOne('SELECT referral_code FROM users WHERE id = ?', [req.user.id]); res.json(queryAll('SELECT * FROM referrals WHERE referrer_code = ? ORDER BY id DESC', [u.referral_code])); });
app.get('/api/logs', auth, (req, res) => res.json([{ time: new Date().toISOString(), level: 'OK', msg: 'Server started' }, { time: new Date().toISOString(), level: 'OK', msg: 'Database initialized' }, { time: new Date().toISOString(), level: 'INFO', msg: 'User ' + req.user.username + ' accessed logs' }]));

app.post('/api/loader/verify', (req, res) => {
  const { token } = req.body;
  if (!token) return res.status(400).json({ isValid: false, error: 'Token required' });
  try { const decoded = jwt.verify(token, SECRET); res.json({ isValid: true, valid: true, license: decoded.license, device: decoded.device, expires_at: decoded.expires }); }
  catch (e) { res.status(401).json({ isValid: false, valid: false, error: 'Invalid or expired token' }); }
});

app.get('/api/admin/stats', auth, adminOnly, (req, res) => {
  const totalUsers = queryOne('SELECT COUNT(*) as c FROM users').c;
  const totalLicenses = queryOne('SELECT COUNT(*) as c FROM licenses').c;
  const usedLicenses = queryOne('SELECT COUNT(*) as c FROM licenses WHERE status = ?', ['used']).c;
  const unusedLicenses = queryOne('SELECT COUNT(*) as c FROM licenses WHERE status = ?', ['unused']).c;
  const totalReferrals = queryOne('SELECT COUNT(*) as c FROM referrals').c;
  res.json({ totalUsers, totalLicenses, usedLicenses, unusedLicenses, totalReferrals });
});

app.get('/api/admin/users', auth, adminOnly, (req, res) => res.json(queryAll('SELECT id, username, fullname, role, license_key, referral_code, referred_by, status, created_at FROM users ORDER BY id DESC')));
app.delete('/api/admin/users/:id', auth, adminOnly, (req, res) => { db.run('DELETE FROM users WHERE id = ?', [req.params.id]); saveDB(); res.json({ ok: true }); });
app.put('/api/admin/users/:id', auth, adminOnly, (req, res) => { const { role, status } = req.body; if (role) db.run('UPDATE users SET role = ? WHERE id = ?', [role, req.params.id]); if (status) db.run('UPDATE users SET status = ? WHERE id = ?', [status, req.params.id]); saveDB(); res.json({ ok: true }); });
app.delete('/api/admin/licenses/:id', auth, adminOnly, (req, res) => { db.run('DELETE FROM licenses WHERE id = ?', [req.params.id]); saveDB(); res.json({ ok: true }); });
app.post('/api/admin/licenses/bulk', auth, adminOnly, (req, res) => { const { count, days, duration, max_devices } = req.body; const num = parseInt(count) || 1; const dur = duration || (days ? days + ' days' : '30 days'); const maxDev = parseInt(max_devices) || 1; const expires = addDuration(dur); if (!expires) return res.status(400).json({ error: 'Invalid duration' }); const keys = []; for (let i = 0; i < num; i++) { const key = genCode('ABDI-VIP'); db.run('INSERT INTO licenses (license_key, duration, expires_at, max_devices) VALUES (?, ?, ?, ?)', [key, dur, expires, maxDev]); keys.push(key); } saveDB(); res.json({ ok: true, count: keys.length, keys: keys }); });
app.get('/api/admin/referrals', auth, adminOnly, (req, res) => res.json(queryAll('SELECT * FROM referrals ORDER BY id DESC')));
app.get('/api/health', (req, res) => res.json({ status: 'ok', server: 'ABDI VIP PANEL', time: new Date() }));

initDB().then(async () => {
  const admin = queryOne('SELECT id FROM users WHERE username = ?', ['abdi']);
  if (!admin) {
    const hash = await bcrypt.hash('abdi123', 10);
    db.run('INSERT INTO users (username, password, fullname, role, referral_code) VALUES (?, ?, ?, ?, ?)', ['abdi', hash, 'Abdi Admin', 'admin', 'ABDI2026']);
    saveDB();
    console.log('Admin created: abdi / abdi123');
  }
  

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
      status: 'success',
      success: true,
      is_valid: true,
      state: 'online',
      message: 'License valid',
      appStatus: 'active',
      httpCode: 200,
      message: 'License valid',
      remaining_seconds: 31536000,
      remaining_text: '365 days',
      package_name: 'com.pubg.obsidian',
      policy_version: 1,
      documentVersion: '4.6.0',
      version: '4.6.0',
      latest_version: '4.6.0',
      apk: { version: '4.6.0', required: false },
      latest_file: { apk: { version: '4.6.0', required: false } },
      app_update_required: false,
      update_required: false,
      latest_apk_version: '4.6.0'
    });
  } catch (e) {
    console.log('[OBSIDIAN ERROR]', e.message);
    res.json({ status: false, data: { EXP: '' }, reason: 'FAILED' });
  }
});

app.get('/ObsidianAuth/api.php', (req, res) => {
    try {
        const action = req.query.action;
        const licenseKey = req.query.license_key || req.query.key || '';
        const clientVersion = req.query.client_apk_version || '4.6.0';
        
        if (action === 'release_manifest') {
            let expDate = '2026-11-01';
            let duration = '365 days';
            let userId = licenseKey || 'GUEST';
            
            if (licenseKey) {
                const lic = queryOne('SELECT * FROM licenses WHERE license_key = ?', [licenseKey]);
                if (lic) {
                    expDate = lic.expires_at || '2026-11-01';
                    duration = lic.duration || '365 days';
                    userId = lic.license_key;
                }
            }
            
            const appVersion = '4.6.0';
            const gameList = [
                { gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Global", gameStatus: "Latest Version", gameVersion: "Latest Version", currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion, gamePackage: "com.tencent.ig", gameIcon: "pubg_global.png", gameObb: "", link: "https://www.pubgmobile.com/" },
                { gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Korea", gameStatus: "Latest Version", gameVersion: "Latest Version", currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion, gamePackage: "com.pubg.krmobile", gameIcon: "pubg_korea.png", gameObb: "", link: "https://www.pubgmobile.com/" },
                { gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Vietnam", gameStatus: "Latest Version", gameVersion: "Latest Version", currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion, gamePackage: "com.vng.pubgmobile", gameIcon: "pubg_vietnam.png", gameObb: "", link: "https://www.pubgmobile.com/" },
                { gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Taiwan", gameStatus: "Latest Version", gameVersion: "Latest Version", currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion, gamePackage: "com.rekoo.pubgm", gameIcon: "pubg_taiwan.png", gameObb: "", link: "https://www.pubgmobile.com/" }
            ];
            
            res.json({
                status: true,
                data: {
                    EXP: expDate, exdate: expDate, expired_date: expDate,
                    appVersion: appVersion, appVersionString: appVersion,
                    firebase_database_url: "https://abdi-vip-panel-default-rtdb.firebaseio.com",
                    databaseUrl: "https://abdi-vip-panel-default-rtdb.firebaseio.com",
                    GAME_LIST_ICON: ["pubg_global.png", "pubg_korea.png", "pubg_vietnam.png", "pubg_taiwan.png"],
                    GAME_LIST_PKG: ["com.tencent.ig", "com.pubg.krmobile", "com.vng.pubgmobile", "com.rekoo.pubgm"],
                    STATUS_BY: "Latest Version",
                    USER_ID: userId,
                    game_list: gameList,
                    games: gameList
                }
            });
        } else {
            res.json({ status: true, success: true });
        }
    } catch (error) {
        res.json({ status: false, data: { EXP: '', exdate: '', expired_date: '' }, reason: 'INVALID' });
    }
});


// ===== ZOON MOD /connect ENDPOINT =====
function parseLoaderBody(rawBody) {
    if (!rawBody) return {};
    let body = rawBody;
    if (typeof body === 'string') {
        try { return JSON.parse(body); } catch (e) {}
        if (body.includes('=')) {
            const params = new URLSearchParams(body);
            const obj = {};
            for (const [k, v] of params) obj[k] = v;
            return obj;
        }
    }
    return body || {};
}

app.post('/connect', (req, res) => {
    console.log('=== /connect REQUEST ===');
    console.log('Body:', JSON.stringify(req.body));
    console.log('Headers:', JSON.stringify(req.headers));
    console.log('Query:', JSON.stringify(req.query));
    try {
        const body = parseLoaderBody(req.body);
        const licKey = body.user_key || body.key || body.license_key || '';
        const deviceId = body.serial || body.device_id || '';
        const game = body.game || '';
        
        if (!licKey) {
            return res.json({ status: false, data: { EXP: '' }, reason: 'INVALID' });
        }
        
        const lic = queryOne('SELECT * FROM licenses WHERE license_key = ?', [licKey]);
        if (!lic) {
            return res.json({ status: false, data: { EXP: '' }, reason: 'INVALID' });
        }
        
        const expiry = lic.expires_at || '2026-11-01';
        if (lic.expires_at && new Date(lic.expires_at) < new Date()) {
            return res.json({ status: false, data: { EXP: expiry }, reason: 'FAILED' });
        }
        
        if (lic.status === 'used' && lic.device_id && lic.device_id !== deviceId) {
            return res.json({ status: false, data: { EXP: expiry }, reason: 'FAILED' });
        }
        
        if (lic.status === 'unused') {
            db.run('UPDATE licenses SET status = ?, device_id = ?, used_at = CURRENT_TIMESTAMP WHERE id = ?', ['used', deviceId, lic.id]);
            saveDB();
        }
        
        const appVersion = '4.6.0';
        const gamesList = [
            { gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Global", gameStatus: "Latest Version", gameVersion: "Latest Version", currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion, gamePackage: "com.tencent.ig", gameIcon: "pubg_global.png", gameObb: "", link: "https://www.pubgmobile.com/" },
            { gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Korea", gameStatus: "Latest Version", gameVersion: "Latest Version", currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion, gamePackage: "com.pubg.krmobile", gameIcon: "pubg_korea.png", gameObb: "", link: "https://www.pubgmobile.com/" },
            { gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Vietnam", gameStatus: "Latest Version", gameVersion: "Latest Version", currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion, gamePackage: "com.vng.pubgmobile", gameIcon: "pubg_vietnam.png", gameObb: "", link: "https://www.pubgmobile.com/" },
            { gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Taiwan", gameStatus: "Latest Version", gameVersion: "Latest Version", currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion, gamePackage: "com.rekoo.pubgm", gameIcon: "pubg_taiwan.png", gameObb: "", link: "https://www.pubgmobile.com/" }
        ];
        
        res.json({
            status: true,
            data: {
                EXP: expiry,
                exdate: expiry,
                expired_date: expiry,
                appVersion: appVersion,
                appVersionString: appVersion,
                firebase_database_url: 'https://abdi-vip-panel-default-rtdb.firebaseio.com',
                databaseUrl: 'https://abdi-vip-panel-default-rtdb.firebaseio.com',
                GAME_LIST_ICON: ["pubg_global.png", "pubg_korea.png", "pubg_vietnam.png", "pubg_taiwan.png"],
                GAME_LIST_PKG: ["com.tencent.ig", "com.pubg.krmobile", "com.vng.pubgmobile", "com.rekoo.pubgm"],
                STATUS_BY: 'Latest Version',
                USER_ID: licKey,
                game_list: gamesList,
                games: gamesList
            }
        });
    } catch (error) {
        res.json({ status: false, data: { EXP: '' }, reason: 'INVALID' });
    }
});

app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));
});
