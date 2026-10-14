require('dotenv').config();
const express = require('express');
const https = require('https');
const TelegramBot = require('node-telegram-bot-api');
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
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_ADMIN_CHAT_ID = process.env.TELEGRAM_ADMIN_CHAT_ID;

// Telegram Bot
let bot = null;
if (TELEGRAM_BOT_TOKEN) {
    bot = new TelegramBot(TELEGRAM_BOT_TOKEN, { polling: true });
    console.log('🤖 Telegram Bot: la diyaariyay');
} else {
    console.log('⚠️  Telegram Bot: TOKEN ma jiro (.env)');
}

// Function: Admin check
function isAdmin(chatId) {
    return String(chatId) === String(TELEGRAM_ADMIN_CHAT_ID);
}

// Function: Abuur license key
function generateLicenseKey(duration) {
    const key = 'ABDI-' + Math.random().toString(36).substring(2, 8).toUpperCase() +
                Math.random().toString(36).substring(2, 8).toUpperCase();
    const expires = new Date();
    if (duration === '1d') expires.setDate(expires.getDate() + 1);
    else if (duration === '7d') expires.setDate(expires.getDate() + 7);
    else if (duration === '30d') expires.setDate(expires.getDate() + 30);
    else if (duration === '90d') expires.setDate(expires.getDate() + 90);
    else if (duration === '1y') expires.setFullYear(expires.getFullYear() + 1);
    else expires.setDate(expires.getDate() + 30);
    
    try {
        db.run('INSERT INTO licenses (license_key, duration, expires_at, status) VALUES (?, ?, ?, ?)',
            [key, duration, expires.toISOString(), 'available']);
        saveDB();
        return { key, expires: expires.toISOString(), duration };
    } catch (err) {
        console.error('License error:', err);
        return null;
    }
}

// Function: Ogeysiin admin-ka
function sendTelegramNotification(message) {
    if (!bot || !TELEGRAM_ADMIN_CHAT_ID) {
        console.log('⚠️  Telegram: ma dirin (bot ama chat_id ma jiro)');
        return;
    }
    bot.sendMessage(TELEGRAM_ADMIN_CHAT_ID, message, { parse_mode: 'HTML' })
        .then(() => console.log('✅ Telegram: notification la diray'))
        .catch(err => console.error('❌ Telegram error:', err.message));
}

