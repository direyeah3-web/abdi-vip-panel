# modern_toast.py - Ku dar Toast casri ah

with open("public/index.html", "r") as f:
    content = f.read()

# ===== 1. KU DAR CSS TOAST =====
toast_css = """
/* ===== TOAST STYLES ===== */
@keyframes toastSlideIn { from{opacity:0;transform:translateX(400px)} to{opacity:1;transform:translateX(0)} }
@keyframes toastSlideOut { from{opacity:1;transform:translateX(0)} to{opacity:0;transform:translateX(400px)} }
@keyframes toastProgress { from{width:100%} to{width:0%} }

.toast-container { position:fixed;top:20px;right:20px;z-index:99999;display:flex;flex-direction:column;gap:10px; }
.toast { display:flex;align-items:center;gap:14px;padding:16px 20px;background:linear-gradient(135deg,#1a1a2e,#16213e);border:1px solid rgba(139,92,246,0.3);border-radius:14px;box-shadow:0 20px 50px rgba(0,0,0,0.5);min-width:300px;max-width:400px;animation:toastSlideIn 0.4s cubic-bezier(0.34,1.56,0.64,1);position:relative;overflow:hidden; }
.toast.removing { animation:toastSlideOut 0.3s ease-out forwards; }
.toast-icon { width:40px;height:40px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0; }
.toast-icon.success { background:rgba(16,185,129,0.2);color:#10b981; }
.toast-icon.error { background:rgba(239,68,68,0.2);color:#ef4444; }
.toast-icon.info { background:rgba(0,212,255,0.2);color:#00d4ff; }
.toast-content { flex:1; }
.toast-title { font-size:14px;font-weight:700;color:#fff;margin-bottom:2px; }
.toast-message { font-size:13px;color:#8b8b9e; }
.toast-close { background:transparent;border:none;color:#8b8b9e;font-size:16px;cursor:pointer;padding:5px;transition:all 0.2s; }
.toast-close:hover { color:#ef4444; }
.toast-progress { position:absolute;bottom:0;left:0;height:3px;background:linear-gradient(90deg,#00d4ff,#8b5cf6);animation:toastProgress 3s linear forwards; }
"""

if "</style>" in content:
    content = content.replace("</style>", toast_css + "\n</style>", 1)
    print("✅ Toast CSS waa lagu daray!")

# ===== 2. KU DAR TOAST CONTAINER (ka hor </body>) =====
toast_html = '<div id="toast-container" class="toast-container"></div>\n'
if "</body>" in content:
    content = content.replace("</body>", toast_html + "</body>", 1)
    print("✅ Toast Container waa lagu daray!")

# ===== 3. KU DAR TOAST FUNCTION =====
toast_js = """
    // ===== MODERN TOAST =====
    function showToast(title, message, type) {
        type = type || 'success';
        var container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        var icons = { success: 'fa-check-circle', error: 'fa-times-circle', info: 'fa-info-circle' };
        var toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerHTML = '<div class="toast-icon ' + type + '"><i class="fa-solid ' + (icons[type] || icons.success) + '"></i></div>' +
            '<div class="toast-content"><div class="toast-title">' + title + '</div><div class="toast-message">' + message + '</div></div>' +
            '<button class="toast-close" onclick="this.parentElement.remove()"><i class="fa-solid fa-xmark"></i></button>' +
            '<div class="toast-progress"></div>';
        container.appendChild(toast);
        setTimeout(function() {
            toast.classList.add('removing');
            setTimeout(function() { toast.remove(); }, 300);
        }, 3000);
    }
"""

if "function handleLogout()" in content:
    content = content.replace("function handleLogout()", toast_js + "\n    function handleLogout()", 1)
    print("✅ Toast Function waa lagu daray!")

# ===== 4. BEDDEL DHAMMAAN ALERT() =====
replacements = [
    ("alert(q+' licenses created!');", "showToast('Success!', q+' license(s) waa la abuuray!', 'success');"),
    ("alert(q + ' licenses created!');", "showToast('Success!', q+' license(s) waa la abuuray!', 'success');"),
    ("alert('User cusub waa la abuuray!');", "showToast('Success!', 'User cusub waa la abuuray!', 'success');"),
    ("alert('Role-ka waa la beddelay!');", "showToast('Success!', 'Role-ka waa la beddelay!', 'success');"),
    ("alert('Login failed: '+(d.message||d.error||'Invalid'));", "showToast('Login Failed', d.message||d.error||'Invalid credentials', 'error');"),
    ("alert('Error: ' + (data.error || 'Unknown'));", "showToast('Error', data.error || 'Unknown error', 'error');"),
    ("alert('Error: ' + e.message);", "showToast('Error', e.message, 'error');"),
    ("alert('Error changing role');", "showToast('Error', 'Role-ka lama beddeli karin', 'error');"),
    ("alert('Error deleting user');", "showToast('Error', 'User-ka lama tirtiri karin', 'error');"),
    ("alert('Error deleting license');", "showToast('Error', 'License-ka lama tirtiri karin', 'error');"),
    ("alert('Fadlan geli username iyo password');", "showToast('Warning', 'Fadlan geli username iyo password', 'info');"),
    ("alert('Fadlan geli tirada maalmood ee saxda ah');", "showToast('Warning', 'Fadlan geli tirada maalmood ee saxda ah', 'info');"),
]

count = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        count += 1

print("✅ " + str(count) + " alert() waa la beddelay Toast!")

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
print("🔥 MODERN TOAST waa dhammaatay!")
