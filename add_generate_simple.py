# add_generate_simple.py - Ku dar endpoint-ka generate license

with open("server.js", "r") as f:
    content = f.read()

if "api/licenses/generate" in content:
    print("⚠️ Endpoint-ka horey ayuu u jiray!")
else:
    gen_code = """
// ===== GENERATE LICENSE =====
app.post('/api/licenses/generate', auth, (req, res) => {
    try {
        const duration = req.body.duration || '30 days';
        const licenseKey = 'ABDI-' + Math.random().toString(36).substring(2, 10).toUpperCase();
        const expiresAt = new Date();
        expiresAt.setDate(expiresAt.getDate() + 30);
        
        db.run("INSERT INTO licenses (license_key, duration, status, expires_at) VALUES (?, ?, ?, ?)", 
            [licenseKey, duration, 'unused', expiresAt.toISOString()]);
        saveDB();
        
        res.json({ success: true, license_key: licenseKey });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

"""
    listen_pos = content.find("app.listen(PORT")
    if listen_pos != -1:
        new_content = content[:listen_pos] + gen_code + content[listen_pos:]
        with open("server.js", "w") as f:
            f.write(new_content)
        print("✅ Endpoint-ka generate license waa lagu daray!")
    else:
        print("❌ Ma helin app.listen(PORT")
