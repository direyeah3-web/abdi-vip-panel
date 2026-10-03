const fs = require('fs');
let code = fs.readFileSync('server.js', 'utf8');

// Ku dar OBJECT iyo DATA fields
code = code.replace(
  /package_name: 'com\.pubg\.obsidian',/g,
  "package_name: 'com.pubg.obsidian',\n      OBJECT: {\n        EXP: '2026-11-01',\n        expires: '2026-11-01',\n        remaining_seconds: 31536000,\n        remaining_text: '365 days',\n        is_valid: true,\n        success: true\n      },\n      DATA: {\n        EXP: '2026-11-01',\n        expires: '2026-11-01',\n        remaining_seconds: 31536000\n      },"
);

fs.writeFileSync('server.js', code);
console.log('PATCHED');
