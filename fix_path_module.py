#!/usr/bin/env python3
import shutil, os, sys

SERVER = os.path.expanduser('~/abdi-panel/server.js')
BACKUP = SERVER + '.backup_before_path_fix'

if not os.path.exists(SERVER):
    print("LAMA HELIN: server.js")
    sys.exit(1)

shutil.copy(SERVER, BACKUP)
print(f"Backup: {BACKUP}")

with open(SERVER, 'r', encoding='utf-8') as f:
    content = f.read()

# Hubi haddii horey loo daray
if "const path = require('path')" in content or 'const path=require' in content:
    print("HOREY AYAA LA DARAY: const path = require('path')")
    # Hubi line 1363
    lines = content.split('\n')
    if len(lines) > 1363:
        print(f"Line 1363: {lines[1362].strip()}")
        print(f"Line 1364: {lines[1363].strip()}")
    sys.exit(0)

# Raadi line 1363
lines = content.split('\n')
if len(lines) > 1363:
    print(f"Line 1362: {lines[1361].strip()}")
    print(f"Line 1363: {lines[1362].strip()}")
    print(f"Line 1364: {lines[1363].strip()}")

# Soo raadi meesha `const fs = require('fs')` ama `const express = require` ee hore
# Wixii ka dambeeya `const app = express()` — halkaas `require('path')` ku dar
marker = "const app = express()"
if marker not in content:
    marker = "const app=express()"
if marker not in content:
    print("LAMA HELIN: const app = express()")
    sys.exit(1)

replacement = marker + "\nconst path = require('path');"

content = content.replace(marker, replacement, 1)

with open(SERVER, 'w', encoding='utf-8') as f:
    f.write(content)

print("OK: const path = require('path') la daray")
