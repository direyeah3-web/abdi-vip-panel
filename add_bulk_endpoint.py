# add_bulk_endpoint.py - Ku dar endpoint abuura licenses badan

with open("server.js", "r") as f:
    content = f.read()

if "/api/licenses/bulk" in content:
    print("⚠️ Endpoint-ka horey ayuu u jiray!")
else:
    bulk_code = """
// ===== BULK GENERATE LICENSES =====
app.post('/api/licenses/bulk', auth, (req, res) => {
    try {
        const { days, quantity } = req.body;
        const qty = parseInt(quantity) || 1;
        const durationDays = parseInt(days) || 30;
        
        const generated = [];
        for (let i = 0; i < qty; i++) {
            const licenseKey = 'ABDI-' + Math.random().toString(36).substring(2, 10).toUpperCase();
            const expiresAt = new Date();
            expiresAt.setDate(expiresAt.getDate() + durationDays);
            
            db.run("INSERT INTO licenses (license_key, duration, status, expires_at) VALUES (?, ?, ?, ?)", 
                [licenseKey, durationDays + ' days', 'unused', expiresAt.toISOString()]);
            generated.push(licenseKey);
        }
        saveDB();
        
        res.json({ success: true, licenses: generated, count: generated.length });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

"""
    listen_pos = content.find("app.listen(PORT")
    if listen_pos != -1:
        new_content = content[:listen_pos] + bulk_code + content[listen_pos:]
        with open("server.js", "w") as f:
            f.write(new_content)
        print("✅ Endpoint-ka bulk generate waa lagu daray!")
    else:
        print("❌ Ma helin app.listen(PORT")

