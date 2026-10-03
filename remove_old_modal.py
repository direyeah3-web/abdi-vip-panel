# remove_old_modal.py - Ka saar showGenerateLicenseModal hore

with open("public/index.html", "r") as f:
    content = f.read()

# Hel meesha showGenerateLicenseModal ka bilaabmo
start = content.find("function showGenerateLicenseModal()")

if start != -1:
    print("✅ Waxaan helay showGenerateLicenseModal hore.")
    
    # Hel meesha uu ku dhammaado (function xigta)
    end = content.find("function showAddUserModal()", start)
    
    if end == -1:
        end = content.find("function toggleProfileMenu()", start)
    
    if end != -1:
        # Ka saar function-kii hore
        new_content = content[:start] + content[end:]
        with open("public/index.html", "w") as f:
            f.write(new_content)
        print("✅ Function-kii hore waa la saaray!")
    else:
        print("❌ Ma helin meesha uu ku dhammaado.")
else:
    print("⚠️ Ma helin showGenerateLicenseModal hore.")
