const fs = require('fs');
let code = fs.readFileSync('server.js', 'utf8');

// Dib u dhis response-ka
code = code.replace(
  /status: 'success',\s*state: 'online',\s*message: '',/g,
  `status: 'success',
      success: true,
      is_valid: true,
      state: 'online',
      message: 'License valid',`
);

fs.writeFileSync('server.js', code);
console.log('PATCHED');
