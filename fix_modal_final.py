# fix_modal_final.py - Ka saar prompt() hore kadibna ku dar function cusub

with open("public/index.html", "r") as f:
    content = f.read()

# ===== TALLAABADA 1: KA SAAR PROMPT() HORE =====
# Hel meesha prompt() ku jiro
prompt_pos = content.find("const duration = prompt('Geli duration-ka license-ka:', '30 days');")

if prompt_pos != -1:
    # Hel meesha function-ka showGenerateLicenseModal ka bilaabmo
    func_start = content.rfind("function showGenerateLicenseModal()", 0, prompt_pos)
    
    if func_start != -1:
        # Hel meesha function-ka ku dhammaado (function xigta)
        func_end = content.find("function showAddUserModal()", func_start)
        if func_end == -1:
            func_end = content.find("function toggleProfileMenu()", func_start)
        if func_end == -1:
            func_end = content.find("function handleLogout()", func_start)
        
        if func_end != -1:
            # Ka saar function-kii hore oo dhan
            content = content[:func_start] + content[func_end:]
            print("✅ Function-kii hore ee prompt() waa la saaray!")
        else:
            print("⚠️ Ma helin meesha function-ku ku dhammaado.")
    else:
        print("⚠️ Ma helin function-ka showGenerateLicenseModal.")
else:
    print("ℹ️ prompt() hore lama helin (waa la saaray horey).")

# ===== TALLAABADA 2: KU DAR FUNCTION CUSUB =====
if "selectDuration" in content and "license-modal" in content:
    print("⚠️ Functions-ka cusub horey ayay u jiraan!")
else:
    js_code = """
    // ===== LICENSE MODAL FUNCTIONS (NEW) =====
    let selectedDays = 1;
    
    function showGenerateLicenseModal() {
        var modal = document.getElementById('license-modal');
        if (!modal) {
            alert('Modal-ka lama helin. Fadlan dib u cusboonaysii bogga.');
            return;
        }
        modal.style.display = 'flex';
        document.getElementById('license-quantity').value = 1;
        document.getElementById('custom-days').style.display = 'none';
        selectedDays = 1;
        var btns = document.querySelectorAll('.duration-btn');
        btns.forEach(function(b) {
            b.classList.remove('active');
            if (b.getAttribute('data-days') === '1') b.classList.add('active');
        });
    }
    
    function closeLicenseModal() {
        var modal = document.getElementById('license-modal');
        if (modal) modal.style.display = 'none';
    }
    
    function selectDuration(btn, days) {
        var btns = document.querySelectorAll('.duration-btn');
        btns.forEach(function(b) { b.classList.remove('active'); });
        btn.classList.add('active');
        selectedDays = days;
        var customInput = document.getElementById('custom-days');
        if (days === 'custom') {
            customInput.style.display = 'block';
            customInput.focus();
        } else {
            customInput.style.display = 'none';
        }
    }
    
    async function generateLicenses() {
        var days = selectedDays;
        if (days === 'custom') {
            days = parseInt(document.getElementById('custom-days').value);
            if (!days || days < 1) {
                alert('Fadlan geli tirada maalmood ee saxda ah');
                return;
            }
        }
        
        var quantity = parseInt(document.getElementById('license-quantity').value) || 1;
        
        try {
            var token = localStorage.getItem('token');
            var response = await fetch('/api/licenses/bulk', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                },
                body: JSON.stringify({ days: days, quantity: quantity })
            });
            
            var data = await response.json();
            
            if (data.success) {
                closeLicenseModal();
                alert(quantity + ' license(s) waa la abuuray!');
                loadLicenses();
            } else {
                alert('Error: ' + (data.error || 'Unknown'));
            }
        } catch (error) {
            alert('Error: ' + error.message);
        }
    }
    
    async function copyLicense(key) {
        try {
            await navigator.clipboard.writeText(key);
            alert('License key waa la copy gareeyay: ' + key);
        } catch (e) {
            var input = document.createElement('input');
            input.value = key;
            document.body.appendChild(input);
            input.select();
            document.execCommand('copy');
            document.body.removeChild(input);
            alert('License key waa la copy gareeyay: ' + key);
        }
    }
    """
    
    # Ku dar ka hor "function handleLogout"
    target = "function handleLogout()"
    pos = content.find(target)
    
    if pos != -1:
        content = content[:pos] + js_code + "\n    " + content[pos:]
        print("✅ Functions-ka cusub waa lagu daray!")
    else:
        print("❌ Ma helin handleLogout")

# Qor faylka
with open("public/index.html", "w") as f:
    f.write(content)

print("✅ Faylka 'public/index.html' waa la cusboonaysiiyay!")
