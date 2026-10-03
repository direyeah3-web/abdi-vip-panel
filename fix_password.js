// Faylkan wuxuu beddelaa password-ka user-ka 'abdi' si uu u noqdo 'abdi123'

const initSqlJs = require('sql.js');
const bcrypt = require('bcryptjs');
const fs = require('fs');

initSqlJs().then(SQL => {
    // Akhri database-ka
    const db = new SQL.Database(fs.readFileSync('abdi.db'));
    
    // Samee password hash cusub
    const newPassword = 'abdi123';
    const hashedPassword = bcrypt.hashSync(newPassword, 10);
    
    // Beddel password-ka user-ka 'abdi'
    db.run("UPDATE users SET password = ? WHERE username = ?", [hashedPassword, 'abdi']);
    
    // Keydi database-ka
    fs.writeFileSync('abdi.db', Buffer.from(db.export()));
    
    console.log("✅ Password-ka user-ka 'abdi' waa la beddelay!");
    console.log("📝 Username: abdi");
    console.log("🔑 Password: abdi123");
    
    // Hubi inuu shaqeeyay
    const res = db.exec("SELECT id, username, role FROM users WHERE username = 'abdi'");
    console.log("📊 User-ka cusub:", JSON.stringify(res, null, 2));
});
