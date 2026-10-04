# fix_generate_license.py - Hagaaji endpoint-ka generate license

with open("public/index.html", "r") as f:
    content = f.read()

# Beddel endpoint-ka khaldan
content = content.replace("fetch('/api/licenses/bulk'", "fetch('/api/admin/licenses/bulk'")
content = content.replace('fetch("/api/licenses/bulk"', 'fetch("/api/admin/licenses/bulk"')
content = content.replace("fetch('/api/licenses/generate'", "fetch('/api/admin/licenses/bulk'")
content = content.replace('fetch("/api/licenses/generate"', 'fetch("/api/admin/licenses/bulk"')

with open("public/index.html", "w") as f:
    f.write(content)

print("✅ Endpoint-ka generate license waa la hagaajiyay!")
