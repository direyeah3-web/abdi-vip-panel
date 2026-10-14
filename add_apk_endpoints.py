import shutil

shutil.copy('server.js', 'server.js.backup_apk')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

old = "app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"

new = """// ===== APK ANALYZER ENDPOINTS =====
const AdmZip = require('adm-zip');
const crypto = require('crypto');

// POST /api/apk/upload — APK soo geli (base64)
app.post('/api/apk/upload', auth, adminOnly, async (req, res) => {
    try {
        const { filename, data } = req.body;
        if (!filename || !data) {
            return res.status(400).json({ success: false, error: 'filename iyo data waa loo baahan yahay' });
        }
        const buffer = Buffer.from(data, 'base64');
        const hash = crypto.createHash('md5').update(buffer).digest('hex');
        const tempPath = '/tmp/apk_' + hash + '.apk';
        const fs = require('fs');
        fs.writeFileSync(tempPath, buffer);
        res.json({
            success: true,
            filename: filename,
            size: buffer.length,
            hash: hash,
            path: tempPath,
            message: 'APK la keydiyay — analyze samee'
        });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

// POST /api/apk/analyze — APK baadh
app.post('/api/apk/analyze', auth, adminOnly, async (req, res) => {
    try {
        const { apkPath, filename } = req.body;
        if (!apkPath) {
            return res.status(400).json({ success: false, error: 'apkPath waa loo baahan yahay' });
        }
        const fs = require('fs');
        const { execSync } = require('child_process');
        if (!fs.existsSync(apkPath)) {
            return res.status(400).json({ success: false, error: 'APK ma jiro: ' + apkPath });
        }

        const zip = new AdmZip(apkPath);
        const entries = zip.getEntries();

        // 1. URLs-ka oo dhan
        const urls = new Set();
        const licenses = new Set();
        const smaliFiles = [];
        const nativeLibs = [];
        const protectionSigns = [];

        // Baadh entries
        for (const entry of entries) {
            const name = entry.entryName;

            // Smali files
            if (name.endsWith('.smali')) {
                smaliFiles.push(name);
                try {
                    const content = entry.getData().toString('utf8');
                    const urlMatches = content.match(/https?:\\/\\/[^\\s"']+/g) || [];
                    urlMatches.forEach(u => urls.add(u));
                    const licMatches = content.match(/ABDI-[A-Z0-9-]+/g) || [];
                    licMatches.forEach(l => licenses.add(l));
                } catch (e) {}
            }

            // Native libs
            if (name.startsWith('lib/') && (name.endsWith('.so') || name.endsWith('.a'))) {
                nativeLibs.push(name);
                try {
                    const buf = entry.getData();
                    const strings = buf.toString('latin1').match(/https?:\\/\\/[^\\x00-\\x20]+/g) || [];
                    strings.forEach(s => urls.add(s));
                } catch (e) {}
            }

            // Protection signs
            if (name.includes('rootbeer') || name.includes('safetynet') ||
                name.includes('integrity') || name.includes('ssl') ||
                name.includes('pinning') || name.includes('obfuscat') ||
                name.includes('proguard') || name.includes('firebase')) {
                protectionSigns.push(name);
            }
        }

        // 2. Response format-ka loader-ka
        let responseFormat = null;
        const smaliContent = smaliFiles.length > 0 ? (() => {
            try {
                const entry = zip.getEntry(smaliFiles.find(f => f.includes('LoginActivity') || f.includes('PanelLicense')));
                if (entry) return entry.getData().toString('utf8');
                return '';
            } catch (e) { return ''; }
        })() : '';

        // Response format hints
        if (smaliContent.includes('"status"')) responseFormat = 'JSON: {status, data, reason}';
        else if (smaliContent.includes('"success"')) responseFormat = 'JSON: {success, data}';

        // 3. License keys (ka database-ka sidoo kale)
        const dbLicenses = queryAll('SELECT license_key FROM licenses LIMIT 100') || [];
        dbLicenses.forEach(l => licenses.add(l.license_key));

        res.json({
            success: true,
            filename: filename,
            total_entries: entries.length,
            urls: Array.from(urls),
            licenses: Array.from(licenses),
            smali_files: smaliFiles.slice(0, 50),
            native_libs: nativeLibs,
            protection_signs: [...new Set(protectionSigns)],
            response_format: responseFormat,
            urls_count: urls.size,
            licenses_count: licenses.size
        });
    } catch (err) {
        console.error('APK analyze error:', err);
        res.status(500).json({ success: false, error: err.message });
    }
});

app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"""

if old in c:
    c = c.replace(old, new, 1)
    print("1. APK endpoints: OK")
else:
    print("1. APK endpoints: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_apk")
