const fs = require('fs');
let code = fs.readFileSync('server.js', 'utf8');

// Beddel response-ka KingMod
const oldBlock = /res\.json\(\{\s*status: 'success',[\s\S]*?latest_apk_version: '3\.5'\s*\}\);/;

const newBlock = `res.json({
      status: 'success',
      appStatus: 'active',
      httpCode: 200,
      message: 'License valid',
      remaining_seconds: 31536000,
      remaining_text: '365 days',
      package_name: 'com.pubg.obsidian',
      policy_version: 1,
      documentVersion: '3.5',
      version: '3.5',
      latest_version: '3.5',
      apk: { version: '3.5', required: false },
      latest_file: { apk: { version: '3.5', required: false } },
      app_update_required: false,
      update_required: false,
      latest_apk_version: '3.5'
    });`;

const count = (code.match(oldBlock) || []).length;
console.log('Found ' + count + ' occurrences');

code = code.replace(oldBlock, newBlock);
fs.writeFileSync('server.js', code);
console.log('PATCHED');
