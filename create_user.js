// create_user.js - Abuur user cusub database-ka Railway
const initSqlJs = require('sql.js');
const bcrypt = require('bcryptjs');
const fs = require('fs');

const DB_FILE = './abdi.db';

initSqlJs().then(SQL => {
    let db;
    if (fs.existsSync(DB_FILE)) {
        db = new SQL.Database(fs.readFileSync(DB_FILE));
    } else {
        db = new SQL.Database();
    }
    
    // Abuur user cusub
    const username = 'admin8';
    const password = 'admin1234';
    const hashed = bcrypt.hashSync(password, 10);
    
    // Hubi haddii user-ku jiro
    const existing = db.exec(`SELECT id FROM users WHERE username = '${username}'`);
    if (existing.length > 0 && existing[0].values.length > 0) {
        console.log("⚠️ User-ku horey ayuu u jiray!");
    } else {
        db.run("INSERT INTO users (username, password, fullname, role) VALUES (?, ?, ?, ?)", 
            [username, hashed, username, 'admin']);
        fs.writeFileSync(DB_FILE, Buffer.from(db.export()));
        console.log("✅ User cusub waa la abuuray!");
        console.log("📝 Username:", username);
        console.log("🔑 Password:", password);
    }
});
