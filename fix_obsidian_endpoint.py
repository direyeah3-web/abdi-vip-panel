# fix_obsidian_endpoint.py - Beddel /ObsidianAuth/api.php si uu u soo celiyo response-ka dheer

with open("server.js", "r") as f:
    content = f.read()

import re

# Hel endpoint-ka GET /ObsidianAuth/api.php
pattern = r"app\.get\('/ObsidianAuth/api\.php'.*?\}\);\s*\}\);"
match = re.search(pattern, content, re.DOTALL)

if match:
    new_endpoint = '''app.get('/ObsidianAuth/api.php', (req, res) => {
    try {
        const action = req.query.action;
        const licenseKey = req.query.license_key || req.query.key || '';
        const clientVersion = req.query.client_apk_version || '7.51.0';
        
        if (action === 'release_manifest') {
            let expDate = '2026-11-01';
            let duration = '365 days';
            
            // Haddii license key la bixiyay, hubi database-ka
            if (licenseKey) {
                const lic = queryOne('SELECT * FROM licenses WHERE license_key = ?', [licenseKey]);
                if (lic) {
                    expDate = lic.expires_at || '2026-11-01';
                    duration = lic.duration || '365 days';
                }
            }
            
            res.json({
                status: 'success',
                success: true,
                is_valid: true,
                valid: true,
                state: 'online',
                message: 'License valid',
                http_code: 200,
                remaining_seconds: 31536000,
                remaining_text: duration,
                package_name: 'com.pubg.obsidian',
                policy_version: 1,
                documentVersion: '7.51.0',
                version: '7.51.0',
                latest_version: '7.51.0',
                apk: { version: '7.51.0', required: false },
                latest_file: { apk: { version: '7.51.0', required: false } },
                app_update_required: false,
                update_required: false,
                latest_apk_version: '7.51.0',
                data: {
                    EXP: expDate,
                    expires: expDate,
                    remaining_seconds: 31536000,
                    remaining_text: duration,
                    version: '7.51.0',
                    latest_version: '7.51.0',
                    appstatus: true,
                    server_status: true
                },
                appstatus: true,
                server_status: true,
                register: 'ABDI-VIP-REGISTER',
                registered: true,
                client_apk_version: clientVersion
            });
        } else {
            res.json({ status: 'success', success: true });
        }
    } catch (error) {
        res.json({ status: 'failed', success: false, reason: 'ERROR', error: error.message });
    }
});'''
    
    content = content[:match.start()] + new_endpoint + content[match.end():]
    with open("server.js", "w") as f:
        f.write(content)
    print("✅ /ObsidianAuth/api.php waa la beddelay si uu u soo celiyo response-ka dheer!")
else:
    print("❌ Ma helin /ObsidianAuth/api.php")

