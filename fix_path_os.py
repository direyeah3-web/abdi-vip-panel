#!/usr/bin/env python3
import shutil, os, sys

SERVER = os.path.expanduser('~/abdi-panel/server.js')
BACKUP = SERVER + '.backup_before_path_os_fix'

if not os.path.exists(SERVER):
    print("LAMA HELIN: server.js")
    sys.exit(1)

shutil.copy(SERVER, BACKUP)
print(f"Backup: {BACKUP}")

with open(SERVER, 'r', encoding='utf-8') as f:
    content = f.read()

# Hubi haddii path horey loo daray
has_path = "const path = require('path')" in content or "const path=require" in content
# Hubi haddii os horey loo daray
has_os = "const os = require('os')" in content or "const os=require" in content

print(f"path exists: {has_path}")
print(f"os exists: {has_os}")

if has_path and has_os:
    print("OK: labada module horey ayaa la daray")
    sys.exit(0)

# Raadi `const app = express()` oo ku dar modules-ka
marker = "const app = express()"
if marker not in content:
    marker = "const app=express()"
if marker not in content:
    print("LAMA HELIN: const app = express()")
    sys.exit(1)

add_lines = []
if not has_path:
    add_lines.append("const path = require('path');")
if not has_os:
    add_lines.append("const os = require('os');")

replacement = marker + "\n" + "\n".join(add_lines)
content = content.replace(marker, replacement, 1)

with open(SERVER, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"OK: {len(add_lines)} module la daray")
for l in add_lines:
    print(f"  + {l}")
