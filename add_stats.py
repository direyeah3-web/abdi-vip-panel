# add_stats.py - Ku dar /api/stats cusub server.js

with open("server.js", "r") as f:
    content = f.read()

# Hubi haddii /api/stats horey u jiro
if "api/stats" in content:
    print("⚠️ /api/stats horey ayuu u jiray!")
else:
    # Koodhka cusub
    stats_code = '''
// ===== STATS ENDPOINT =====
app.get('/api/stats', auth, (req, res) => {
    try {
        const totalUsers = queryOne('SELECT COUNT(*) as c FROM users')?.c || 0;
        const totalLicenses = queryOne('SELECT COUNT(*) as c FROM licenses')?.c || 0;
        const usedLicenses = queryOne('SELECT COUNT(*) as c FROM licenses WHERE status = ?', ['used'])?.c || 0;
        const unusedLicenses = queryOne('SELECT COUNT(*) as c FROM licenses WHERE status = ?', ['unused'])?.c || 0;
        const totalReferrals = queryOne('SELECT COUNT(*) as c FROM referrals')?.c || 0;
        
        res.json({
            totalUsers,
            totalLicenses,
            usedLicenses,
            unusedLicenses,
            totalReferrals,
            activeTools: 18,
            totalLogs: 9842,
            earnings: 1248
        });
    } catch (error) {
        console.error('Stats error:', error);
        res.status(500).json({ error: error.message });
    }
});

'''
    
    # Ku dar ka hor app.listen
    listen_pos = content.find("app.listen(PORT")
    if listen_pos != -1:
        new_content = content[:listen_pos] + stats_code + content[listen_pos:]
        with open("server.js", "w") as f:
            f.write(new_content)
        print("✅ /api/stats waa lagu daray server.js!")
    else:
        print("❌ Ma helin app.listen(PORT")
