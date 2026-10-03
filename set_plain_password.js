// set_plain_password.js - Beddel password-ka user-ka 'abdi' mid caadi ah
const initSqlJs = require('sql.js');
const fs = require('fs');

initSqlJs().then(SQL => {
    const db = new SQL.Database(fs.readFileSync('abdi.db'));
    
    // Beddel password-ka mid caadi ah (ma aha bcrypt)
    db.run("UPDATE users SET password = ? WHERE username = ?", ['abdi123', 'abdi']);
    
    fs.writeFileSync('abdi.db', Buffer.from(db.export()));
    console.log("✅ Password-ka 'abdi' waa la beddelay mid caadi ah: abdi123");
});
