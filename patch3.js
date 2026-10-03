const fs = require('fs');
let code = fs.readFileSync('server.js', 'utf8');

// Ku dar remaining_text iyo register response-ka
code = code.replace(
  /remaining_seconds: 31536000,/g,
  "remaining_seconds: 31536000,\n        remaining_text: '365 days',"
);

// Ku dar register field
code = code.replace(
  /valid: true,\n      isValid: true,\n      success: true,/g,
  "valid: true,\n      isValid: true,\n      success: true,\n      register: 'ABDI-VIP-REGISTER',\n      registered: true,"
);

fs.writeFileSync('server.js', code);
console.log('PATCHED');
