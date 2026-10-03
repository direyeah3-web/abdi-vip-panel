# change_branding.py - Beddel magaca loader-ka

with open("loader/index.html", "r") as f:
    content = f.read()

# Beddel magaca
content = content.replace("Obsidian Bypass", "ABDI VIP BYPASS")
content = content.replace("obsidian_title", "abdi_title")
content = content.replace("obsidian-title", "abdi-title")
content = content.replace("Obsidian", "ABDI VIP")
content = content.replace("obsidian_", "abdi_")

with open("loader/index.html", "w") as f:
    f.write(content)

print("✅ Magaca loader-ka waa la beddelay (ABDI VIP BYPASS)!")
