# fix_zoom.py - Hagaaji zoom-ka si uu u noqdo mid dhexdhexaad ah

with open("public/index.html", "r") as f:
    content = f.read()

# Beddel viewport-ka
old_viewport = '<meta name="viewport" content="width=1280, initial-scale=0.25, maximum-scale=5.0, user-scalable=yes">'
new_viewport = '<meta name="viewport" content="width=1100, initial-scale=0.35, maximum-scale=3.0, user-scalable=yes">'

if old_viewport in content:
    content = content.replace(old_viewport, new_viewport)
    print("✅ Viewport-ka waa la hagaajiyay (0.35)!")
else:
    # Isku day inaad hesho viewport kasta
    import re
    content = re.sub(
        r'<meta name="viewport"[^>]*>',
        '<meta name="viewport" content="width=1100, initial-scale=0.35, maximum-scale=3.0, user-scalable=yes">',
        content
    )
    print("✅ Viewport-ka waa la hagaajiyay (regex)!")

# Beddel min-width-ka
content = content.replace('min-width: 1280px;', 'min-width: 1100px;')

with open("public/index.html", "w") as f:
    f.write(content)

print("✅ Faylka waa la keydiyay!")
