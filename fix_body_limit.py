import shutil

shutil.copy('server.js', 'server.js.backup_limit')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Beddel line 68
old_json = "app.use(bodyParser.json());"
new_json = "app.use(bodyParser.json({ limit: '100mb' }));"

if old_json in c:
    c = c.replace(old_json, new_json, 1)
    print("1. bodyParser.json limit: OK")
else:
    print("1. bodyParser.json: LAMA HELIN")

# Beddel line 69
old_url = "app.use(bodyParser.urlencoded({ extended: true }));"
new_url = "app.use(bodyParser.urlencoded({ extended: true, limit: '100mb' }));"

if old_url in c:
    c = c.replace(old_url, new_url, 1)
    print("2. bodyParser.urlencoded limit: OK")
else:
    print("2. bodyParser.urlencoded: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_limit")
