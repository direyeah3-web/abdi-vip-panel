# fix_register_v3.py - Tirtir fulIname:f (f is not defined)

with open("public/index.html", "r") as f:
    content = f.read()

# Calaamadda saxda ah - fulIname:f,
old_code = "fulIname:f,referral_code:ref"
new_code = "referral_code:ref"

if old_code in content:
    content = content.replace(old_code, new_code)
    with open("public/index.html", "w") as f:
        f.write(content)
    print("✅ fulIname:f waa la tirtiray!")
else:
    print("⚠️ Code-ka lama helin — isku day qaab kale")

# Hubi haddii uu wali jiro
if "fulIname" in content:
    print("⚠️ fulIname wali wuu jiraa!")
else:
    print("✅ fulIname waa la tirtiray gebi ahaan!")
