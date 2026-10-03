const fs = require('fs');
let code = fs.readFileSync('server.js', 'utf8');

// Ku dar documentVersion iyo policy_version
code = code.replace(
  /policy_version: 1,/g,
  "policy_version: 1,\n      documentVersion: '3.5',\n      version_code: 5,"
);

fs.writeFileSync('server.js', code);
console.log('PATCHED');
