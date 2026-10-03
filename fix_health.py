# fix_health.py - Hagaaji /api/health

with open("server.js", "r") as f:
    content = f.read()

# Hel endpoint-ka health hore
import re
pattern = r"app\.get\('/api/health'.*?\}\);\s*\}\);"
match = re.search(pattern, content, re.DOTALL)

if match:
    new_health = '''app.get('/api/health', (req, res) => {
    try {
        const userCount = queryOne('SELECT COUNT(*) as c FROM users')?.c || 0;
        const licenseCount = queryOne('SELECT COUNT(*) as c FROM licenses')?.c || 0;
        res.json({
            status: 'ok',
            server: 'ABDI VIP PANEL',
            version: '3.0.0',
            node_version: process.version,
            environment: process.env.NODE_ENV || 'production',
            uptime: process.uptime(),
            timestamp: new Date().toISOString(),
            database: {
                users: userCount,
                licenses: licenseCount,
                status: 'connected'
            }
        });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});'''
    
    content = content[:match.start()] + new_health + content[match.end():]
    
    with open("server.js", "w") as f:
        f.write(content)
    print("✅ /api/health waa la hagaajiyay!")
else:
    print("❌ Ma helin /api/health")
