#!/usr/bin/env python3
import shutil, os, sys, re

SERVER = os.path.expanduser('~/abdi-panel/server.js')
BACKUP = SERVER + '.backup_before_auto_patch'

if not os.path.exists(SERVER):
    print("LAMA HELIN: server.js")
    sys.exit(1)

shutil.copy(SERVER, BACKUP)
print(f"Backup: {BACKUP}")

with open(SERVER, 'r', encoding='utf-8') as f:
    content = f.read()

if 'AUTO_PATCH_TRIGGERED' in content:
    print("HOREY AYAA LA DARAY")
    sys.exit(0)

# Raadi meesha analyze-ku natiijada dirayo: `res.json(result);`
# Tan waa line-ka ugu dambeeya ee analyze function-ka
old = """      result.filename = filename;
      result.success = true;

      res.json(result);"""

new = """      result.filename = filename;
      result.success = true;
      result.apkPath = apkPath;

      // AUTO-PATCH: trigger GitHub Actions si toos ah
      try {
        const ghRepo = process.env.GH_REPO || 'direyeah3-web/abdi-patcher';
        const ghToken = process.env.GH_TOKEN;
        const panelUrl = process.env.PANEL_URL || 'https://abdi-vip-panel-production.up.railway.app';
        const webhookSecret = process.env.PANEL_WEBHOOK_SECRET || '';

        if (ghToken) {
          const jobId = 'j_' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
          const apkFilename = require('path').basename(apkPath);

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

          // Fire and forget
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

      res.json(result);"""

if old not in content:
    print("LAMA HELIN: analyze response block")
    print("Raadi 'result.filename = filename;' oo soo bandhig 5 line kadib:")
    idx = content.find('result.filename = filename')
    if idx != -1:
        print(content[idx-100:idx+400])
    sys.exit(1)

content = content.replace(old, new, 1)

with open(SERVER, 'w', encoding='utf-8') as f:
    f.write(content)

print("OK: auto-patch la daray")
