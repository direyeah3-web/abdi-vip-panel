# fix_zoom_final.py - Hagaaji zoom-ka si uu u noqdo 0.5

with open("public/index.html", "r") as f:
    content = f.read()

# Beddel viewport-ka
import re
content = re.sub(
    r'<meta name="viewport"[^>]*>',
    '<meta name="viewport" content="width=900, initial-scale=0.5, maximum-scale=3.0, user-scalable=yes">',
    content
)

# Beddel min-width-ka
content = content.replace('min-width: 1100px;', 'min-width: 900px;')

with open("public/index.html", "w") as f:
    f.write(content)

print("✅ Viewport-ka waa la beddelay (0.5)!")
