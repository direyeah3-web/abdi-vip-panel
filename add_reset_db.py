# add_reset_db.py - Ku dar koodh tirtira database-ka marka la bilaabo

with open("server.js", "r") as f:
    content = f.read()

reset_code = '''
// ===== RESET DATABASE (TEMPORARY) =====
if (process.env.RESET_DB === 'true') {
    try {
        if (fs.existsSync(DB_FILE)) {
            fs.unlinkSync(DB_FILE);
            console.log('🗑️ Database file deleted!');
        }
    } catch(e) {
        console.log('Reset error:', e.message);
    }
}
'''

# Ku dar ka hor "if (fs.existsSync(DB_FILE))"
target = "if (fs.existsSync(DB_FILE))"
target_pos = content.find(target)

if target_pos != -1 and 'RESET_DB' not in content:
    new_content = content[:target_pos] + reset_code + "\n" + content[target_pos:]
    with open("server.js", "w") as f:
        f.write(new_content)
    print("✅ Reset DB code waa lagu daray!")
elif 'RESET_DB' in content:
    print("⚠️ Reset DB code horey ayuu u jiray!")
else:
    print("❌ Ma helin target")
