# add_zoon_endpoint.py - Ku dar endpoint-ka ZOON MOD

with open("server.js", "r") as f:
    content = f.read()

if "zoon_auth" in content or "/api/zoon" in content:
    print("⚠️ Endpoint-ka ZOON horey ayuu u jiray!")
else:
    zoon_code = '''
// ===== ZOON MOD ENDPOINT =====
app.post('/api/zoon', (req, res) => {
    try {
        const body = req.body || {};
        const licenseKey = String(body.license_key || body.key || body.USER_ID || '').trim();
        
        if (!licenseKey) {
            return res.json({
                status: false,
                data: { EXP: '', exdate: '', expired_date: '' },
                reason: 'INVALID'
            });
        }
        
        // Hubi license key-ga database-ka
        const lic = queryOne('SELECT * FROM licenses WHERE license_key = ?', [licenseKey]);
        
        if (!lic) {
            return res.json({
                status: false,
                data: { EXP: '', exdate: '', expired_date: '' },
                reason: 'INVALID'
            });
        }
        
        if (lic.status === 'used') {
            return res.json({
                status: false,
                data: { 
                    EXP: lic.expires_at || '2026-11-01',
                    exdate: lic.expires_at || '2026-11-01',
                    expired_date: lic.expires_at || '2026-11-01'
                },
                reason: 'FAILED'
            });
        }
        
        const expDate = lic.expires_at || '2026-11-01';
        const appVersion = '4.5';
        
        // Liiska games-ka
        const gameList = [
            {
                gameTitle: "PUBG MOBILE",
                gamename: "PUBG MOBILE",
                region: "Global",
                gameStatus: "Latest Version",
                gameVersion: "Latest Version",
                currentversion: appVersion,
                appVersion: appVersion,
                appVersionString: appVersion,
                gamePackage: "com.tencent.ig",
                gameIcon: "pubg_global.png",
                gameObb: "",
                link: "https://www.pubgmobile.com/"
            },
            {
                gameTitle: "PUBG MOBILE",
                gamename: "PUBG MOBILE",
                region: "Korea",
                gameStatus: "Latest Version",
                gameVersion: "Latest Version",
                currentversion: appVersion,
                appVersion: appVersion,
                appVersionString: appVersion,
                gamePackage: "com.pubg.krmobile",
                gameIcon: "pubg_korea.png",
                gameObb: "",
                link: "https://www.pubgmobile.com/"
            },
            {
                gameTitle: "PUBG MOBILE",
                gamename: "PUBG MOBILE",
                region: "Vietnam",
                gameStatus: "Latest Version",
                gameVersion: "Latest Version",
                currentversion: appVersion,
                appVersion: appVersion,
                appVersionString: appVersion,
                gamePackage: "com.vng.pubgmobile",
                gameIcon: "pubg_vietnam.png",
                gameObb: "",
                link: "https://www.pubgmobile.com/"
            },
            {
                gameTitle: "PUBG MOBILE",
                gamename: "PUBG MOBILE",
                region: "Taiwan",
                gameStatus: "Latest Version",
                gameVersion: "Latest Version",
                currentversion: appVersion,
                appVersion: appVersion,
                appVersionString: appVersion,
                gamePackage: "com.rekoo.pubgm",
                gameIcon: "pubg_taiwan.png",
                gameObb: "",
                link: "https://www.pubgmobile.com/"
            }
        ];
        
        res.json({
            status: true,
            data: {
                EXP: expDate,
                exdate: expDate,
                expired_date: expDate,
                appVersion: appVersion,
                appVersionString: appVersion,
                firebase_database_url: "https://abdi-vip-panel-default-rtdb.firebaseio.com",
                databaseUrl: "https://abdi-vip-panel-default-rtdb.firebaseio.com",
                GAME_LIST_ICON: ["pubg_global.png", "pubg_korea.png", "pubg_vietnam.png", "pubg_taiwan.png"],
                GAME_LIST_PKG: ["com.tencent.ig", "com.pubg.krmobile", "com.vng.pubgmobile", "com.rekoo.pubgm"],
                STATUS_BY: "Latest Version",
                USER_ID: licenseKey,
                game_list: gameList,
                games: gameList
            }
        });
    } catch (error) {
        res.json({
            status: false,
            data: { EXP: '', exdate: '', expired_date: '' },
            reason: 'INVALID'
        });
    }
});

// ===== ZOON MOD GET ENDPOINT =====
app.get('/api/zoon', (req, res) => {
    const licenseKey = req.query.license_key || req.query.key || '';
    
    if (!licenseKey) {
        return res.json({
            status: false,
            data: { EXP: '', exdate: '', expired_date: '' },
            reason: 'INVALID'
        });
    }
    
    // Samee sida POST
    const lic = queryOne('SELECT * FROM licenses WHERE license_key = ?', [licenseKey]);
    
    if (!lic) {
        return res.json({
            status: false,
            data: { EXP: '', exdate: '', expired_date: '' },
            reason: 'INVALID'
        });
    }
    
    const expDate = lic.expires_at || '2026-11-01';
    const appVersion = '4.5';
    
    const gameList = [
        {
            gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Global",
            gameStatus: "Latest Version", gameVersion: "Latest Version",
            currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion,
            gamePackage: "com.tencent.ig", gameIcon: "pubg_global.png", gameObb: "",
            link: "https://www.pubgmobile.com/"
        },
        {
            gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Korea",
            gameStatus: "Latest Version", gameVersion: "Latest Version",
            currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion,
            gamePackage: "com.pubg.krmobile", gameIcon: "pubg_korea.png", gameObb: "",
            link: "https://www.pubgmobile.com/"
        },
        {
            gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Vietnam",
            gameStatus: "Latest Version", gameVersion: "Latest Version",
            currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion,
            gamePackage: "com.vng.pubgmobile", gameIcon: "pubg_vietnam.png", gameObb: "",
            link: "https://www.pubgmobile.com/"
        },
        {
            gameTitle: "PUBG MOBILE", gamename: "PUBG MOBILE", region: "Taiwan",
            gameStatus: "Latest Version", gameVersion: "Latest Version",
            currentversion: appVersion, appVersion: appVersion, appVersionString: appVersion,
            gamePackage: "com.rekoo.pubgm", gameIcon: "pubg_taiwan.png", gameObb: "",
            link: "https://www.pubgmobile.com/"
        }
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
            USER_ID: licenseKey,
            game_list: gameList,
            games: gameList
        }
    });
});

'''
    listen_pos = content.find("app.listen(PORT")
    if listen_pos != -1:
        new_content = content[:listen_pos] + zoon_code + content[listen_pos:]
        with open("server.js", "w") as f:
            f.write(new_content)
        print("✅ Endpoint-ka ZOON MOD waa lagu daray!")
    else:
        print("❌ Ma helin app.listen(PORT")
