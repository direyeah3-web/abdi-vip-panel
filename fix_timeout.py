import shutil

shutil.copy('server.js', 'server.js.backup_timeout')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

old = "app.use(bodyParser.json({ limit: '10mb' }));"
new = "app.use(bodyParser.json({ limit: '100mb' }));"

if old in c:
    c = c.replace(old, new, 1)
    print("1. bodyParser limit: OK")
else:
    print("1. bodyParser limit: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)
