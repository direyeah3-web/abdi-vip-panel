# fix_modern_button.py - Beddel botton-ka si uu u waco modal-ka cusub

with open("public/index.html", "r") as f:
    content = f.read()

# Beddel dhammaan bottonada Generate License
old1 = 'onclick="showGenerateLicenseModal()"'
new1 = 'onclick="showModernLicenseModal()"'

if old1 in content:
    content = content.replace(old1, new1)
    print("✅ Botton-ka Generate License waa la beddelay!")
else:
    print("⚠️ Botton-ka lama helin")

# Beddel sidoo kale haddii uu jiro showLicenseModal
old2 = 'onclick="showLicenseModal()"'
new2 = 'onclick="showModernLicenseModal()"'

if old2 in content:
    content = content.replace(old2, new2)
    print("✅ Botton-ka showLicenseModal waa la beddelay!")

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
