import shutil

shutil.copy('server.js', 'server.js.backup_helper')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

old = "app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"

new = """// ===== LOADER HELPER ENDPOINT =====
app.post('/api/loader/helper', auth, adminOnly, async (req, res) => {
    try {
        const { analysis, serverUrl } = req.body;
        if (!analysis) {
            return res.status(400).json({ success: false, error: 'analysis waa loo baahan yahay' });
        }

        const helper = {
            server_location: 'unknown',
            patch_method: 'unknown',
            license_flow: [],
            response_format: null,
            code_snippet: null,
            worker_template: null,
            steps: []
        };

        const urls = analysis.urls || [];
        const nativeLibs = analysis.native_libs || [];
        const dexFiles = analysis.dex_files || [];

        // 1. Server location — DEX vs Native
        const dexUrls = urls.filter(u => u.file && u.file.endsWith('.dex') && u.url && u.url.startsWith('http'));
        const nativeUrls = urls.filter(u => u.file && u.file.includes('lib/') && u.url && u.url.startsWith('http') && !u.url.includes('%s'));

        if (dexUrls.length > 0) {
            helper.server_location = 'dex';
            helper.patch_method = 'smali / DEX editor (NP Manager, MT Manager)';
        } else if (nativeUrls.length > 0) {
            helper.server_location = 'native';
            helper.patch_method = 'IDA Pro 7.7 + hex patch / Ghidra';
        } else {
            helper.server_location = 'unknown';
            helper.patch_method = 'Baadh APK-ga si qoto dheer';
        }

        // 2. License flow — sida loo sameeyo
        helper.license_flow = [
            '1. Panel-ka: Generate License → hel license key (ABDI-XXXX)',
            '2. Loader-ka: User-ku geliyaa license key',
            '3. Loader-ku: Wuxuu u diraa server-kaaga (' + (serverUrl || 'a.dirxx.workers.dev') + ')',
            '4. Server-ka: Wuxuu hubinayaa license-ka database-ka',
            '5. Server-ka: Wuxuu soo celiyaa JSON response',
            '6. Loader-ku: Wuxuu akhriyaa response-ka → login/deny'
        ];

        // 3. Response format — qaabka loader-ku aqbalo
        helper.response_format = {
            valid: {
                status: true,
                success: true,
                data: {
                    EXP: '2026-11-01',
                    expired_date: '2026-11-01',
                    appVersion: '4.6.0',
                    firebase_database_url: 'https://abdi-vip-panel-default-rtdb.firebaseio.com',
                    GAME_LIST_ICON: ['pubg_global.png'],
                    GAME_LIST_PKG: ['com.tencent.ig'],
                    STATUS_BY: 'Latest Version',
                    USER_ID: 'user_id',
                    game_list: 'game_list',
                    games: 'games'
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
                data: { EXP: '2026-11-01' },
                reason: 'FAILED'
            }
        };

        // 4. Code snippet — loader-ka login
        helper.code_snippet = '// Loader-ka login code\\n' +
            'const SERVER = "' + (serverUrl || 'https://a.dirxx.workers.dev') + '";\\n' +
            'const KEY = userInputKey;\\n' +
            'const res = await fetch(SERVER + "/connect", {\\n' +
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

        // 5. Worker template — haddii loo baahdo
        helper.worker_template = 'export default {\\n' +
            '  async fetch(request, env, ctx) {\\n' +
            '    // Proxy to Railway\\n' +
            '    const url = new URL(request.url);\\n' +
            '    const target = "https://abdi-vip-panel-production.up.railway.app" + url.pathname;\\n' +
            '    return fetch(target, {\\n' +
            '      method: request.method,\\n' +
            '      headers: request.headers,\\n' +
            '      body: request.method !== "GET" ? await request.text() : null\\n' +
            '    });\\n' +
            '  }\\n' +
            '};';

        // 6. Steps — tallaabooyinka
        helper.steps = [
            '1. Panel-ka → APK Analyzer → APK soo geli',
            '2. Hubi qaybta ESSENTIAL INFO — Server URL-ka saxda ah',
            '3. ' + (helper.server_location === 'dex' ? 'NP Manager → DEX Editor → Beddel URL-ka' : helper.server_location === 'native' ? 'IDA Pro 7.7 → hex patch → Beddel URL-ka' : 'Baadh APK-ga dheeraad'),
            '4. Panel-ka → Licenses → Generate License (duration dooro)',
            '5. License key-ga koobi',
            '6. Loader-ka → Key geli → LOGIN',
            '7. Loader-ku server-kaaga wuu wacayaa → response-ka hubi',
            '8. Haddii khalad — Cloudflare Worker template beddel'
        ];

        res.json({ success: true, helper: helper });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"""

if old in c:
    c = c.replace(old, new, 1)
    print("1. Helper endpoint: OK")
else:
    print("1. Helper endpoint: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_helper")
