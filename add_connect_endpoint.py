# add_connect_endpoint.py - Ku dar /connect endpoint ZOON MOD

with open("server.js", "r") as f:
    content = f.read()

if "app.post('/connect'" in content or 'app.post("/connect"' in content:
    print("⚠️ Endpoint-ka /connect horey ayuu u jiray!")
else:
    connect_code = '''
// ===== ZOON MOD /connect ENDPOINT =====
function parseLoaderBody(rawBody) {
    if (!rawBody) return {};
    let body = rawBody;
    if (typeof body === 'string') {
        try { return JSON.parse(body); } catch (e) {}
        if (body.includes('=')) {
            const params = new URLSearchParams(body);
            const obj = {};
            for (const [k, v] of params) obj[k] = v;
            return obj;
        }
    }
    return body || {};
}

app.post('/connect', (req, res) => {
    try {
        const body = parseLoaderBody(req.body);
        const licKey = body.user_key || body.key || body.license_key || '';
        const deviceId = body.serial || body.device_id || '';
        const game = body.game || '';
        
        if (!licKey) {
            return res.json({ status: false, data: { EXP: '' }, reason: 'INVALID' });
        }
        
        const lic = queryOne('SELECT * FROM licenses WHERE license_key = ?', [licKey]);
        if (!lic) {
            return res.json({ status: false, data: { EXP: '' }, reason: 'INVALID' });
        }
        
        const expiry = lic.expires_at || '2026-11-01';
        if (lic.expires_at && new Date(lic.expires_at) < new Date()) {
            return res.json({ status: false, data: { EXP: expiry }, reason: 'FAILED' });
        }
        
        if (lic.status === 'used' && lic.device_id && lic.device_id !== deviceId) {
            return res.json({ status: false, data: { EXP: expiry }, reason: 'FAILED' });
        }
        
        if (lic.status === 'unused') {
            db.run('UPDATE licenses SET status = ?, device_id = ?, used_at = CURRENT_TIMESTAMP WHERE id = ?', ['used', deviceId, lic.id]);
            saveDB();
        }
        
        const appVersion = '4.6.0';
        const gamesList = [
            { gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Global", gameStatus: "Latest Version", gameVersion: "Latest Version", currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion, gamePackage: "com.tencent.ig", gameIcon: "pubg_global.png", gameObb: "", link: "https://www.pubgmobile.com/" },
            { gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Korea", gameStatus: "Latest Version", gameVersion: "Latest Version", currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion, gamePackage: "com.pubg.krmobile", gameIcon: "pubg_korea.png", gameObb: "", link: "https://www.pubgmobile.com/" },
            { gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Vietnam", gameStatus: "Latest Version", gameVersion: "Latest Version", currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion, gamePackage: "com.vng.pubgmobile", gameIcon: "pubg_vietnam.png", gameObb: "", link: "https://www.pubgmobile.com/" },
            { gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Taiwan", gameStatus: "Latest Version", gameVersion: "Latest Version", currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion, gamePackage: "com.rekoo.pubgm", gameIcon: "pubg_taiwan.png", gameObb: "", link: "https://www.pubgmobile.com/" }
        ];
        
        res.json({
            status: true,
            data: {
                EXP: expiry,
                exdate: expiry,
                expired_date: expiry,
                appVersion: appVersion,
                appVersionString: appVersion,
                firebase_database_url: 'https://abdi-vip-panel-default-rtdb.firebaseio.com',
                databaseUrl: 'https://abdi-vip-panel-default-rtdb.firebaseio.com',
                GAME_LIST_ICON: ["pubg_global.png", "pubg_korea.png", "pubg_vietnam.png", "pubg_taiwan.png"],
                GAME_LIST_PKG: ["com.tencent.ig", "com.pubg.krmobile", "com.vng.pubgmobile", "com.rekoo.pubgm"],
                STATUS_BY: 'Latest Version',
                USER_ID: licKey,
                game_list: gamesList,
                games: gamesList
            }
        });
    } catch (error) {
        res.json({ status: false, data: { EXP: '' }, reason: 'INVALID' });
    }
});

'''
    listen_pos = content.find("app.listen(PORT")
    if listen_pos != -1:
        new_content = content[:listen_pos] + connect_code + content[listen_pos:]
        with open("server.js", "w") as f:
            f.write(new_content)
        print("✅ Endpoint-ka /connect waa lagu daray!")
    else:
        print("❌ Ma helin app.listen(PORT")
