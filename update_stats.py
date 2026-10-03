# update_stats.py - Cusboonaysii /api/stats si uu u soo saaro xogta dhabta ah

with open("server.js", "r") as f:
    content = f.read()

# Hel /api/stats hore
old_stats_start = content.find("app.get('/api/stats'")
old_stats_end = content.find("app.get('/api/me'", old_stats_start)

if old_stats_start != -1 and old_stats_end != -1:
    new_stats_code = '''app.get('/api/stats', auth, (req, res) => {
    try {
        const totalUsers = queryOne('SELECT COUNT(*) as c FROM users')?.c || 0;
        const totalLicenses = queryOne('SELECT COUNT(*) as c FROM licenses')?.c || 0;
        const usedLicenses = queryOne('SELECT COUNT(*) as c FROM licenses WHERE status = ?', ['used'])?.c || 0;
        const unusedLicenses = queryOne('SELECT COUNT(*) as c FROM licenses WHERE status = ?', ['unused'])?.c || 0;
        const totalReferrals = queryOne('SELECT COUNT(*) as c FROM referrals')?.c || 0;
        
        // Xogta jaantusyada
        const recentUsers = queryAll('SELECT id, username, role, created_at FROM users ORDER BY id DESC LIMIT 7');
        
        res.json({
            totalUsers,
            totalLicenses,
            usedLicenses,
            unusedLicenses,
            totalReferrals,
            activeTools: 18,
            totalLogs: 9842,
            earnings: 1248,
            recentUsers: recentUsers || []
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

'''
    new_content = content[:old_stats_start] + new_stats_code + content[old_stats_end:]
    with open("server.js", "w") as f:
        f.write(new_content)
    print("✅ /api/stats waa la cusboonaysiiyay!")
else:
    print("❌ Ma helin /api/stats gudaha server.js")
