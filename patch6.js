const fs = require('fs');
let code = fs.readFileSync('server.js', 'utf8');

// Ku dar nativeInit iyo getRegister/setRegister fields
code = code.replace(
  /package_name: 'com\.pubg\.obsidian',/g,
  "package_name: 'com.pubg.obsidian',\n      nativeInit: true,\n      getRegister: 'ABDI-VIP-REGISTER',\n      setRegister: true,\n      getSavedRegister: 'ABDI-VIP-REGISTER',\n      register: 'ABDI-VIP-REGISTER',\n      registered: true,"
);

fs.writeFileSync('server.js', code);
console.log('PATCHED');
