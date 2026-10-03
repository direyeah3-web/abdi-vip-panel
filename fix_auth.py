# fix_auth.py - Beddel auth middleware si uu u aqbalo token-ka cusub

with open("server.js", "r") as f:
    content = f.read()

# Hel auth middleware hore
old_auth_start = content.find("function auth(")
if old_auth_start == -1:
    old_auth_start = content.find("const auth = (")

# Hel meesha uu ku dhammaado (function xigta)
if old_auth_start != -1:
    # Raadi '}' ee ugu horreeya ka dib function-ka
    brace_count = 0
    i = old_auth_start
    found_start = False
    while i < len(content):
        if content[i] == '{':
            brace_count += 1
            found_start = True
        elif content[i] == '}':
            brace_count -= 1
            if found_start and brace_count == 0:
                old_auth_end = i + 1
                break
        i += 1
    
    # Auth middleware cusub (fudud)
    new_auth = '''function auth(req, res, next) {
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
}'''
    
    new_content = content[:old_auth_start] + new_auth + content[old_auth_end:]
    
    with open("server.js", "w") as f:
        f.write(new_content)
    print("✅ Auth middleware waa la beddelay!")
else:
    print("❌ Ma helin auth middleware")
