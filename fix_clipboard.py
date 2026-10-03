# fix_clipboard.py - Xall dhibaatada clipboard

with open("loader/index.html", "r") as f:
    content = f.read()

# Beddel pasteKey function
old_paste = '''async function pasteKey() {
    try {
        var text = await navigator.clipboard.readText();
        document.getElementById('license-key').value = text;
    } catch(e) {
        alert('Paste manually');
    }
}'''

new_paste = '''async function pasteKey() {
    try {
        if (navigator.clipboard && navigator.clipboard.readText) {
            var text = await navigator.clipboard.readText();
            document.getElementById('license-key').value = text;
            showToast('License key waa la dhejiyay!');
        } else {
            showToast('Fadlan gacanta ku qor license key-ga');
        }
    } catch(e) {
        showToast('Fadlan gacanta ku qor license key-ga');
    }
}'''

content = content.replace(old_paste, new_paste)

with open("loader/index.html", "w") as f:
    f.write(content)

print("✅ Dhibaatada clipboard waa la xalliyay!")
