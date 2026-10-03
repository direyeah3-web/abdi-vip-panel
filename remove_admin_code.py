# remove_admin_code.py - Ka saar koodhka auto-create admin ee qaldan

with open("server.js", "r") as f:
    content = f.read()

# Calaamadda koodhka aan rabno inaan ka saarno
start_marker = "// ===== AUTO CREATE ADMIN USER ====="
end_marker = "app.listen(PORT"

if start_marker in content:
    # Hel meesha koodhku ka bilaabmo iyo meesha uu ku dhammaado
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)
    
    if end_idx != -1:
        # Ka saar koodhka
        new_content = content[:start_idx] + content[end_idx:]
        
        with open("server.js", "w") as f:
            f.write(new_content)
        print("✅ Koodhka auto-create admin waa laga saaray server.js!")
    else:
        print("❌ Ma helin meesha koodhku ku dhammaado")
else:
    print("⚠️ Koodhka auto-create admin lama helin server.js")
