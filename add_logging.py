# add_logging.py - Ku dar logging /connect

with open("server.js", "r") as f:
    content = f.read()

old_connect = "app.post('/connect', (req, res) => {\n    try {"
new_connect = """app.post('/connect', (req, res) => {
    console.log('=== /connect REQUEST ===');
    console.log('Body:', JSON.stringify(req.body));
    console.log('Headers:', JSON.stringify(req.headers));
    console.log('Query:', JSON.stringify(req.query));
    try {"""

content = content.replace(old_connect, new_connect)

with open("server.js", "w") as f:
    f.write(content)
print("✅ Logging waa lagu daray!")
