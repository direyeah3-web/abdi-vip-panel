const fs = require('fs');
let code = fs.readFileSync('server.js', 'utf8');

// Ku dar state: 'online' response-ka
code = code.replace(
  /status: 'success',/g,
  "status: 'success',\n      state: 'online',\n      message: '',"
);

fs.writeFileSync('server.js', code);
console.log('PATCHED');
