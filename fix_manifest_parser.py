import shutil
import re

shutil.copy('server.js', 'server.js.backup_manifest')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Ku dar function cusub parseManifest
old = "const AdmZip = require('adm-zip');"
new = """const AdmZip = require('adm-zip');

// Parse AndroidManifest.xml (binary XML)
function parseManifest(buf) {
    const result = { package_name: null, launcher: null, application: null, permissions: [] };
    try {
        const str = buf.toString('latin1');
        // Package name: usually near "package" attribute
        const pkgMatch = str.match(/(com\\.[a-z0-9_]+\\.[a-z0-9_.]+)/i);
        if (pkgMatch) result.package_name = pkgMatch[1];
        // Launcher activity: contains "android.intent.action.MAIN" + "LAUNCHER"
        const actMatches = str.match(/([A-Z][a-zA-Z0-9_]*(?:Activity|MainActivity))/g);
        if (actMatches) result.launcher = actMatches[actMatches.length - 1];
        // Application class
        const appMatches = str.match(/([A-Z][a-zA-Z0-9_]*Application)/g);
        if (appMatches) result.application = appMatches[appMatches.length - 1];
        // Permissions
        const permMatches = str.match(/android\\.permission\\.[A-Z_]+/g) || [];
        result.permissions = [...new Set(permMatches)];
    } catch (e) {}
    return result;
}"""

if old in c:
    c = c.replace(old, new, 1)
    print("1. parseManifest function: OK")
else:
    print("1. parseManifest: LAMA HELIN")

# Beddel qaybta manifest-ka
old_m = """        const manifestPath = tmpDir + '/AndroidManifest.xml';
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
        }"""

new_m = """        const manifestPath = tmpDir + '/AndroidManifest.xml';
        if (fs.existsSync(manifestPath)) {
            try {
                const buf = fs.readFileSync(manifestPath);
                const manifest = parseManifest(buf);
                result.package_name = manifest.package_name || 'N/A';
                result.launcher_activity = manifest.launcher || 'N/A';
                result.application_class = manifest.application || 'N/A';
                result.permissions = manifest.permissions || [];
            } catch (e) {}
        }"""

if old_m in c:
    c = c.replace(old_m, new_m, 1)
    print("2. Manifest parse: OK")
else:
    print("2. Manifest parse: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_manifest")
