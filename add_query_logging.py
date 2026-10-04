# add_query_logging.py - Ku dar logging query-ga

with open("server.js", "r") as f:
    content = f.read()

old = "const lic = queryOne('SELECT * FROM licenses WHERE license_key = ?', [licKey]);"
new = """console.log('>>> QUERY licKey:', licKey);
        const lic = queryOne('SELECT * FROM licenses WHERE license_key = ?', [licKey]);
        console.log('>>> QUERY RESULT:', JSON.stringify(lic));"""

content = content.replace(old, new, 1)

with open("server.js", "w") as f:
    f.write(content)
print("✅ Logging query waa lagu daray!")

