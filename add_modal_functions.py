# add_modal_functions.py - Ku dar functions-ka modal-ka

with open("public/index.html", "r") as f:
    content = f.read()

if "function showGenerateLicenseModal()" in content and "closeLicenseModal" in content:
    print("⚠️ Functions-ka horey ayay u jiraan!")
else:
    js_code = """
    // ===== LICENSE MODAL FUNCTIONS =====
    let selectedDays = 1;
    
    function showGenerateLicenseModal() {
        document.getElementById('license-modal').style.display = 'flex';
        document.getElementById('license-quantity').value = 1;
        document.getElementById('custom-days').style.display = 'none';
        selectedDays = 1;
        document.querySelectorAll('.duration-btn').forEach(function(b) {
            b.classList.remove('active');
            if (b.dataset.days === '1') b.classList.add('active');
        });
    }
    
    function closeLicenseModal() {
        document.getElementById('license-modal').style.display = 'none';
    }
    
    function selectDuration(btn, days) {
        document.querySelectorAll('.duration-btn').forEach(function(b) { b.classList.remove('active'); });
        btn.classList.add('active');
        selectedDays = days;
        const customInput = document.getElementById('custom-days');
        if (days === 'custom') {
            customInput.style.display = 'block';
            customInput.focus();
        } else {
            customInput.style.display = 'none';
        }
    }
    
    async function generateLicenses() {
        let days = selectedDays;
        if (days === 'custom') {
            days = parseInt(document.getElementById('custom-days').value);
            if (!days || days < 1) {
                alert('Fadlan geli tirada maalmood ee saxda ah');
                return;
            }
        }
        
        const quantity = parseInt(document.getElementById('license-quantity').value) || 1;
        
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/licenses/bulk', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                },
                body: JSON.stringify({ days: days, quantity: quantity })
            });
            
            const data = await response.json();
            
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
            // Fallback
            const input = document.createElement('input');
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
        # Ka saar showGenerateLicenseModal hore haddii uu jiro
        old_modal = content.find("function showGenerateLicenseModal()")
        if old_modal != -1:
            # Hel meesha uu ku dhammaado
            end_modal = content.find("function showAddUserModal", old_modal)
            if end_modal != -1:
                content = content[:old_modal] + content[end_modal:]
                print("✅ showGenerateLicenseModal hore waa la saaray.")
                # Dib u raadi target
                pos = content.find(target)
        
        new_content = content[:pos] + js_code + "\n    " + content[pos:]
        with open("public/index.html", "w") as f:
            f.write(new_content)
        print("✅ Functions-ka modal-ka waa lagu daray!")
    else:
        print("❌ Ma helin handleLogout")