app.use(cors());
app.use(bodyParser.json({ limit: '100mb' }));
app.use(bodyParser.urlencoded({ extended: true, limit: '100mb' }));
app.use(express.static('public', {
    setHeaders: (res, path) => {
        if (path.endsWith('index.html')) {
            res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
            res.setHeader('Pragma', 'no-cache');
            res.setHeader('Expires', '0');
        }
    }
}));

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
    try {
        const { username, password, fullname, referral_code } = req.body;
        
        // Xaqiiji xogta
        if (!username || !password) {
            return res.status(400).json({ success: false, message: 'Username iyo password waa loo baahan yahay' });
        }
        
        // ===== HUBI REFERRAL CODE (AMMAANKA) =====
        if (!referral_code || String(referral_code).trim() === '') {
            return res.status(403).json({ 
                success: false, 
                message: 'Referral code waa loo baahan yahay! Codsi code-ka admin-ka.' 
            });
        }
        
        // Hubi haddii referral code uu sax yahay (database-ka)
        const refCode = String(referral_code).trim().toUpperCase();
        const validReferral = queryOne('SELECT id, username FROM users WHERE referral_code = ?', [refCode]);
        
        if (!validReferral) {
            return res.status(403).json({ 
                success: false, 
                message: 'Referral code-ka waa khaldan yahay! Codsi code sax ah.' 
            });
        }
        
        // Hubi haddii user-ku horey u jiray
        const existing = queryOne('SELECT id FROM users WHERE username = ?', [username]);
        if (existing) {
            return res.status(400).json({ success: false, message: 'User-ku horey ayuu u jiray' });
        }
        
        // Abuur user cusub
        const hashed = await bcrypt.hash(password, 10);
        const myRef = 'ABDI' + Math.random().toString(36).substring(2, 8).toUpperCase();
        
        db.run("INSERT INTO users (username, password, fullname, role, referral_code, referred_by) VALUES (?, ?, ?, ?, ?, ?)", 
            [username, hashed, fullname || username, 'user', myRef, validReferral.username]);
        saveDB();
        
        // Telegram notification — user cusub
        sendTelegramNotification(
            '🆕 <b>User Cusub!</b>\n\n' +
            '👤 Username: <b>' + username + '</b>\n' +
            '🔑 Referral Code: <code>' + (refCode || 'N/A') + '</code>\n' +
            '👥 Referred By: <b>' + (validReferral ? validReferral.username : 'N/A') + '</b>\n' +
            '🕐 Waqti: ' + new Date().toLocaleString()
        );
        
        // Diiwaangeli referral-ka
        db.run("INSERT INTO referrals (referrer_code, referred_user) VALUES (?, ?)", 
            [refCode, username]);
        saveDB();
        
        const user = queryOne('SELECT * FROM users WHERE username = ?', [username]);
        const token = jwt.sign({ id: user.id, username: user.username, role: user.role }, SECRET);
        
        res.json({
            success: true,
            token: token,
            user: {
                id: user.id,
                username: user.username,
                fullname: user.fullname,
                role: user.role,
                referral_code: user.referral_code
            }
        });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
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
app.get('/api/health', (req, res) => {
    try {
        const userCount = queryOne('SELECT COUNT(*) as c FROM users')?.c || 0;
        const licCount = queryOne('SELECT COUNT(*) as c FROM licenses')?.c || 0;
        res.json({
            status: 'ok',
            server: 'ABDI VIP PANEL',
            version: '3.0.0',
            node_version: process.version,
            environment: process.env.NODE_ENV || 'production',
            uptime: Math.floor(process.uptime()),
            timestamp: new Date().toISOString(),
            database: {
                users: userCount,
                licenses: licCount,
                status: 'connected'
            }
        });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});

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


// ===== STATS ENDPOINT (for dashboard) =====
app.get('/api/stats', auth, (req, res) => {
    try {
        const totalUsers = queryOne('SELECT COUNT(*) as c FROM users')?.c || 0;
        const totalLicenses = queryOne('SELECT COUNT(*) as c FROM licenses')?.c || 0;
        const usedLicenses = queryOne('SELECT COUNT(*) as c FROM licenses WHERE status = ?', ['used'])?.c || 0;
        const unusedLicenses = queryOne('SELECT COUNT(*) as c FROM licenses WHERE status = ?', ['unused'])?.c || 0;
        const totalReferrals = queryOne('SELECT COUNT(*) as c FROM referrals')?.c || 0;
        
        res.json({
            totalUsers,
            totalLicenses,
            usedLicenses,
            unusedLicenses,
            totalReferrals,
            activeTools: 18,
            totalLogs: 9842,
            earnings: 1248
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});


// ===== WORKER CHECK ENDPOINT =====
app.get('/api/worker-check', async (req, res) => {
    try {
        const startTime = Date.now();
        const workerUrl = req.query.worker_url || 'https://a.dirxx.workers.dev';
        try {
            const response = await fetch(workerUrl, { method: 'HEAD' });
            const responseTime = Date.now() - startTime;
            const contentType = response.headers.get('content-type') || '';
            const isJson = contentType.includes('application/json');
            const isProxied = response.headers.get('x-railway-edge') !== null;
            res.json({
                status: response.ok ? 'online' : 'error',
                worker_url: workerUrl,
                response_time: responseTime + 'ms',
                http_status: response.status,
                content_type: contentType,
                is_json: isJson,
                is_proxied: isProxied,
                reachable: response.ok,
                message: isProxied ? 'Worker-ku wuxuu u gudbiyaa Railway si guul leh!' : (isJson ? 'Worker-ku wuu shaqeynayaa (JSON)' : 'Worker-ku wuxuu soo celiyaa HTML'),
                timestamp: new Date().toISOString()
            });
        } catch (fetchError) {
            const responseTime = Date.now() - startTime;
            res.json({
                status: 'offline',
                worker_url: workerUrl,
                response_time: responseTime + 'ms',
                reachable: false,
                error: fetchError.message,
                timestamp: new Date().toISOString()
            });
        }
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});

// Telegram — Test endpoint
// Telegram — Status endpoint
app.get('/api/telegram/status', auth, adminOnly, async (req, res) => {
    try {
        if (!bot) {
            return res.json({ 
                success: true, 
                online: false, 
                error: 'Bot ma jiro — .env hubi' 
            });
        }
        if (!TELEGRAM_BOT_TOKEN) {
            return res.json({ 
                success: true, 
                online: false, 
                error: 'Token ma jiro' 
            });
        }
        // Hubi bot-ka getMe
        const https = require('https');
        const botInfo = await new Promise((resolve, reject) => {
            https.get('https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/getMe', (r) => {
                let data = '';
                r.on('data', chunk => data += chunk);
                r.on('end', () => {
                    try { resolve(JSON.parse(data)); } 
                    catch(e) { reject(e); }
                });
            }).on('error', reject);
        });
        
        if (botInfo && botInfo.ok) {
            res.json({
                success: true,
                online: true,
                username: botInfo.result.username,
                name: botInfo.result.first_name,
                polling: true,
                version: '3.0.0',
                node: process.version,
                uptime: Math.floor(process.uptime()),
                chat_id: TELEGRAM_ADMIN_CHAT_ID
            });
        } else {
            res.json({
                success: true,
                online: false,
                error: botInfo.description || 'Bot ma shaqeynayo'
            });
        }
    } catch (err) {
        res.json({ 
            success: true, 
            online: false, 
            error: err.message 
        });
    }
});

app.post('/api/telegram/test', auth, adminOnly, async (req, res) => {
    try {
        if (!bot) {
            return res.status(400).json({ success: false, error: 'Bot ma jiro — .env hubi' });
        }
        if (!TELEGRAM_ADMIN_CHAT_ID) {
            return res.status(400).json({ success: false, error: 'Chat ID ma jiro' });
        }
        const testMsg = '🧪 <b>Test Message</b>\n\n✅ Telegram Bot wuu shaqaynayaa!\n🕐 ' + new Date().toLocaleString();
        await bot.sendMessage(TELEGRAM_ADMIN_CHAT_ID, testMsg, { parse_mode: 'HTML' });
        res.json({ success: true, message: 'Test message la diray!' });
    } catch (err) {
        console.error('Telegram test error:', err);
        res.status(500).json({ success: false, error: err.message });
    }
});

// ===== TELEGRAM BOT HANDLERS =====
if (bot) {
    // /start
    bot.onText(/\/start/, (msg) => {
        const chatId = msg.chat.id;
        if (isAdmin(chatId)) {
            bot.sendMessage(chatId,
                '<b>╔══════════════════════════╗</b>\n' +
                '<b>║   👋 WELCOME ADMIN   ║</b>\n' +
                '<b>╚══════════════════════════╝</b>\n\n' +
                '📋 <b>Commands-ka la heli karo:</b>\n\n' +
                '<b>🔑 LICENSE GENERATOR:</b>\n' +
                '<code>/gen 1d</code>  — 1 maalin\n' +
                '<code>/gen 7d</code>  — 7 maalin\n' +
                '<code>/gen 30d</code> — 30 maalin\n' +
                '<code>/gen 90d</code> — 90 maalin\n' +
                '<code>/gen 1y</code>  — 1 sano\n\n' +
                '<b>📊 XOGTA:</b>\n' +
                '<code>/stats</code> — Xogta panel-ka\n' +
                '<code>/help</code>  — Caawimaad\n\n' +
                '<b>━━━━━━━━━━━━━━━━━━━━━━</b>\n' +
                '<b>🛡️ ABDI VIP PANEL</b>',
                { parse_mode: 'HTML' }
            );
        } else {
            bot.sendMessage(chatId, '⛔ Kaliya admin-ka ayaa isticmaali kara bot-kan.');
        }
    });

    // /help
    bot.onText(/\/help/, (msg) => {
        const chatId = msg.chat.id;
        if (!isAdmin(chatId)) {
            bot.sendMessage(chatId, '⛔ Kaliya admin-ka.');
            return;
        }
        bot.sendMessage(chatId,
            '📋 <b>License Generator Commands:</b>\n\n' +
            '<code>/gen 1d</code> — 1 maalin\n' +
            '<code>/gen 7d</code> — 7 maalin\n' +
            '<code>/gen 30d</code> — 30 maalin\n' +
            '<code>/gen 90d</code> — 90 maalin\n' +
            '<code>/gen 1y</code> — 1 sano\n\n' +
            '/stats — Xogta panel-ka',
            { parse_mode: 'HTML' }
        );
    });

    // /stats
    bot.onText(/\/stats/, (msg) => {
        const chatId = msg.chat.id;
        if (!isAdmin(chatId)) {
            bot.sendMessage(chatId, '⛔ Kaliya admin-ka.');
            return;
        }
        try {
            const users = queryOne('SELECT COUNT(*) as c FROM users');
            const licenses = queryOne('SELECT COUNT(*) as c FROM licenses');
            const available = queryOne("SELECT COUNT(*) as c FROM licenses WHERE status = 'available'");
            const referrals = queryOne('SELECT COUNT(*) as c FROM referrals');
            bot.sendMessage(chatId,
                '📊 <b>ABDI VIP PANEL — Stats</b>\n\n' +
                '👥 Users: <b>' + (users ? users.c : 0) + '</b>\n' +
                '🔑 Licenses: <b>' + (licenses ? licenses.c : 0) + '</b>\n' +
                '✅ Available: <b>' + (available ? available.c : 0) + '</b>\n' +
                '🎯 Referrals: <b>' + (referrals ? referrals.c : 0) + '</b>',
                { parse_mode: 'HTML' }
            );
        } catch (err) {
            bot.sendMessage(chatId, '❌ Error: ' + err.message);
        }
    });

    // /gen
    bot.onText(/\/gen(?:\s+(.+))?/, (msg, match) => {
        const chatId = msg.chat.id;
        if (!isAdmin(chatId)) {
            bot.sendMessage(chatId, '⛔ Kaliya admin-ka ayaa license abuuri kara.');
            return;
        }
        const duration = (match[1] || '30d').trim().toLowerCase();
        const validDurations = ['1d', '7d', '30d', '90d', '1y'];
        if (!validDurations.includes(duration)) {
            bot.sendMessage(chatId,
                '⚠️ Duration khaldan!\n\nIsticmaal: <code>/gen 30d</code>\n\n' +
                'Doorashooyin: 1d, 7d, 30d, 90d, 1y',
                { parse_mode: 'HTML' }
            );
            return;
        }
        const result = generateLicenseKey(duration);
        if (result) {
            const keyboard = {
                reply_markup: {
                    inline_keyboard: [
                        [{ text: '📋 COPY CODE', copy_text: { text: result.key } }]
                    ]
                }
            };
            bot.sendMessage(chatId,
                '<b>╔══════════════════════════╗</b>\n' +
                '<b>║   ✅ LICENSE KEY LA ABUURAY   ║</b>\n' +
                '<b>╚══════════════════════════╝</b>\n\n' +
                '🔑 <b>License Key:</b>\n' +
                '<code>' + result.key + '</code>\n\n' +
                '⏱️ <b>Duration:</b> ' + result.duration + '\n' +
                '📅 <b>Expires:</b> ' + new Date(result.expires).toLocaleString() + '\n' +
                '📊 <b>Status:</b> Available\n\n' +
                '<b>━━━━━━━━━━━━━━━━━━━━━━</b>\n' +
                '<b>🛡️ ABDI VIP PANEL</b>',
                Object.assign({ parse_mode: 'HTML' }, keyboard)
            );
        } else {
            bot.sendMessage(chatId, '❌ License abuurista waa guuldareysatay.');
        }
    });

    // Callback query handler (COPY CODE, STATS)
    bot.on('callback_query', (query) => {
        const chatId = query.message.chat.id;
        const data = query.data;
        if (!isAdmin(chatId)) {
            bot.answerCallbackQuery(query.id, { text: '⛔ Kaliya admin-ka.' });
            return;
        }
        if (data.startsWith('copy_')) {
            const key = data.replace('copy_', '');
            bot.answerCallbackQuery(query.id, { text: '✅ ' + key + ' waa la koobiyay!', show_alert: false });
        } else if (data === 'stats') {
            try {
                const users = queryOne('SELECT COUNT(*) as c FROM users');
                const licenses = queryOne('SELECT COUNT(*) as c FROM licenses');
                const available = queryOne("SELECT COUNT(*) as c FROM licenses WHERE status = 'available'");
                const referrals = queryOne('SELECT COUNT(*) as c FROM referrals');
                bot.sendMessage(chatId,
                    '📊 <b>ABDI VIP PANEL — Stats</b>\n\n' +
                    '👥 Users: <b>' + (users ? users.c : 0) + '</b>\n' +
                    '🔑 Licenses: <b>' + (licenses ? licenses.c : 0) + '</b>\n' +
                    '✅ Available: <b>' + (available ? available.c : 0) + '</b>\n' +
                    '🎯 Referrals: <b>' + (referrals ? referrals.c : 0) + '</b>',
                    { parse_mode: 'HTML' }
                );
            } catch (err) {
                bot.sendMessage(chatId, '❌ Error: ' + err.message);
            }
        }
        bot.answerCallbackQuery(query.id);
    });

    console.log('🤖 Telegram Bot: handlers la diyaariyay');
}

// ===== CLOUDFLARE WORKER ENDPOINTS =====
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
            // Nadiifi boundary lines — kaliya code-ka
            let cleanCode = text;
            const exportIdx = cleanCode.indexOf('export default');
            if (exportIdx > 0) {
                cleanCode = cleanCode.substring(exportIdx);
            }
            // Ka saar boundary line-ka ugu dambeeya (--boundary--)
            const lastBoundary = cleanCode.lastIndexOf('\n--');
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
        // Native FormData (Node 18+) — multipart/form-data
        const form = new FormData();
        form.append('metadata', new Blob([JSON.stringify({
            main_module: 'worker.js',
            compatibility_date: '2024-01-01'
        })], { type: 'application/json' }), 'metadata.json');
        form.append('worker.js', new Blob([code], { type: 'application/javascript+module' }), 'worker.js');
        const r = await fetch(url, {
            method: 'PUT',
            headers: { 'Authorization': 'Bearer ' + token },
            body: form
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

// ===== APK ANALYZER ENDPOINTS =====
const AdmZip = require('adm-zip');

// Extract essential loader info — server URL, endpoint, response format
function extractEssential(allUrls, dexFiles) {
    const essential = {
        server_url: null,
        endpoint: null,
        full_url: null,
        response_format: null,
        source_ip: null,
        license_methods: [],
        json_fields: []
    };

    // 1. Filter server URLs — ma aha schemas.android.com, crbug, google.com
    const ignoreHosts = ['schemas.android.com', 'crbug.com', 'google.com', 'googleapis.com', 'github.com', 'shizuku.rikka.app', 'curl.se', 'llvm.org', 'DeNA'];
    const serverUrls = allUrls.filter(u => {
        const url = u.url || '';
        // Ka saar format strings
        if (url.includes('%s') || url.includes('%d')) return false;
        // Ka saar native libs — DEX kaliya
        if (u.file && u.file.includes('lib/')) return false;
        // Ka saar useless URLs
        if (url.includes('schemas.android.com') || url.includes('crbug.com') || url.includes('google.com') || url.includes('github.com') || url.includes('curl.se') || url.includes('llvm.org') || url.includes('DeNA')) return false;
        return url.startsWith('http');
    });

    if (serverUrls.length > 0) {
        essential.server_url = serverUrls[0].url;
        essential.full_url = serverUrls[0].url;
        // Endpoint ka soo qaado
        const urlObj = serverUrls[0].url;
        const pathMatch = urlObj.match(/https?:\/\/[^\/]+(\/[^\s"']*)?/);
        if (pathMatch && pathMatch[1]) {
            essential.endpoint = pathMatch[1];
        } else {
            essential.endpoint = '/';
        }
    }

    // 2. DEX — license methods + JSON fields
    const methodKw = ['login', 'validate', 'checkLicense', 'verifyLicense', 'auth', 'connect', 'statusTrue', 'isValid', 'performLogin', 'nativeValidateLicense', 'checkKey'];
    const jsonKw = ['"status"', '"success"', '"data"', '"reason"', '"EXP"', '"expired_date"', '"license"', '"key"', '"valid"', '"message"'];

    for (const dex of dexFiles) {
        // Dex waa la baadhay horey — kaliya soo qaado keyword-yada
    }

    return essential;
}

// Parse AndroidManifest.xml (binary XML)
function parseManifest(buf) {
    const result = { package_name: null, launcher: null, application: null, permissions: [] };
    try {
        const str = buf.toString('latin1');
        // Package name: usually near "package" attribute
        const pkgMatch = str.match(/(com\.[a-z0-9_]+\.[a-z0-9_.]+)/i);
        if (pkgMatch) result.package_name = pkgMatch[1];
        // Launcher activity: contains "android.intent.action.MAIN" + "LAUNCHER"
        const actMatches = str.match(/([A-Z][a-zA-Z0-9_]*(?:Activity|MainActivity))/g);
        if (actMatches) result.launcher = actMatches[actMatches.length - 1];
        // Application class
        const appMatches = str.match(/([A-Z][a-zA-Z0-9_]*Application)/g);
        if (appMatches) result.application = appMatches[appMatches.length - 1];
        // Permissions
        const permMatches = str.match(/android\.permission\.[A-Z_]+/g) || [];
        result.permissions = [...new Set(permMatches)];
    } catch (e) {}
    return result;
}
const crypto = require('crypto');

// POST /api/apk/upload — APK soo geli (base64)
app.post('/api/apk/upload', auth, adminOnly, async (req, res) => {
    try {
        const { filename, data } = req.body;
        if (!filename || !data) {
            return res.status(400).json({ success: false, error: 'filename iyo data waa loo baahan yahay' });
        }
        const buffer = Buffer.from(data, 'base64');
        const hash = crypto.createHash('md5').update(buffer).digest('hex');
        const tempPath = '/tmp/apk_' + hash + '.apk';
        const fs = require('fs');
        fs.writeFileSync(tempPath, buffer);
        res.json({
            success: true,
            filename: filename,
            size: buffer.length,
            hash: hash,
            path: tempPath,
            message: 'APK la keydiyay — analyze samee'
        });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

// POST /api/apk/analyze — APK baadh
app.post('/api/apk/analyze', auth, adminOnly, async (req, res) => {
    try {
        const { apkPath, filename } = req.body;
        if (!apkPath) return res.status(400).json({ success: false, error: 'apkPath waa loo baahan yahay' });
        const fs = require('fs');
        const { execSync } = require('child_process');
        if (!fs.existsSync(apkPath)) return res.status(400).json({ success: false, error: 'APK ma jiro' });

        const zip = new AdmZip(apkPath);
        const entries = zip.getEntries();
        const tmpDir = '/tmp/apk_extract_' + Date.now();
        fs.mkdirSync(tmpDir, { recursive: true });

        // Soo qaado dhammaan entries
        for (const entry of entries) {
            const target = tmpDir + '/' + entry.entryName;
            if (!entry.isDirectory) {
                const dir = require('path').dirname(target);
                fs.mkdirSync(dir, { recursive: true });
                fs.writeFileSync(target, entry.getData());
            }
        }

        const result = {
            // 1. APK identification
            package_name: 'N/A',
            launcher_activity: 'N/A',
            application_class: 'N/A',
            dex_files: [],
            native_libs: [],
            assets: [],
            // 2. License check
            license_routines: [],
            // 3. URLs
            urls: [],
            // 4. Signature verification
            signature_checks: [],
            // 5. Integrity / anti-tamper
            integrity_checks: [],
            // 6. Native methods (JNI)
            native_methods: [],
            jni_exports: [],
            // 7. Hermes bytecode
            hermes: null
        };

        // ===== 1. APK identification (AndroidManifest.xml) =====
        const manifestPath = tmpDir + '/AndroidManifest.xml';
        if (fs.existsSync(manifestPath)) {
            try {
                const buf = fs.readFileSync(manifestPath);
                const manifest = parseManifest(buf);
                result.package_name = manifest.package_name || 'N/A';
                result.launcher_activity = manifest.launcher || 'N/A';
                result.application_class = manifest.application || 'N/A';
                result.permissions = manifest.permissions || [];
            } catch (e) {}
        }

        // ===== DEX files =====
        const dexList = entries.filter(e => e.entryName.match(/^classes[0-9]*\.dex$/)).map(e => e.entryName);
        result.dex_files = dexList;

        // ===== Native libs =====
        const nativeList = entries.filter(e => e.entryName.match(/^lib\/.*\.so$/)).map(e => e.entryName);
        result.native_libs = nativeList;

        // ===== Assets =====
        const assetList = entries.filter(e => e.entryName.startsWith('assets/') && !e.isDirectory).map(e => e.entryName);
        result.assets = assetList;

        // ===== 2-6. DEX analysis =====
        const licenseKw = ['LicenseManager', 'AuthManager', 'PanelLicense', 'LoginActivity', 'LoginModule', 'activateSdk', 'MetaActivationManager', 'BuildSeal', 'validateLicense', 'nativeValidateLicense', 'checkLicense', 'statusTrue', 'isValid', 'is_valid', 'performLogin'];
        const urlRegex = /https?:\/\/[^\x00-\x20"']+/g;
        const sigKw = ['getPackageInfo', 'GET_SIGNATURES', 'GET_SIGNING_CERTIFICATES', 'Signature', 'MessageDigest', 'SHA-256', 'SHA-1', 'X509Certificate', 'certSha256', 'OFFICIAL_CERT', 'expectedHash'];
        const integKw = ['SafetyNet', 'PlayIntegrity', 'IntegrityToken', 'Frida', 'frida', 'ptrace', 'TracerPid', 'Magisk', 'zygisk', 'Xposed', 'Substrate', 'ro.debuggable', 'ro.kernel.qemu', 'goldfish', 'ranchu', 'qemu_pipe', 'test-keys'];
        const nativeKw = ['native ', 'nativeValidate', 'nativeEnsure'];

        for (const entry of entries) {
            const name = entry.entryName;
            if (!name.endsWith('.dex')) continue;

            try {
                const buf = entry.getData();
                const str = buf.toString('latin1');
                const lines = str.split('\n');

                // URLs
                const urlMatches = str.match(urlRegex) || [];
                urlMatches.forEach(u => result.urls.push({ file: name, line: 0, url: u }));

                // License routines
                lines.forEach((line, idx) => {
                    if (licenseKw.some(k => line.includes(k))) {
                        result.license_routines.push({ file: name, line: idx + 1, match: line.trim().substring(0, 200) });
                    }
                });

                // Signature
                lines.forEach((line, idx) => {
                    if (sigKw.some(k => line.includes(k))) {
                        result.signature_checks.push({ file: name, line: idx + 1, match: line.trim().substring(0, 200) });
                    }
                });

                // Integrity
                lines.forEach((line, idx) => {
                    if (integKw.some(k => line.includes(k))) {
                        result.integrity_checks.push({ file: name, line: idx + 1, match: line.trim().substring(0, 200) });
                    }
                });

                // Native methods
                lines.forEach((line, idx) => {
                    if (nativeKw.some(k => line.includes(k))) {
                        result.native_methods.push({ file: name, line: idx + 1, match: line.trim().substring(0, 200) });
                    }
                });
            } catch (e) {}
        }

        // ===== 3. URLs in assets =====
        for (const entry of entries) {
            if (!entry.entryName.startsWith('assets/')) continue;
            try {
                const buf = entry.getData();
                const str = buf.toString('latin1');
                const urlMatches = str.match(urlRegex) || [];
                urlMatches.forEach(u => result.urls.push({ file: entry.entryName, line: 0, url: u }));
            } catch (e) {}
        }

        // ===== 4-5. Signature + Integrity in native libs =====
        for (const entry of entries) {
            if (!entry.entryName.startsWith('lib/') || !entry.entryName.endsWith('.so')) continue;
            try {
                const buf = entry.getData();
                const str = buf.toString('latin1');
                const urlMatches = str.match(urlRegex) || [];
                urlMatches.forEach(u => result.urls.push({ file: entry.entryName, line: 0, url: u }));

                // JNI exports
                const jniMatches = str.match(/Java_[a-zA-Z0-9_]+/g) || [];
                jniMatches.forEach(j => result.jni_exports.push({ file: entry.entryName, symbol: j }));

                // Integrity in native
                sigKw.concat(integKw).forEach(kw => {
                    if (str.includes(kw)) {
                        result.signature_checks.push({ file: entry.entryName, line: 0, match: 'native: ' + kw });
                    }
                });
            } catch (e) {}
        }

        // ===== 7. Hermes bytecode =====
        const bundlePath = tmpDir + '/assets/index.android.bundle';
        if (fs.existsSync(bundlePath)) {
            try {
                const buf = fs.readFileSync(bundlePath);
                const magic = buf.slice(0, 8).toString('hex');
                const version = buf.readUInt32LE(8);
                const str = buf.toString('latin1');
                const urlMatches = str.match(urlRegex) || [];
                urlMatches.forEach(u => result.urls.push({ file: 'assets/index.android.bundle', line: 0, url: u }));
                const licMatches = str.match(/(validateLicense|license|LicenseManager|isValid|statusTrue)/g) || [];
                result.hermes = {
                    magic: magic,
                    version: version,
                    size: buf.length,
                    license_hits: [...new Set(licMatches)]
                };
            } catch (e) {}
        }

        // Clean up
        try { execSync('rm -rf ' + tmpDir); } catch (e) {}

        // Counts
        result.urls_count = result.urls.length;
        result.license_count = result.license_routines.length;
        result.signature_count = result.signature_checks.length;
        result.integrity_count = result.integrity_checks.length;
        result.native_count = result.native_methods.length;
        result.jni_count = result.jni_exports.length;
        result.essential = extractEssential(result.urls, result.dex_files);
        result.filename = filename;
        result.success = true;

        res.json(result);
    } catch (err) {
        console.error('APK analyze error:', err);
        res.status(500).json({ success: false, error: err.message });
    }
});

// ===== LOADER HELPER ENDPOINT =====
app.post('/api/loader/helper', auth, adminOnly, async (req, res) => {
    try {
        const { analysis, serverUrl } = req.body;
        if (!analysis) return res.status(400).json({ success: false, error: 'analysis waa loo baahan yahay' });

        const helper = {
            server_location: 'unknown',
            server_url_real: null,
            server_source: null,
            patch_method: 'unknown',
            patch_steps: [],
            license_flow: [],
            response_format: null,
            code_snippet: null,
            worker_template: null,
            url_locations: []
        };

        const urls = analysis.urls || [];
        const nativeLibs = analysis.native_libs || [];
        const dexFiles = analysis.dex_files || [];

        // 1. Raadi URL-ka dhabta ah — DEX miyaa mise native
        const ignoreHosts = ['schemas.android.com', 'crbug.com', 'google.com', 'googleapis.com', 'github.com', 'shizuku.rikka.app', 'curl.se', 'llvm.org', 'DeNA', 'play.google.com'];

        // DEX URLs
        const dexUrls = urls.filter(u => {
            if (!u.file || !u.file.endsWith('.dex')) return false;
            if (!u.url || !u.url.startsWith('http')) return false;
            if (u.url.includes('%s') || u.url.includes('%d')) return false;
            if (ignoreHosts.some(h => u.url.includes(h))) return false;
            return true;
        });

        // Native URLs
        const nativeUrls = urls.filter(u => {
            if (!u.file || !u.file.includes('lib/')) return false;
            if (!u.url || !u.url.startsWith('http')) return false;
            if (u.url.includes('%s') || u.url.includes('%d')) return false;
            if (ignoreHosts.some(h => u.url.includes(h))) return false;
            return true;
        });

        // 2. Go'aanso location + URL-ka dhabta ah
        if (dexUrls.length > 0) {
            helper.server_location = 'dex';
            helper.server_url_real = dexUrls[0].url;
            helper.server_source = dexUrls[0].file + ' : L' + dexUrls[0].line;
            helper.patch_method = 'smali / DEX editor (NP Manager, MT Manager)';
            helper.patch_steps = [
                'NP Manager fur → APK fur → DEX Editor',
                'Raadi: ' + dexUrls[0].url,
                'Beddel: ' + (serverUrl || dexUrls[0].url),
                'Save → Sign APK'
            ];
        } else if (nativeUrls.length > 0) {
            helper.server_location = 'native';
            helper.server_url_real = nativeUrls[0].url;
            helper.server_source = nativeUrls[0].file + ' : L' + nativeUrls[0].line;
            helper.patch_method = 'IDA Pro 7.7 + hex patch';
            helper.patch_steps = [
                'IDA Pro 7.7 fur → ' + nativeUrls[0].file,
                'Raadi string: ' + nativeUrls[0].url,
                'Beddel URL-ka (hex patch)',
                'Save → APK repack'
            ];
        } else {
            helper.server_location = 'unknown';
            helper.patch_method = 'Baadh APK-ga dheeraad — NP Manager + IDA Pro';
            helper.patch_steps = ['APK-ga baadh dheeraad', 'Hubi DEX + native libs'];
        }

        // 3. URL locations — dhammaan meelaha
        helper.url_locations = urls.filter(u => u.url && u.url.startsWith('http') && !ignoreHosts.some(h => u.url.includes(h))).map(u => ({
            file: u.file,
            line: u.line,
            url: u.url
        }));

        // 4. License flow — DYNAMIC (ka soo qaado APK-ga)
        const licenseRoutines = analysis.license_routines || [];
        helper.license_flow = [
            '1. Panel-ka → Licenses → Generate License',
            '2. Loader-ka → Key geli → ' + (helper.server_url_real || serverUrl || 'N/A'),
            '3. Loader-ku server-ka wacayaa: ' + (helper.server_location === 'dex' ? 'DEX' : helper.server_location === 'native' ? 'Native (JNI)' : 'Unknown'),
            '4. Server-ka → Database hubin (license_key)',
            '5. Server-ka → JSON response',
            '6. Loader-ku → response akhriyaa → login/deny'
        ];
        if (licenseRoutines.length > 0) {
            helper.license_flow.push('License methods la helay: ' + licenseRoutines.slice(0, 3).map(l => l.file + ' L' + l.line).join(', '));
        }

        // 5. Response format — DYNAMIC (ka soo qaado APK analysis)
        const dexStrings = analysis.dex_strings || {};
        // Haddii aan la helin dex_strings, isticmaal APK-ga signature checks si loo ogaado fields
        const responseFields = [];
        if (dexStrings.fields && dexStrings.fields.length > 0) {
            dexStrings.fields.forEach(f => responseFields.push(f));
        } else {
            // Default fields (kuwa caadiga ah ee loader-ka)
            responseFields.push('status', 'success', 'data', 'reason', 'EXP', 'expired_date');
        }

        helper.response_format = {
            valid: {
                status: true,
                success: true,
                data: {
                    EXP: 'YYYY-MM-DD',
                    expired_date: 'YYYY-MM-DD'
                }
            },
            invalid: {
                status: false,
                success: false,
                data: { EXP: '', expired_date: '' },
                reason: 'INVALID'
            },
            expired: {
                status: false,
                success: false,
                data: { EXP: 'YYYY-MM-DD' },
                reason: 'FAILED'
            },
            fields_detected: responseFields
        };

        // 6. Code snippet — DYNAMIC (server URL-ka dhabta ah)
        const realServer = helper.server_url_real || serverUrl || 'https://a.dirxx.workers.dev';
        helper.code_snippet = '// Loader-ka login code\n' +
            'const SERVER = "' + realServer + '";\n' +
            'const KEY = userInputKey;\n' +
            'const res = await fetch(SERVER, {\n' +
            '  method: "POST",\n' +
            '  headers: { "Content-Type": "application/json" },\n' +
            '  body: JSON.stringify({ user_key: KEY, serial: deviceId, game: "pubg" })\n' +
            '});\n' +
            'const data = await res.json();\n' +
            'if (data.status === true && data.success === true) {\n' +
            '  // LOGIN SUCCESS\n' +
            '} else {\n' +
            '  // LOGIN FAILED — data.reason\n' +
            '}';

        // 7. Worker template
        helper.worker_template = 'export default {\n' +
            '  async fetch(request, env, ctx) {\n' +
            '    const url = new URL(request.url);\n' +
            '    const target = "https://abdi-vip-panel-production.up.railway.app" + url.pathname;\n' +
            '    return fetch(target, {\n' +
            '      method: request.method,\n' +
            '      headers: request.headers,\n' +
            '      body: request.method !== "GET" ? await request.text() : null\n' +
            '    });\n' +
            '  }\n' +
            '};';

        res.json({ success: true, helper: helper });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));
});
