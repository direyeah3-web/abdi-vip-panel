const fs = require('fs');
let code = fs.readFileSync('server.js', 'utf8');

// Ku dar nativeInit gudaha data object
code = code.replace(
  /data: \{\s*EXP: '2026-11-01',/g,
  "data: {\n        nativeInit: true,\n        getRegister: 'ABDI-VIP-REGISTER',\n        setRegister: true,\n        EXP: '2026-11-01',"
);

fs.writeFileSync('server.js', code);
console.log('PATCHED');
