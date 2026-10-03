# new_login_system.py - Beddel nidaamka login-ka mid cusub oo fudud

# Akhri server.js
with open("server.js", "r") as f:
    content = f.read()

# Hel meesha /api/login ka bilaabmo
start_login = content.find("app.post('/api/login'")
end_login = content.find("app.get('/api/me'", start_login)

if start_login != -1 and end_login != -1:
    # Koodhka cusub ee login-ka (password kaliya)
    new_login_code = '''app.post('/api/login', async (req, res) => {
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

'''
    
    # Beddel koodhka login-ka
    new_content = content[:start_login] + new_login_code + content[end_login:]
    
    with open("server.js", "w") as f:
        f.write(new_content)
    print("✅ Nidaamka login-ka cusub waa lagu daray server.js!")
else:
    print("❌ Ma helin /api/login ama /api/me gudaha server.js")
