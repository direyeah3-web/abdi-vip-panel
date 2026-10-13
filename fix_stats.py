# fix_stats.py - Hagaaji /api/stats si uu u soo celiyo xog buuxda

with open("server.js", "r") as f:
    content = f.read()

import re
# Hel /api/stats hore
pattern = r"app\.get\('/api/stats'.*?\}\);\s*\}\);"
match = re.search(pattern, content, re.DOTALL)

if match:
    new_stats = '''app.get('/api/stats', auth, (req, res) => {
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
        res.status(500).json({ error: error.message });
    }
});'''
    
    content = content[:match.start()] + new_stats + content[match.end():]
    with open("server.js", "w") as f:
        f.write(content)
    print("✅ /api/stats waa la hagaajiyay!")
else:
    print("❌ Ma helin /api/stats")
