# add_ref_endpoint.py - Ku dar endpoint referrals

with open("server.js", "r") as f:
    content = f.read()

if "/api/admin/referrals" in content:
    print("⚠️ Endpoint-ka horey ayuu u jiray!")
else:
    ref_code = """
// ===== REFERRALS LIST =====
app.get('/api/admin/referrals', auth, (req, res) => {
    try {
        const referrals = queryAll('SELECT * FROM referrals ORDER BY id DESC');
        res.json(referrals || []);
    } catch (error) {
        res.json([]);
    }
});

"""
    listen_pos = content.find("app.listen(PORT")
    if listen_pos != -1:
        new_content = content[:listen_pos] + ref_code + content[listen_pos:]
        with open("server.js", "w") as f:
            f.write(new_content)
        print("✅ Endpoint-ka referrals waa lagu daray!")
    else:
        print("❌ Ma helin app.listen(PORT")
