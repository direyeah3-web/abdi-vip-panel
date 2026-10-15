#!/usr/bin/env python3
import shutil, os, sys

SERVER = os.path.expanduser('~/abdi-panel/server.js')
BACKUP = SERVER + '.backup_before_apk_logging'

if not os.path.exists(SERVER):
    print("LAMA HELIN: server.js")
    sys.exit(1)

shutil.copy(SERVER, BACKUP)
print(f"Backup: {BACKUP}")

with open(SERVER, 'r', encoding='utf-8') as f:
    content = f.read()

# Hubi haddii horey loo daray
if 'APK_UPLOAD_PATH:' in content:
    print("HOREY AYAA LA DARAY")
    sys.exit(0)

# Raadi endpoint /api/apk/upload oo ku dar console.log
old = """      const buffer = Buffer.from(data, 'base64');
      const hash = crypto.createHash('md5').update(buffer).digest('hex');
      const tempPath = '/tmp/apk_' + hash + '.apk';
      fs.writeFileSync(tempPath, buffer);"""

new = """      const buffer = Buffer.from(data, 'base64');
      const hash = crypto.createHash('md5').update(buffer).digest('hex');
      const tempPath = '/tmp/apk_' + hash + '.apk';
      fs.writeFileSync(tempPath, buffer);
      console.log('APK_UPLOAD_PATH: ' + tempPath);
      console.log('APK_UPLOAD_NAME: ' + filename);
      console.log('APK_UPLOAD_SIZE: ' + buffer.length);"""

if old not in content:
    print("LAMA HELIN: upload code block")
    print("Halkan soo bandhig:")
    # Print 10 lines around 'tempPath'
    idx = content.find('tempPath')
    if idx != -1:
        print(content[idx-200:idx+300])
    sys.exit(1)

content = content.replace(old, new, 1)

with open(SERVER, 'w', encoding='utf-8') as f:
    f.write(content)

print("OK: console.log la daray")
