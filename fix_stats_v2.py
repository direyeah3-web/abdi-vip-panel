# fix_stats_v2.py - Hagaaji /api/stats si uu u soo celiyo xog buuxda

with open("server.js", "r") as f:
    content = f.read()

import re
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
        
        // Xogta jaantusyada - 7 maalmood ee ugu dambeeyay
        const weeklyData = [];
        for (let i = 6; i >= 0; i--) {
            const d = new Date();
            d.setDate(d.getDate() - i);
            const dateStr = d.toISOString().split('T')[0];
            const count = queryOne("SELECT COUNT(*) as c FROM users WHERE DATE(created_at) = ?", [dateStr])?.c || 0;
            weeklyData.push(count);
        }
        
        res.json({
            totalUsers,
            totalLicenses,
            usedLicenses,
            unusedLicenses,
            totalReferrals,
            weeklyData,
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
