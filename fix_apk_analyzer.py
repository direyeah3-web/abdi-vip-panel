import shutil

shutil.copy('server.js', 'server.js.backup_analyzer')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Raadi endpoint-ka /api/apk/analyze oo dhan
import re
pattern = r"app\.post\('/api/apk/analyze', auth, adminOnly, async \(req, res\) => \{.*?\n\}\);"
match = re.search(pattern, c, re.DOTALL)

new_analyze = """app.post('/api/apk/analyze', auth, adminOnly, async (req, res) => {
    try {
        const { apkPath, filename } = req.body;
        if (!apkPath) {
            return res.status(400).json({ success: false, error: 'apkPath waa loo baahan yahay' });
        }
        const fs = require('fs');
        if (!fs.existsSync(apkPath)) {
            return res.status(400).json({ success: false, error: 'APK ma jiro: ' + apkPath });
        }

        const zip = new AdmZip(apkPath);
        const entries = zip.getEntries();

        // ===== 1. URLs (file -> line -> url) =====
        const urlsList = [];
        const smaliFiles = [];
        const nativeLibs = [];
        const dexFiles = [];

        // ===== 2. License/auth/verification routine =====
        const licenseRoutines = [];
        const signatureChecks = [];
        const integrityChecks = [];
        const startupCalls = [];

        const urlRegex = /https?:\\/\\/[^\\s"']+/g;
        const licKeywords = ['license', 'verify', 'auth', 'activation', 'validate', 'checkLicense', 'checkKey', 'Premium', 'vip'];
        const sigKeywords = ['getPackageInfo', 'GET_SIGNATURES', 'MessageDigest', 'PackageManager', 'signature', 'Signature', 'certificate', 'CERT', 'SHA-1', 'SHA1', 'MD5', 'CRC'];
        const integKeywords = ['SafetyNet', 'PlayIntegrity', 'attest', 'rootBeer', 'RootBeer', 'isRooted', 'emulator', 'isEmulator', 'debugger', 'isDebuggerConnected', 'isDebug', 'tamper', 'Tamper', 'Integrity'];
        const startupKeywords = ['onCreate', 'Application', 'attachBaseContext', '<init>', 'onStart', 'LauncherActivity'];

        // Track file name
        const getName = (e) => e.entryName;

        for (const entry of entries) {
            const name = entry.entryName;

            // Smali files
            if (name.endsWith('.smali')) {
                smaliFiles.push(name);
                let content = '';
                try {
                    const buf = entry.getData();
                    content = buf.toString('utf8');
                } catch (err) {
                    try { content = entry.getData().toString('latin1'); } catch (e) {}
                }

                const lines = content.split('\\n');

                // URLs with line numbers
                lines.forEach((line, idx) => {
                    const matches = line.match(urlRegex);
                    if (matches) {
                        matches.forEach(u => {
                            urlsList.push({ file: name, line: idx + 1, url: u });
                        });
                    }
                });

                // License routines
                const lowerName = name.toLowerCase();
                const lowerContent = content.toLowerCase();
                let licMatch = licKeywords.some(k => lowerName.includes(k.toLowerCase()) || lowerContent.includes(k.toLowerCase()));
                if (licMatch) {
                    // Soo qaado class name iyo method
                    const classMatch = content.match(/\\.class[^\\n]*/);
                    const methodMatch = content.match(/\\.method[^\\n]*/);
                    lines.forEach((line, idx) => {
                        if (licKeywords.some(k => line.toLowerCase().includes(k.toLowerCase()))) {
                            licenseRoutines.push({
                                file: name,
                                line: idx + 1,
                                class_name: classMatch ? classMatch[0] : 'N/A',
                                method_name: methodMatch ? methodMatch[0] : 'N/A',
                                smali_line: line.trim().substring(0, 200)
                            });
                        }
                    });
                }

                // Signature checks
                lines.forEach((line, idx) => {
                    if (sigKeywords.some(k => line.includes(k))) {
                        signatureChecks.push({
                            file: name,
                            line: idx + 1,
                            match: line.trim().substring(0, 200)
                        });
                    }
                });

                // Integrity checks
                lines.forEach((line, idx) => {
                    if (integKeywords.some(k => line.includes(k))) {
                        integrityChecks.push({
                            file: name,
                            line: idx + 1,
                            match: line.trim().substring(0, 200)
                        });
                    }
                });

                // Startup calls
                lines.forEach((line, idx) => {
                    if (startupKeywords.some(k => line.includes(k)) && urlRegex.test(line)) {
                        startupCalls.push({
                            file: name,
                            line: idx + 1,
                            method: line.trim().substring(0, 200)
                        });
                    }
                });
            }

            // Native libs
            if (name.startsWith('lib/') && (name.endsWith('.so') || name.endsWith('.a'))) {
                nativeLibs.push(name);
                try {
                    const buf = entry.getData();
                    const str = buf.toString('latin1');
                    const matches = str.match(urlRegex) || [];
                    matches.forEach(u => {
                        urlsList.push({ file: name, line: 0, url: u });
                    });
                    // License key strings
                    const licStrings = str.match(/ABDI-[A-Z0-9-]+/g) || [];
                    licStrings.forEach(l => {
                        licenseRoutines.push({ file: name, line: 0, match: l });
                    });
                } catch (e) {}
            }

            // DEX files
            if (name.endsWith('.dex')) {
                dexFiles.push(name);
            }
        }

        // Database licenses
        const dbLicenses = queryAll('SELECT license_key FROM licenses LIMIT 200') || [];
        const allLicenses = dbLicenses.map(l => l.license_key);

        res.json({
            success: true,
            filename: filename,
            total_entries: entries.length,
            smali_files_count: smaliFiles.length,
            native_libs_count: nativeLibs.length,
            dex_files_count: dexFiles.length,
            urls: urlsList,
            license_routines: licenseRoutines.slice(0, 100),
            signature_checks: signatureChecks.slice(0, 100),
            integrity_checks: integrityChecks.slice(0, 100),
            startup_calls: startupCalls.slice(0, 50),
            db_licenses: allLicenses,
            urls_count: urlsList.length,
            licenses_count: licenseRoutines.length
        });
    } catch (err) {
        console.error('APK analyze error:', err);
        res.status(500).json({ success: false, error: err.message });
    }
});"""

if match:
    c = c[:match.start()] + new_analyze + c[match.end():]
    print("1. Analyze endpoint: OK")
else:
    print("1. Analyze endpoint: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_analyzer")
