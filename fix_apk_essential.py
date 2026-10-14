import shutil
import re

shutil.copy('server.js', 'server.js.backup_essential')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Ku dar function cusub — extractEssential
old_marker = "// Parse AndroidManifest.xml (binary XML)"
new_marker = """// Extract essential loader info — server URL, endpoint, response format
function extractEssential(allUrls, dexFiles) {
    const essential = {
        server_url: null,
        endpoint: null,
        full_url: null,
        response_format: null,
        source_ip: null,
        license_methods: [],
        json_fields: []
    };

    // 1. Filter server URLs — ma aha schemas.android.com, crbug, google.com
    const ignoreHosts = ['schemas.android.com', 'crbug.com', 'google.com', 'googleapis.com', 'github.com', 'shizuku.rikka.app', 'curl.se', 'llvm.org', 'DeNA'];
    const serverUrls = allUrls.filter(u => {
        const url = u.url || '';
        return url.startsWith('http') && !ignoreHosts.some(h => url.includes(h));
    });

    if (serverUrls.length > 0) {
        essential.server_url = serverUrls[0].url;
        essential.full_url = serverUrls[0].url;
        // Endpoint ka soo qaado
        const urlObj = serverUrls[0].url;
        const pathMatch = urlObj.match(/https?:\\/\\/[^\\/]+(\\/[^\\s"']*)?/);
        if (pathMatch && pathMatch[1]) {
            essential.endpoint = pathMatch[1];
        } else {
            essential.endpoint = '/';
        }
    }

    // 2. DEX — license methods + JSON fields
    const methodKw = ['login', 'validate', 'checkLicense', 'verifyLicense', 'auth', 'connect', 'statusTrue', 'isValid', 'performLogin', 'nativeValidateLicense', 'checkKey'];
    const jsonKw = ['"status"', '"success"', '"data"', '"reason"', '"EXP"', '"expired_date"', '"license"', '"key"', '"valid"', '"message"'];

    for (const dex of dexFiles) {
        // Dex waa la baadhay horey — kaliya soo qaado keyword-yada
    }

    return essential;
}

// Parse AndroidManifest.xml (binary XML)"""

if old_marker in c:
    c = c.replace(old_marker, new_marker, 1)
    print("1. extractEssential: OK")
else:
    print("1. extractEssential: LAMA HELIN")

# Ku dar essential-ka response-ka
old_res = "        result.filename = filename;"
new_res = """        result.essential = extractEssential(result.urls, result.dex_files);
        result.filename = filename;"""

if old_res in c:
    c = c.replace(old_res, new_res, 1)
    print("2. Response essential: OK")
else:
    print("2. Response essential: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_essential")
