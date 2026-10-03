# remove_zoom.py - Ka saar zoom-ka si boggu u noqdo PC-style

with open("public/index.html", "r") as f:
    content = f.read()

# Beddel viewport meta tag-ka si uu u noqdo desktop view
old_viewport = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
new_viewport = '<meta name="viewport" content="width=1280, initial-scale=0.25, maximum-scale=5.0, user-scalable=yes">'

if old_viewport in content:
    content = content.replace(old_viewport, new_viewport)
    print("✅ Viewport meta tag waa la beddelay (desktop view)!")
else:
    print("⚠️ Viewport meta tag lama helin. Waxaan isku dayayaa beddel kale...")
    # Isku day inaad hesho viewport kasta
    import re
    content = re.sub(
        r'<meta name="viewport"[^>]*>',
        '<meta name="viewport" content="width=1280, initial-scale=0.25, maximum-scale=5.0, user-scalable=yes">',
        content
    )
    print("✅ Viewport meta tag waa la beddelay (regex)!")

# Beddel media query-ga si uusan u beddelin qaabka mobile-ka
old_media_start = content.find("@media(max-width:768px){")
if old_media_start == -1:
    old_media_start = content.find("@media(max-width: 768px)")

if old_media_start != -1:
    # Hel meesha uu ku dhammaado
    brace_count = 0
    i = old_media_start
    found_start = False
    end_media = -1
    while i < len(content):
        if content[i] == '{':
            brace_count += 1
            found_start = True
        elif content[i] == '}':
            brace_count -= 1
            if found_start and brace_count == 0:
                end_media = i + 1
                break
        i += 1
    
    if end_media != -1:
        # Ka saar media query-ga
        content = content[:old_media_start] + content[end_media:]
        print("✅ Media query-ga mobile-ka waa la saaray!")

# Ku dar CSS cusub si boggu u noqdo mid PC ah
desktop_css = '''
<style>
/* ===== FORCE DESKTOP VIEW ===== */
html, body {
    min-width: 1280px;
}
.sidebar {
    width: 260px !important;
}
.sidebar-brand, .nav-item span, .nav-section, .user-info {
    display: block !important;
}
.nav-item {
    justify-content: flex-start !important;
}
.main {
    margin-left: 260px !important;
}
.content-grid {
    grid-template-columns: 2fr 1fr !important;
}
.stats-grid {
    grid-template-columns: repeat(4, 1fr) !important;
}
.search-bar {
    width: 400px !important;
}
.topnav {
    padding: 15px 30px !important;
    flex-wrap: nowrap !important;
}
.hero {
    padding: 35px !important;
}
.hero h1 {
    font-size: 32px !important;
}
.page {
    padding: 30px !important;
}
.menu-toggle {
    display: none !important;
}
.mobile-overlay {
    display: none !important;
}
</style>
'''

# Ku dar CSS-ka cusub ka hor </head>
head_pos = content.find("</head>")
if head_pos != -1:
    content = content[:head_pos] + desktop_css + content[head_pos:]
    print("✅ CSS-ka desktop view waa lagu daray!")

with open("public/index.html", "w") as f:
    f.write(content)

print("✅ Faylka 'public/index.html' waa la cusboonaysiiyay!")
