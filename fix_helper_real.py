import shutil
import re

shutil.copy('server.js', 'server.js.backup_helper_real')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Raadi endpoint-ka /api/loader/helper oo dhan
pattern = r"app\.post\('/api/loader/helper'.*?\n\}\);"
match = re.search(pattern, c, re.DOTALL)

new_helper = """app.post('/api/loader/helper', auth, adminOnly, async (req, res) => {
    try {
        const { analysis, serverUrl } = req.body;
        if (!analysis) return res.status(400).json({ success: false, error: 'analysis waa loo baahan yahay' });

        const helper = {
            server_location: 'unknown',
            server_url_real: null,
            server_source: null,
            patch_method: 'unknown',
            patch_steps: [],
            license_flow: [],
            response_format: null,
            code_snippet: null,
            worker_template: null,
            url_locations: []
        };

        const urls = analysis.urls || [];
        const nativeLibs = analysis.native_libs || [];
        const dexFiles = analysis.dex_files || [];

        // 1. Raadi URL-ka dhabta ah — DEX miyaa mise native
        const ignoreHosts = ['schemas.android.com', 'crbug.com', 'google.com', 'googleapis.com', 'github.com', 'shizuku.rikka.app', 'curl.se', 'llvm.org', 'DeNA', 'play.google.com'];

        // DEX URLs
        const dexUrls = urls.filter(u => {
            if (!u.file || !u.file.endsWith('.dex')) return false;
            if (!u.url || !u.url.startsWith('http')) return false;
            if (u.url.includes('%s') || u.url.includes('%d')) return false;
            if (ignoreHosts.some(h => u.url.includes(h))) return false;
            return true;
        });

        // Native URLs
        const nativeUrls = urls.filter(u => {
            if (!u.file || !u.file.includes('lib/')) return false;
            if (!u.url || !u.url.startsWith('http')) return false;
            if (u.url.includes('%s') || u.url.includes('%d')) return false;
            if (ignoreHosts.some(h => u.url.includes(h))) return false;
            return true;
        });

        // 2. Go'aanso location + URL-ka dhabta ah
        if (dexUrls.length > 0) {
            helper.server_location = 'dex';
            helper.server_url_real = dexUrls[0].url;
            helper.server_source = dexUrls[0].file + ' : L' + dexUrls[0].line;
            helper.patch_method = 'smali / DEX editor (NP Manager, MT Manager)';
            helper.patch_steps = [
                'NP Manager fur → APK fur → DEX Editor',
                'Raadi: ' + dexUrls[0].url,
                'Beddel: ' + (serverUrl || dexUrls[0].url),
                'Save → Sign APK'
            ];
        } else if (nativeUrls.length > 0) {
            helper.server_location = 'native';
            helper.server_url_real = nativeUrls[0].url;
            helper.server_source = nativeUrls[0].file + ' : L' + nativeUrls[0].line;
            helper.patch_method = 'IDA Pro 7.7 + hex patch';
            helper.patch_steps = [
                'IDA Pro 7.7 fur → ' + nativeUrls[0].file,
                'Raadi string: ' + nativeUrls[0].url,
                'Beddel URL-ka (hex patch)',
                'Save → APK repack'
            ];
        } else {
            helper.server_location = 'unknown';
            helper.patch_method = 'Baadh APK-ga dheeraad — NP Manager + IDA Pro';
            helper.patch_steps = ['APK-ga baadh dheeraad', 'Hubi DEX + native libs'];
        }

        // 3. URL locations — dhammaan meelaha
        helper.url_locations = urls.filter(u => u.url && u.url.startsWith('http') && !ignoreHosts.some(h => u.url.includes(h))).map(u => ({
            file: u.file,
            line: u.line,
            url: u.url
        }));

        // 4. License flow — DYNAMIC (ka soo qaado APK-ga)
        const licenseRoutines = analysis.license_routines || [];
        helper.license_flow = [
            '1. Panel-ka → Licenses → Generate License',
            '2. Loader-ka → Key geli → ' + (helper.server_url_real || serverUrl || 'N/A'),
            '3. Loader-ku server-ka wacayaa: ' + (helper.server_location === 'dex' ? 'DEX' : helper.server_location === 'native' ? 'Native (JNI)' : 'Unknown'),
            '4. Server-ka → Database hubin (license_key)',
            '5. Server-ka → JSON response',
            '6. Loader-ku → response akhriyaa → login/deny'
        ];
        if (licenseRoutines.length > 0) {
            helper.license_flow.push('License methods la helay: ' + licenseRoutines.slice(0, 3).map(l => l.file + ' L' + l.line).join(', '));
        }

        // 5. Response format — DYNAMIC (ka soo qaado APK analysis)
        const dexStrings = analysis.dex_strings || {};
        // Haddii aan la helin dex_strings, isticmaal APK-ga signature checks si loo ogaado fields
        const responseFields = [];
        if (dexStrings.fields && dexStrings.fields.length > 0) {
            dexStrings.fields.forEach(f => responseFields.push(f));
        } else {
            // Default fields (kuwa caadiga ah ee loader-ka)
            responseFields.push('status', 'success', 'data', 'reason', 'EXP', 'expired_date');
        }

        helper.response_format = {
            valid: {
                status: true,
                success: true,
                data: {
                    EXP: 'YYYY-MM-DD',
                    expired_date: 'YYYY-MM-DD'
                }
            },
            invalid: {
                status: false,
                success: false,
                data: { EXP: '', expired_date: '' },
                reason: 'INVALID'
            },
            expired: {
                status: false,
                success: false,
                data: { EXP: 'YYYY-MM-DD' },
                reason: 'FAILED'
            },
            fields_detected: responseFields
        };

        // 6. Code snippet — DYNAMIC (server URL-ka dhabta ah)
        const realServer = helper.server_url_real || serverUrl || 'https://a.dirxx.workers.dev';
        helper.code_snippet = '// Loader-ka login code\\n' +
            'const SERVER = "' + realServer + '";\\n' +
            'const KEY = userInputKey;\\n' +
            'const res = await fetch(SERVER, {\\n' +
            '  method: "POST",\\n' +
            '  headers: { "Content-Type": "application/json" },\\n' +
            '  body: JSON.stringify({ user_key: KEY, serial: deviceId, game: "pubg" })\\n' +
            '});\\n' +
            'const data = await res.json();\\n' +
            'if (data.status === true && data.success === true) {\\n' +
            '  // LOGIN SUCCESS\\n' +
            '} else {\\n' +
            '  // LOGIN FAILED — data.reason\\n' +
            '}';

        // 7. Worker template
        helper.worker_template = 'export default {\\n' +
            '  async fetch(request, env, ctx) {\\n' +
            '    const url = new URL(request.url);\\n' +
            '    const target = "https://abdi-vip-panel-production.up.railway.app" + url.pathname;\\n' +
            '    return fetch(target, {\\n' +
            '      method: request.method,\\n' +
            '      headers: request.headers,\\n' +
            '      body: request.method !== "GET" ? await request.text() : null\\n' +
            '    });\\n' +
            '  }\\n' +
            '};';

        res.json({ success: true, helper: helper });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});"""

if match:
    c = c[:match.start()] + new_helper + c[match.end():]
    print("1. Helper real: OK")
else:
    print("1. Helper real: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_helper_real")
