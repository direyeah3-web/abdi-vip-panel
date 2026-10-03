# add_admin_user.py - Ku dar koodh abuura user cusub marka server-ku bilaabo

with open("server.js", "r") as f:
    content = f.read()

# Calaamadda koodhka cusub
admin_code = """
// ===== AUTO CREATE ADMIN USER =====
if (process.env.CREATE_ADMIN_USER) {
    try {
        const parts = process.env.CREATE_ADMIN_USER.split(':');
        const adminUser = parts[0];
        const adminPass = parts[1];
        if (adminUser && adminPass) {
            const existing = queryOne('SELECT id FROM users WHERE username = ?', [adminUser]);
            if (!existing) {
                db.run("INSERT INTO users (username, password, fullname, role) VALUES (?, ?, ?, ?)", 
                    [adminUser, adminPass, adminUser, 'admin']);
                saveDB();
                console.log('✅ Admin user created: ' + adminUser);
            } else {
                console.log('ℹ️ Admin user already exists: ' + adminUser);
            }
        }
    } catch (e) {
        console.log('❌ Error creating admin:', e.message);
    }
}
"""

# Hubi haddii code-ku horey u jiro
if 'CREATE_ADMIN_USER' in content:
    print("⚠️ Code-ku horey ayuu u jiray! Waxaan ka saareynaa kii hore...")
    # Ka saar kii hore
    start = content.find("// ===== AUTO CREATE ADMIN USER =====")
    end = content.find("app.listen(PORT", start)
    if start != -1 and end != -1:
        content = content[:start] + content[end:]
        print("✅ Kii hore waa la saaray.")

# Ku dar ka hor app.listen
listen_pos = content.find("app.listen(PORT")
if listen_pos != -1:
    new_content = content[:listen_pos] + admin_code + "\n" + content[listen_pos:]
    with open("server.js", "w") as f:
        f.write(new_content)
    print("✅ Koodhka cusub waa lagu daray server.js!")
else:
    print("❌ Ma helin app.listen(PORT")
