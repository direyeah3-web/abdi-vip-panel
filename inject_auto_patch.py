#!/usr/bin/env python3
import shutil, os, sys

SERVER = os.path.expanduser('~/abdi-panel/server.js')
BACKUP = SERVER + '.backup_before_auto_patch'

if not os.path.exists(SERVER):
    print("LAMA HELIN: server.js")
    sys.exit(1)

shutil.copy(SERVER, BACKUP)
print(f"Backup: {BACKUP}")

with open(SERVER, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Hubi line 1294 (index 1293) — waa in ay tahay "res.json(result);"
idx = 1293
if idx >= len(lines):
    print(f"LAMA HELIN: line {idx+1} ma jiro")
    sys.exit(1)

line_1294 = lines[idx].strip()
print(f"Line 1294: {line_1294}")

if 'res.json(result)' not in line_1294:
    print("LAMA HELIN: line 1294 ma aha res.json(result)")
    print("Raadi line-ka saxda ah:")
    for i, l in enumerate(lines):
        if 'res.json(result)' in l:
            print(f"  Line {i+1}: {l.strip()}")
    sys.exit(1)

# Hubi line 1291 (index 1290)
line_1291 = lines[1290].strip()
print(f"Line 1291: {line_1291}")

if 'result.filename' not in line_1291:
    print("LAMA HELIN: line 1291 ma aha result.filename")
    sys.exit(1)

# Code-ka cusub — auto-patch
auto_patch_code = '''
      // ============ AUTO-PATCH TRIGGER ============
      try {
        const pathMod = require('path');
        const ghRepo = process.env.GH_REPO || 'direyeah3-web/abdi-patcher';
        const ghToken = process.env.GH_TOKEN;
        const panelUrl = process.env.PANEL_URL || 'https://abdi-vip-panel-production.up.railway.app';

        if (ghToken) {
          const jobId = 'j_' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
          const apkFilename = pathMod.basename(apkPath);

          if (!global.patchJobs) global.patchJobs = new Map();
          global.patchJobs.set(jobId, {
            status: 'queued',
            apkPath: apkPath,
            filename: apkFilename,
            createdAt: Date.now(),
          });

          const ghBody = JSON.stringify({
            ref: 'main',
            inputs: {
              apk_url: panelUrl + '/api/apk/raw/' + apkFilename,
              job_id: jobId,
              patch_options: '{}',
            },
          });

          fetch('https://api.github.com/repos/' + ghRepo + '/actions/workflows/patch.yml/dispatches', {
            method: 'POST',
            headers: {
              'Authorization': 'Bearer ' + ghToken,
              'Accept': 'application/vnd.github+json',
              'Content-Type': 'application/json',
            },
            body: ghBody,
          }).then(r => {
            console.log('AUTO_PATCH_TRIGGERED: ' + jobId + ' status=' + r.status);
          }).catch(e => {
            console.log('AUTO_PATCH_ERROR: ' + e.message);
          });

          result.patchJobId = jobId;
          result.patchStatus = 'queued';
        } else {
          result.patchStatus = 'skipped_no_token';
        }
      } catch (e) {
        result.patchError = e.message;
      }
      // ============ END AUTO-PATCH ============
'''

# Ku dar auto-patch code-ka ka hor line 1294 (res.json(result);)
new_lines = lines[:idx] + [auto_patch_code] + lines[idx:]

with open(SERVER, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"OK: auto-patch la daray line {idx+1} ka hor")
print(f"Lines cusub: {len(new_lines)}")
