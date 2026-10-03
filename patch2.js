const fs = require('fs');
let code = fs.readFileSync('server.js', 'utf8');

// Ku dar valid iyo success response-ka ObsidianAuth POST
const oldLine = "      message: 'License valid',\n      latest_apk_version: '4.6.0'\n    });";
const newLine = "      valid: true,\n      isValid: true,\n      success: true,\n      message: 'License valid',\n      latest_apk_version: '4.6.0'\n    });";

const count = (code.match(/message: 'License valid',/g) || []).length;
console.log('Found ' + count + ' occurrences');

code = code.replace(/message: 'License valid',\n      latest_apk_version: '4\.6\.0'\n    \}\);/g,
  "valid: true,\n      isValid: true,\n      success: true,\n      message: 'License valid',\n      latest_apk_version: '4.6.0'\n    });"
);

fs.writeFileSync('server.js', code);
console.log('PATCHED');
