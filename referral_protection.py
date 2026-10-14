# referral_protection.py - Ku qasab referral code marka la isdiiwaangelinayo
import shutil

# Backup
shutil.copy("server.js", "server.js.backup_referral")
shutil.copy("public/index.html", "public/index.html.backup_referral")
print("✅ Backup waa la sameeyay!")

# ===== 1. CUSBOONAYSI SERVER.JS =====
with open("server.js", "r") as f:
    server = f.read()

# Hel /api/register hore
import re
pattern = r"app\.post\('/api/register'.*?\}\);\s*\}\);"
match = re.search(pattern, server, re.DOTALL)

if match:
    new_register = '''app.post('/api/register', async (req, res) => {
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
});'''
    
    server = server[:match.start()] + new_register + server[match.end():]
    with open("server.js", "w") as f:
        f.write(server)
    print("✅ /api/register waa la cusboonaysiiyay (referral protection)!")
else:
    print("⚠️ /api/register lama helin")

# ===== 2. CUSBOONAYSI FRONTEND-KA =====
with open("public/index.html", "r") as f:
    content = f.read()

# Calaamadda handleRegister hore
old_register = "async function handleRegister(e){e.preventDefault();var u=document.getElementById('reg-username').value;var p=document.getElementById('reg-password').value;var f=document.getElementById('reg-fullname').value;"

new_register = "async function handleRegister(e){e.preventDefault();var u=document.getElementById('reg-username').value;var p=document.getElementById('reg-password').value;var f=document.getElementById('reg-fullname').value;var ref=prompt('Geli Referral Code-ka (waa loo baahan yahay ammaanka):');if(!ref||ref.trim()===''){showToast('Warning','Referral code waa loo baahan yahay!','info');return;}ref=ref.trim().toUpperCase();"

if old_register in content:
    content = content.replace(old_register, new_register)
    print("✅ Frontend handleRegister waa la cusboonaysiiyay!")
else:
    print("⚠️ handleRegister lama helin")

# Cusboonaysii body-ga request-ka (ku dar referral_code)
old_body = "body:JSON.stringify({username:u,password:p,fullname:f})"
new_body = "body:JSON.stringify({username:u,password:p,fullname:f,referral_code:ref})"

if old_body in content:
    content = content.replace(old_body, new_body)
    print("✅ Body-ga request-ka waa la cusboonaysiiyay (referral_code)!")

with open("public/index.html", "w") as f:
    f.write(content)
    print("✅ Faylka waa la keydiyay!")

print("🔥 REFERRAL PROTECTION waa dhammaatay!")
