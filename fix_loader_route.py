# fix_loader_route.py - Ku dar route-ka loader-ka server.js

with open("server.js", "r") as f:
    content = f.read()

if "/loader" in content and "express.static" in content:
    print("⚠️ Route-ka loader-ka horey ayuu u jiray!")
else:
    loader_code = """
// ===== LOADER STATIC ROUTE =====
app.use('/loader', express.static(__dirname + '/loader'));

"""
    # Ku dar ka hor app.use(express.static('public'))
    target = "app.use(express.static('public'))"
    target_pos = content.find(target)
    
    if target_pos == -1:
        # Isku day inaad hesho nooc kale
        target = "express.static"
        target_pos = content.find(target)
    
    if target_pos != -1:
        # Ku dar ka hor static-ka public
        new_content = content[:target_pos] + loader_code + content[target_pos:]
        with open("server.js", "w") as f:
            f.write(new_content)
        print("✅ Route-ka loader-ka waa lagu daray!")
    else:
        # Haddii aysan jirin static, ku dar ka hor app.listen
        listen_pos = content.find("app.listen(PORT")
        if listen_pos != -1:
            new_content = content[:listen_pos] + loader_code + content[listen_pos:]
            with open("server.js", "w") as f:
                f.write(new_content)
            print("✅ Route-ka loader-ka waa lagu daray (ka hor app.listen)!")
        else:
            print("❌ Ma helin meesha saxda ah")
