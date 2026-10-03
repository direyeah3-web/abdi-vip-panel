const fs = require('fs');
let code = fs.readFileSync('server.js', 'utf8');

// Raadi response block-ka ObsidianAuth POST
const oldBlock = /res\.json\(\{\s*status:\s*true,[\s\S]*?latest_apk_version:\s*'4\.6\.0'\s*\}\);/;

const newBlock = `res.json({
      status: 'success',
      success: true,
      is_valid: true,
      message: 'License valid',
      http_code: 200,
      remaining_seconds: 31536000,
      remaining_text: '365 days',
      package_name: 'com.pubg.obsidian',
      policy_version: 1,
      data: {
        EXP: '2026-11-01',
        expires: '2026-11-01',
        remaining_seconds: 31536000,
        remaining_text: '365 days',
        version: '4.6.0',
        latest_version: '4.6.0'
      },
      apk: { version: '4.6.0', required: false },
      latest_file: { apk: { version: '4.6.0', required: false } },
      app_update_required: false,
      update_required: false,
      latest_apk_version: '4.6.0'
    });`;

const count = (code.match(oldBlock) || []).length;
console.log('Found ' + count + ' occurrences');

code = code.replace(oldBlock, newBlock);
fs.writeFileSync('server.js', code);
console.log('PATCHED');
