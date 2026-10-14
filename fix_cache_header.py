import shutil

shutil.copy('server.js', 'server.js.backup6')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Ku dar no-cache header index.html
old = "app.use(express.static('public'));"
new = """app.use(express.static('public', {
    setHeaders: (res, path) => {
        if (path.endsWith('index.html')) {
            res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
            res.setHeader('Pragma', 'no-cache');
            res.setHeader('Expires', '0');
        }
    }
}));"""

if old in c:
    c = c.replace(old, new, 1)
    print("1. Cache-Control: OK")
else:
    print("1. Cache-Control: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup6")
