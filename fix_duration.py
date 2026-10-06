# fix_duration.py - Hagaaji duration-ka

with open("server.js", "r") as f:
    content = f.read()

old_line = "const { count, duration, max_devices } = req.body;"
new_line = "const { count, days, duration, max_devices } = req.body;"

content = content.replace(old_line, new_line)

old_dur = "const dur = duration || '30 days';"
new_dur = "const dur = duration || (days ? days + ' days' : '30 days');"

content = content.replace(old_dur, new_dur)

with open("server.js", "w") as f:
    f.write(content)
print("✅ Duration-ka waa la hagaajiyay!")
