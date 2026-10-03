// seed_data.js - Ku dar xog tusaale ah database-ka Railway
const initSqlJs = require('sql.js');
const bcrypt = require('bcryptjs');
const fs = require('fs');

const DB_FILE = './abdi.db';

initSqlJs().then(SQL => {
    let db;
    if (fs.existsSync(DB_FILE)) {
        db = new SQL.Database(fs.readFileSync(DB_FILE));
    } else {
        db = new SQL.Database();
    }
    
    console.log("📊 Database-ka waa la furay");
    
    // Abuur tables haddii aysan jirin
    db.run(`CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        fullname TEXT,
        role TEXT DEFAULT 'user',
        license_key TEXT,
        referral_code TEXT,
        referred_by TEXT,
        status TEXT DEFAULT 'active',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);
    
    db.run(`CREATE TABLE IF NOT EXISTS licenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        license_key TEXT UNIQUE,
        user_id INTEGER,
        device_id TEXT,
        duration TEXT,
        expires_at TEXT,
        status TEXT DEFAULT 'unused',
        used_at DATETIME
    )`);
    
    db.run(`CREATE TABLE IF NOT EXISTS referrals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        referrer_code TEXT,
        referred_user TEXT
    )`);
    
    console.log("✅ Tables waa la abuuray");
    
    // Abuur user admin
    const adminPass = bcrypt.hashSync('abdi123', 10);
    try {
        db.run("INSERT OR IGNORE INTO users (username, password, fullname, role, referral_code) VALUES (?, ?, ?, ?, ?)", 
            ['abdi', adminPass, 'Abdi Admin', 'admin', 'ABDI2026']);
        console.log("✅ User 'abdi' waa la abuuray");
    } catch(e) {
        console.log("ℹ️ User 'abdi' horey ayuu u jiray");
    }
    
    // Abuur 5 users oo tusaale ah
    const sampleUsers = [
        ['user1', 'user1pass', 'User One', 'user'],
        ['user2', 'user2pass', 'User Two', 'user'],
        ['user3', 'user3pass', 'User Three', 'user'],
        ['user4', 'user4pass', 'User Four', 'user'],
        ['user5', 'user5pass', 'User Five', 'user']
    ];
    
    sampleUsers.forEach(([username, password, fullname, role]) => {
        try {
            const hashed = bcrypt.hashSync(password, 10);
            db.run("INSERT OR IGNORE INTO users (username, password, fullname, role) VALUES (?, ?, ?, ?)", 
                [username, hashed, fullname, role]);
        } catch(e) {}
    });
    console.log("✅ 5 users oo tusaale ah waa la abuuray");
    
    // Abuur 10 licenses oo tusaale ah
    for (let i = 1; i <= 10; i++) {
        const key = 'ABDI-LIC-' + String(i).padStart(4, '0');
        const status = i <= 4 ? 'used' : 'unused';
        const userId = i <= 4 ? i : null;
        try {
            db.run("INSERT OR IGNORE INTO licenses (license_key, user_id, duration, status) VALUES (?, ?, ?, ?)", 
                [key, userId, '30 days', status]);
        } catch(e) {}
    }
    console.log("✅ 10 licenses oo tusaale ah waa la abuuray");
    
    // Keydi database-ka
    fs.writeFileSync(DB_FILE, Buffer.from(db.export()));
    console.log("✅ Database-ka waa la keydiyay!");
    
    // Hubi tirada
    const userCount = db.exec("SELECT COUNT(*) FROM users")[0].values[0][0];
    const licCount = db.exec("SELECT COUNT(*) FROM licenses")[0].values[0][0];
    console.log(`📊 Total Users: ${userCount}`);
    console.log(`📊 Total Licenses: ${licCount}`);
});
