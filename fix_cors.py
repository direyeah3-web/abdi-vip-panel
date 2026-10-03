# fix_cors.py - Ku dar CORS middleware

with open("server.js", "r") as f:
    content = f.read()

if "cors" in content and "app.use(cors" in content:
    print("⚠️ CORS middleware horey ayuu u jiray!")
else:
    cors_code = """
// ===== CORS MIDDLEWARE =====
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
    if (req.method === 'OPTIONS') {
        return res.sendStatus(200);
    }
    next();
});

"""
    # Ku dar ka hor app.use(express.json())
    target = "app.use(express.json())"
    target_pos = content.find(target)
    
    if target_pos != -1:
        new_content = content[:target_pos] + cors_code + content[target_pos:]
        with open("server.js", "w") as f:
            f.write(new_content)
        print("✅ CORS middleware waa lagu daray!")
    else:
        print("❌ Ma helin app.use(express.json())")
