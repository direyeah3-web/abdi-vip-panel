# update_stats_v2.py - Cusboonaysii /api/stats (regex version)
import re

with open("server.js", "r") as f:
    content = f.read()

# Raadi /api/stats kasta (hal sadar ama dhowr sadar)
pattern = r"app\.get\('/api/stats'.*?\}\);\s*\}?\s*\);"

match = re.search(pattern, content, re.DOTALL)

if match:
    print("✅ Waxaan helay /api/stats!")
    print("Qoraalka hore:", match.group()[:100] + "...")
    
    # Koodhka cusub
    new_stats_code = '''app.get('/api/stats', auth, (req, res) => {
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
    
    # Beddel
    new_content = content[:match.start()] + new_stats_code + content[match.end():]
    
    with open("server.js", "w") as f:
        f.write(new_content)
    print("✅ /api/stats waa la cusboonaysiiyay!")
else:
    print("❌ Ma helin /api/stats. Fadlan ii soo dir qoraalka:")
    print("grep -n 'api/stats' server.js")
