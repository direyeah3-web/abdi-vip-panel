# add_seed_to_server.py - Ku dar koodh abuura seed data marka server-ku bilaabo

with open("server.js", "r") as f:
    content = f.read()

# Koodhka cusub
seed_code = '''
// ===== AUTO SEED DATA =====
if (process.env.SEED_DATA === 'true') {
    try {
        console.log('🌱 Seeding data...');
        
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
        
        // Abuur user admin
        const adminPass = bcrypt.hashSync('abdi123', 10);
        try {
            db.run("INSERT OR IGNORE INTO users (username, password, fullname, role, referral_code) VALUES (?, ?, ?, ?, ?)", 
                ['abdi', adminPass, 'Abdi Admin', 'admin', 'ABDI2026']);
        } catch(e) {}
        
        // Abuur 5 users
        const sampleUsers = [
            ['user1', 'user1pass', 'User One', 'user'],
            ['user2', 'user2pass', 'User Two', 'user'],
            ['user3', 'user3pass', 'User Three', 'user'],
            ['user4', 'user4pass', 'User Four', 'user'],
            ['user5', 'user5pass', 'User Five', 'user']
        ];
        sampleUsers.forEach(([u, p, f, r]) => {
            try {
                const hashed = bcrypt.hashSync(p, 10);
                db.run("INSERT OR IGNORE INTO users (username, password, fullname, role) VALUES (?, ?, ?, ?)", [u, hashed, f, r]);
            } catch(e) {}
        });
        
        // Abuur 10 licenses
        for (let i = 1; i <= 10; i++) {
            const key = 'ABDI-LIC-' + String(i).padStart(4, '0');
            const status = i <= 4 ? 'used' : 'unused';
            const userId = i <= 4 ? i : null;
            try {
                db.run("INSERT OR IGNORE INTO licenses (license_key, user_id, duration, status) VALUES (?, ?, ?, ?)", 
                    [key, userId, '30 days', status]);
            } catch(e) {}
        }
        
        saveDB();
        const userCount = queryOne('SELECT COUNT(*) as c FROM users')?.c || 0;
        const licCount = queryOne('SELECT COUNT(*) as c FROM licenses')?.c || 0;
        console.log(`✅ Seed data created! Users: ${userCount}, Licenses: ${licCount}`);
    } catch (e) {
        console.log('❌ Seed error:', e.message);
    }
}
'''

# Hubi haddii code-ku horey u jiro
if 'SEED_DATA' in content:
    print("⚠️ Code-ku horey ayuu u jiray!")
else:
    # Ku dar ka hor app.listen
    listen_pos = content.find("app.listen(PORT")
    if listen_pos != -1:
        new_content = content[:listen_pos] + seed_code + "\n" + content[listen_pos:]
        with open("server.js", "w") as f:
            f.write(new_content)
        print("✅ Koodhka seed data waa lagu daray server.js!")
    else:
        print("❌ Ma helin app.listen(PORT")
