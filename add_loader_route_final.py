# add_loader_route_final.py - Ku dar static route loader-ka server.js

with open("server.js", "r") as f:
    content = f.read()

# Hubi haddii route-ku horey u jiro
if "app.use('/loader'" in content or 'app.use("/loader"' in content:
    print("⚠️ Route-ka loader-ka horey ayuu u jiray!")
else:
    # Raadi 'app.use(express.json())' ama 'app.use(express.urlencoded'
    target1 = "app.use(express.json())"
    target2 = "app.use(express.urlencoded"
    
    loader_code = """
// ===== LOADER STATIC ROUTE =====
app.use('/loader', express.static(__dirname + '/loader'));

"""
    
    if target1 in content:
        # Ku dar ka dib app.use(express.json())
        new_content = content.replace(target1, target1 + "\n" + loader_code, 1)
        with open("server.js", "w") as f:
            f.write(new_content)
        print("✅ Route-ka loader-ka waa lagu daray (ka dib express.json)!")
    elif target2 in content:
        # Hel meesha uu ku dhammaado
        idx = content.find(target2)
        end_idx = content.find("\n", idx)
        if end_idx == -1:
            end_idx = len(content)
        new_content = content[:end_idx] + "\n" + loader_code + content[end_idx:]
        with open("server.js", "w") as f:
            f.write(new_content)
        print("✅ Route-ka loader-ka waa lagu daray (ka dib express.urlencoded)!")
    else:
        # Ku dar ka hor app.listen
        listen_pos = content.find("app.listen(PORT")
        if listen_pos != -1:
            new_content = content[:listen_pos] + loader_code + "\n" + content[listen_pos:]
            with open("server.js", "w") as f:
                f.write(new_content)
            print("✅ Route-ka loader-ka waa lagu daray (ka hor app.listen)!")
        else:
            print("❌ Ma helin meesha saxda ah")
