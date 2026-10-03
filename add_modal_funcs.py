# add_modal_funcs.py - Ku dar function-ka cusub ee Modal-ka

with open("public/index.html", "r") as f:
    content = f.read()

# Hubi haddii function-ka cusub uu jiro
if "function selectDuration(" in content:
    print("⚠️ Function-ka cusub horey ayuu u jiray!")
else:
    js_code = """
    // ===== LICENSE MODAL FUNCTIONS =====
    var selectedDays = 1;
    
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

# Qor
with open("public/index.html", "w") as f:
    f.write(content)

print("✅ Faylka waa la keydiyay!")

