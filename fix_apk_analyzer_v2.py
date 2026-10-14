import shutil
import re

shutil.copy('server.js', 'server.js.backup_analyzer_v2')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Raadi endpoint-ka hore
pattern = r"app\.post\('/api/apk/analyze', auth, adminOnly, async \(req, res\) => \{.*?\n\}\);"
match = re.search(pattern, c, re.DOTALL)

new_analyze = """app.post('/api/apk/analyze', auth, adminOnly, async (req, res) => {
    try {
        const { apkPath, filename } = req.body;
        if (!apkPath) return res.status(400).json({ success: false, error: 'apkPath waa loo baahan yahay' });
        const fs = require('fs');
        const { execSync } = require('child_process');
        if (!fs.existsSync(apkPath)) return res.status(400).json({ success: false, error: 'APK ma jiro' });

        const zip = new AdmZip(apkPath);
        const entries = zip.getEntries();
        const tmpDir = '/tmp/apk_extract_' + Date.now();
        fs.mkdirSync(tmpDir, { recursive: true });

        // Soo qaado dhammaan entries
        for (const entry of entries) {
            const target = tmpDir + '/' + entry.entryName;
            if (!entry.isDirectory) {
                const dir = require('path').dirname(target);
                fs.mkdirSync(dir, { recursive: true });
                fs.writeFileSync(target, entry.getData());
            }
        }

        const result = {
            // 1. APK identification
            package_name: 'N/A',
            launcher_activity: 'N/A',
            application_class: 'N/A',
            dex_files: [],
            native_libs: [],
            assets: [],
            // 2. License check
            license_routines: [],
            // 3. URLs
            urls: [],
            // 4. Signature verification
            signature_checks: [],
            // 5. Integrity / anti-tamper
            integrity_checks: [],
            // 6. Native methods (JNI)
            native_methods: [],
            jni_exports: [],
            // 7. Hermes bytecode
            hermes: null
        };

        // ===== 1. APK identification (AndroidManifest.xml) =====
        const manifestPath = tmpDir + '/AndroidManifest.xml';
        if (fs.existsSync(manifestPath)) {
            try {
                const buf = fs.readFileSync(manifestPath);
                // Binary XML — baadh strings
                const str = buf.toString('latin1');
                // Package name
                const pkgMatch = str.match(/com\\.[a-z0-9]+\\.[a-z0-9_.]+/i);
                if (pkgMatch) result.package_name = pkgMatch[0];
                // Launcher
                const launcherMatch = str.match(/([A-Z][a-zA-Z0-9_]+Activity)/);
                if (launcherMatch) result.launcher_activity = launcherMatch[0];
                // Application
                const appMatch = str.match(/([A-Z][a-zA-Z0-9_]+Application)/);
                if (appMatch) result.application_class = appMatch[0];
            } catch (e) {}
        }

        // ===== DEX files =====
        const dexList = entries.filter(e => e.entryName.match(/^classes[0-9]*\\.dex$/)).map(e => e.entryName);
        result.dex_files = dexList;

        // ===== Native libs =====
        const nativeList = entries.filter(e => e.entryName.match(/^lib\\/.*\\.so$/)).map(e => e.entryName);
        result.native_libs = nativeList;

        // ===== Assets =====
        const assetList = entries.filter(e => e.entryName.startsWith('assets/') && !e.isDirectory).map(e => e.entryName);
        result.assets = assetList;

        // ===== 2-6. DEX analysis =====
        const licenseKw = ['LicenseManager', 'AuthManager', 'PanelLicense', 'LoginActivity', 'LoginModule', 'activateSdk', 'MetaActivationManager', 'BuildSeal', 'validateLicense', 'nativeValidateLicense', 'checkLicense', 'statusTrue', 'isValid', 'is_valid', 'performLogin'];
        const urlRegex = /https?:\\/\\/[^\\x00-\\x20"']+/g;
        const sigKw = ['getPackageInfo', 'GET_SIGNATURES', 'GET_SIGNING_CERTIFICATES', 'Signature', 'MessageDigest', 'SHA-256', 'SHA-1', 'X509Certificate', 'certSha256', 'OFFICIAL_CERT', 'expectedHash'];
        const integKw = ['SafetyNet', 'PlayIntegrity', 'IntegrityToken', 'Frida', 'frida', 'ptrace', 'TracerPid', 'Magisk', 'zygisk', 'Xposed', 'Substrate', 'ro.debuggable', 'ro.kernel.qemu', 'goldfish', 'ranchu', 'qemu_pipe', 'test-keys'];
        const nativeKw = ['native ', 'nativeValidate', 'nativeEnsure'];

        for (const entry of entries) {
            const name = entry.entryName;
            if (!name.endsWith('.dex')) continue;

            try {
                const buf = entry.getData();
                const str = buf.toString('latin1');
                const lines = str.split('\\n');

                // URLs
                const urlMatches = str.match(urlRegex) || [];
                urlMatches.forEach(u => result.urls.push({ file: name, line: 0, url: u }));

                // License routines
                lines.forEach((line, idx) => {
                    if (licenseKw.some(k => line.includes(k))) {
                        result.license_routines.push({ file: name, line: idx + 1, match: line.trim().substring(0, 200) });
                    }
                });

                // Signature
                lines.forEach((line, idx) => {
                    if (sigKw.some(k => line.includes(k))) {
                        result.signature_checks.push({ file: name, line: idx + 1, match: line.trim().substring(0, 200) });
                    }
                });

                // Integrity
                lines.forEach((line, idx) => {
                    if (integKw.some(k => line.includes(k))) {
                        result.integrity_checks.push({ file: name, line: idx + 1, match: line.trim().substring(0, 200) });
                    }
                });

                // Native methods
                lines.forEach((line, idx) => {
                    if (nativeKw.some(k => line.includes(k))) {
                        result.native_methods.push({ file: name, line: idx + 1, match: line.trim().substring(0, 200) });
                    }
                });
            } catch (e) {}
        }

        // ===== 3. URLs in assets =====
        for (const entry of entries) {
            if (!entry.entryName.startsWith('assets/')) continue;
            try {
                const buf = entry.getData();
                const str = buf.toString('latin1');
                const urlMatches = str.match(urlRegex) || [];
                urlMatches.forEach(u => result.urls.push({ file: entry.entryName, line: 0, url: u }));
            } catch (e) {}
        }

        // ===== 4-5. Signature + Integrity in native libs =====
        for (const entry of entries) {
            if (!entry.entryName.startsWith('lib/') || !entry.entryName.endsWith('.so')) continue;
            try {
                const buf = entry.getData();
                const str = buf.toString('latin1');
                const urlMatches = str.match(urlRegex) || [];
                urlMatches.forEach(u => result.urls.push({ file: entry.entryName, line: 0, url: u }));

                // JNI exports
                const jniMatches = str.match(/Java_[a-zA-Z0-9_]+/g) || [];
                jniMatches.forEach(j => result.jni_exports.push({ file: entry.entryName, symbol: j }));

                // Integrity in native
                sigKw.concat(integKw).forEach(kw => {
                    if (str.includes(kw)) {
                        result.signature_checks.push({ file: entry.entryName, line: 0, match: 'native: ' + kw });
                    }
                });
            } catch (e) {}
        }

        // ===== 7. Hermes bytecode =====
        const bundlePath = tmpDir + '/assets/index.android.bundle';
        if (fs.existsSync(bundlePath)) {
            try {
                const buf = fs.readFileSync(bundlePath);
                const magic = buf.slice(0, 8).toString('hex');
                const version = buf.readUInt32LE(8);
                const str = buf.toString('latin1');
                const urlMatches = str.match(urlRegex) || [];
                urlMatches.forEach(u => result.urls.push({ file: 'assets/index.android.bundle', line: 0, url: u }));
                const licMatches = str.match(/(validateLicense|license|LicenseManager|isValid|statusTrue)/g) || [];
                result.hermes = {
                    magic: magic,
                    version: version,
                    size: buf.length,
                    license_hits: [...new Set(licMatches)]
                };
            } catch (e) {}
        }

        // Clean up
        try { execSync('rm -rf ' + tmpDir); } catch (e) {}

        // Counts
        result.urls_count = result.urls.length;
        result.license_count = result.license_routines.length;
        result.signature_count = result.signature_checks.length;
        result.integrity_count = result.integrity_checks.length;
        result.native_count = result.native_methods.length;
        result.jni_count = result.jni_exports.length;
        result.filename = filename;
        result.success = true;

        res.json(result);
    } catch (err) {
        console.error('APK analyze error:', err);
        res.status(500).json({ success: false, error: err.message });
    }
});"""

if match:
    c = c[:match.start()] + new_analyze + c[match.end():]
    print("1. Analyze v2: OK")
else:
    print("1. Analyze v2: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_analyzer_v2")
