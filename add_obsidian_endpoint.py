# add_obsidian_endpoint.py - Ku dar endpoint u eg Obsidian

with open("server.js", "r") as f:
    content = f.read()

if "ObsidianAuth/api.php" in content:
    print("⚠️ Endpoint-ka horey ayuu u jiray!")
else:
    obsidian_code = '''
// ===== OBSIDIAN AUTH ENDPOINT =====
app.get('/ObsidianAuth/api.php', (req, res) => {
    try {
        const action = req.query.action;
        const licenseKey = req.query.license_key || req.query.key || '';
        
        if (action === 'release_manifest') {
            // Hubi license key-ga (haddii la bixiyay)
            let licenseData = {
                EXP: '2026-11-01',
                expires: '2026-11-01',
                remaining_seconds: 31536000,
                remaining_text: '365 days',
                version: '7.51.0',
                latest_version: '7.51.0',
                appstatus: true,
                server_status: true,
                valid: true,
                isValid: true,
                success: true,
                message: 'License valid',
                register: 'ABDI-VIP-REGISTER',
                registered: true,
                latest_apk_version: '7.51.0'
            };
            
            // Haddii license key la bixiyay, hubi database-ka
            if (licenseKey) {
                const lic = queryOne('SELECT * FROM licenses WHERE license_key = ?', [licenseKey]);
                if (!lic) {
                    return res.json({ status: 'failed', success: false, is_valid: false, valid: false, reason: 'INVALID' });
                }
                if (lic.status === 'used') {
                    return res.json({ status: 'failed', success: false, is_valid: false, valid: false, reason: 'USED' });
                }
                // Xogta license-ka
                licenseData.EXP = lic.expires_at || '2026-11-01';
                licenseData.expires = lic.expires_at || '2026-11-01';
                licenseData.remaining_text = lic.duration || '365 days';
            }
            
            res.json({
                status: 'success',
                success: true,
                is_valid: true,
                valid: true,
                state: 'online',
                message: 'License valid',
                http_code: 200,
                remaining_seconds: licenseData.remaining_seconds,
                remaining_text: licenseData.remaining_text,
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
                    EXP: licenseData.EXP,
                    expires: licenseData.expires,
                    remaining_seconds: licenseData.remaining_seconds,
                    remaining_text: licenseData.remaining_text,
                    version: '7.51.0',
                    latest_version: '7.51.0'
                }
            });
        } else {
            res.json({ status: 'failed', success: false, reason: 'INVALID_ACTION' });
        }
    } catch (error) {
        res.json({ status: 'failed', success: false, reason: 'ERROR', error: error.message });
    }
});

// ===== OBSIDIAN POST ENDPOINT (haddii app-ku isticmaalo POST) =====
app.post('/ObsidianAuth/api.php', (req, res) => {
    try {
        const action = req.body.action || req.query.action;
        const licenseKey = req.body.license_key || req.body.key || req.query.license_key || '';
        
        if (action === 'release_manifest') {
            let licenseData = {
                EXP: '2026-11-01',
                expires: '2026-11-01',
                remaining_seconds: 31536000,
                remaining_text: '365 days',
                version: '7.51.0',
                latest_version: '7.51.0'
            };
            
            if (licenseKey) {
                const lic = queryOne('SELECT * FROM licenses WHERE license_key = ?', [licenseKey]);
                if (!lic) {
                    return res.json({ status: 'failed', success: false, is_valid: false, valid: false, reason: 'INVALID' });
                }
                licenseData.EXP = lic.expires_at || '2026-11-01';
                licenseData.expires = lic.expires_at || '2026-11-01';
                licenseData.remaining_text = lic.duration || '365 days';
            }
            
            res.json({
                status: 'success',
                success: true,
                is_valid: true,
                valid: true,
                state: 'online',
                message: 'License valid',
                http_code: 200,
                remaining_seconds: licenseData.remaining_seconds,
                remaining_text: licenseData.remaining_text,
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
                    EXP: licenseData.EXP,
                    expires: licenseData.expires,
                    remaining_seconds: licenseData.remaining_seconds,
                    remaining_text: licenseData.remaining_text,
                    version: '7.51.0',
                    latest_version: '7.51.0'
                }
            });
        } else {
            res.json({ status: 'failed', success: false, reason: 'INVALID_ACTION' });
        }
    } catch (error) {
        res.json({ status: 'failed', success: false, reason: 'ERROR', error: error.message });
    }
});

'''
    listen_pos = content.find("app.listen(PORT")
    if listen_pos != -1:
        new_content = content[:listen_pos] + obsidian_code + content[listen_pos:]
        with open("server.js", "w") as f:
            f.write(new_content)
        print("✅ Endpoint-ka Obsidian waa lagu daray!")
    else:
        print("❌ Ma helin app.listen(PORT")
