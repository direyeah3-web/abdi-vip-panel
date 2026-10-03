# clean_seed_data.py - Ka saar xogta tusaale ah, sii hay user-ka admin

with open("server.js", "r") as f:
    content = f.read()

# Hel koodhka SEED_DATA hore
start_marker = "// ===== AUTO SEED DATA ====="
end_marker = "app.listen(PORT"

start_pos = content.find(start_marker)
end_pos = content.find(end_marker, start_pos)

if start_pos != -1 and end_pos != -1:
    # Koodhka cusub - kaliya abuur tables iyo admin user
    new_seed_code = '''// ===== AUTO CREATE ADMIN USER =====
if (process.env.SEED_DATA === 'true') {
    try {
        console.log('🌱 Initializing database...');
        
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
        
        // Kaliya abuur user-ka admin haddii uusan jirin
        const adminPass = bcrypt.hashSync('abdi123', 10);
        try {
            db.run("INSERT OR IGNORE INTO users (username, password, fullname, role, referral_code) VALUES (?, ?, ?, ?, ?)", 
                ['abdi', adminPass, 'Abdi Admin', 'admin', 'ABDI2026']);
            console.log('✅ Admin user ready');
        } catch(e) {}
        
        saveDB();
        
        const userCount = queryOne('SELECT COUNT(*) as c FROM users')?.c || 0;
        const licCount = queryOne('SELECT COUNT(*) as c FROM licenses')?.c || 0;
        console.log(`📊 Database ready! Users: ${userCount}, Licenses: ${licCount}`);
    } catch (e) {
        console.log('❌ Init error:', e.message);
    }
}
'''
    
    new_content = content[:start_pos] + new_seed_code + "\n" + content[end_pos:]
    with open("server.js", "w") as f:
        f.write(new_content)
    print("✅ Seed data code waa la nadiifiyay!")
else:
    print("❌ Ma helin SEED_DATA marker")
