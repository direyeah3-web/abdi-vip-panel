# add_admin_creation.py - Ku dar auto-create admin user server.js

with open("server.js", "r") as f:
    content = f.read()

# Qoraalka aan rabno inaan ku darno ka hor app.listen
admin_code = '''
// ===== AUTO CREATE ADMIN USER =====
if (process.env.CREATE_ADMIN_USER) {
    const parts = process.env.CREATE_ADMIN_USER.split(':');
    const adminUser = parts[0];
    const adminPass = parts[1];
    if (adminUser && adminPass) {
        const existing = queryOne('SELECT id FROM users WHERE username = ?', [adminUser]);
        if (!existing) {
            const hashedPass = bcrypt.hashSync(adminPass, 10);
            db.run("INSERT INTO users (username, password, fullname, role) VALUES (?, ?, ?, ?)", 
                [adminUser, hashedPass, adminUser, 'admin']);
            saveDB();
            console.log('✅ Admin user created: ' + adminUser);
        } else {
            console.log('ℹ️ Admin user already exists: ' + adminUser);
        }
    }
}
'''

# Hubi haddii code-ku horey u jiro
if 'CREATE_ADMIN_USER' in content:
    print("⚠️ Code-ku horey ayuu u jiray!")
else:
    # Ku dar ka hor app.listen
    old_listen = "app.listen(PORT"
    new_content = content.replace(old_listen, admin_code + "\n" + old_listen, 1)
    
    if new_content != content:
        with open("server.js", "w") as f:
            f.write(new_content)
        print("✅ Code-ka auto-create admin user waa lagu daray server.js!")
    else:
        print("❌ Ma helin 'app.listen(PORT' gudaha server.js")
