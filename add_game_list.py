# add_game_list.py - Ku dar game_list endpoint-ka Obsidian

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
        const clientVersion = req.query.client_apk_version || '4.6.0';
        
        if (action === 'release_manifest') {
            let expDate = '2026-11-01';
            let duration = '365 days';
            let userId = licenseKey || 'GUEST';
            
            if (licenseKey) {
                const lic = queryOne('SELECT * FROM licenses WHERE license_key = ?', [licenseKey]);
                if (lic) {
                    expDate = lic.expires_at || '2026-11-01';
                    duration = lic.duration || '365 days';
                    userId = lic.license_key;
                }
            }
            
            const appVersion = '4.6.0';
            const gameList = [
                { gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Global", gameStatus: "Latest Version", gameVersion: "Latest Version", currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion, gamePackage: "com.tencent.ig", gameIcon: "pubg_global.png", gameObb: "", link: "https://www.pubgmobile.com/" },
                { gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Korea", gameStatus: "Latest Version", gameVersion: "Latest Version", currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion, gamePackage: "com.pubg.krmobile", gameIcon: "pubg_korea.png", gameObb: "", link: "https://www.pubgmobile.com/" },
                { gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Vietnam", gameStatus: "Latest Version", gameVersion: "Latest Version", currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion, gamePackage: "com.vng.pubgmobile", gameIcon: "pubg_vietnam.png", gameObb: "", link: "https://www.pubgmobile.com/" },
                { gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Taiwan", gameStatus: "Latest Version", gameVersion: "Latest Version", currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion, gamePackage: "com.rekoo.pubgm", gameIcon: "pubg_taiwan.png", gameObb: "", link: "https://www.pubgmobile.com/" }
            ];
            
            res.json({
                status: true,
                data: {
                    EXP: expDate, exdate: expDate, expired_date: expDate,
                    appVersion: appVersion, appVersionString: appVersion,
                    firebase_database_url: "https://abdi-vip-panel-default-rtdb.firebaseio.com",
                    databaseUrl: "https://abdi-vip-panel-default-rtdb.firebaseio.com",
                    GAME_LIST_ICON: ["pubg_global.png", "pubg_korea.png", "pubg_vietnam.png", "pubg_taiwan.png"],
                    GAME_LIST_PKG: ["com.tencent.ig", "com.pubg.krmobile", "com.vng.pubgmobile", "com.rekoo.pubgm"],
                    STATUS_BY: "Latest Version",
                    USER_ID: userId,
                    game_list: gameList,
                    games: gameList
                }
            });
        } else {
            res.json({ status: true, success: true });
        }
    } catch (error) {
        res.json({ status: false, data: { EXP: '', exdate: '', expired_date: '' }, reason: 'INVALID' });
    }
});'''
    
    content = content[:match.start()] + new_endpoint + content[match.end():]
    with open("server.js", "w") as f:
        f.write(content)
    print("✅ game_list waa lagu daray endpoint-ka Obsidian!")
else:
    print("❌ Ma helin endpoint-ka")
