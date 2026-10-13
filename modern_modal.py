# modern_modal.py - Modern Generate License Modal
import shutil

# Backup
shutil.copy("public/index.html", "public/index.html.backup3")
print("✅ Backup waa la sameeyay!")

with open("public/index.html", "r") as f:
    content = f.read()

# ===== 1. KU DAR CSS CUSUB =====
modern_css = """
/* ===== MODERN MODAL STYLES ===== */
@keyframes modalSlideUp { from{opacity:0;transform:translateY(50px) scale(0.95)} to{opacity:1;transform:translateY(0) scale(1)} }
@keyframes modalFadeIn { from{opacity:0} to{opacity:1} }
@keyframes gradientShift { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }

.modern-modal-overlay {
    display: none;
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(0,0,0,0.85);
    backdrop-filter: blur(10px);
    z-index: 9999;
    justify-content: center;
    align-items: center;
    animation: modalFadeIn 0.3s ease;
}
.modern-modal-overlay.active { display: flex; }

.modern-modal {
    background: linear-gradient(135deg, var(--card-bg) 0%, #1a1a2e 100%);
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 24px;
    padding: 35px;
    width: 90%;
    max-width: 480px;
    box-shadow: 0 30px 80px rgba(139,92,246,0.3), 0 0 0 1px rgba(139,92,246,0.1) inset;
    animation: modalSlideUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    position: relative;
    overflow: hidden;
}
.modern-modal::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(139,92,246,0.15) 0%, transparent 60%);
    animation: gradientShift 8s ease infinite;
    pointer-events: none;
}
.modern-modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
    position: relative;
    z-index: 1;
}
.modern-modal-title {
    font-size: 24px;
    font-weight: 800;
    background: linear-gradient(135deg, #fff, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: flex;
    align-items: center;
    gap: 12px;
}
.modern-modal-title i {
    -webkit-text-fill-color: #8b5cf6;
    font-size: 22px;
}
.modern-modal-close {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.3);
    color: #ef4444;
    width: 36px; height: 36px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 16px;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
}
.modern-modal-close:hover {
    background: #ef4444;
    color: white;
    transform: rotate(90deg);
}
.modern-label {
    display: block;
    margin-bottom: 10px;
    font-size: 13px;
    font-weight: 700;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    position: relative;
    z-index: 1;
}
.modern-duration-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 24px;
    position: relative;
    z-index: 1;
}
.modern-duration-btn {
    padding: 14px 8px;
    background: rgba(139,92,246,0.05);
    border: 1px solid var(--border);
    border-radius: 12px;
    color: var(--muted);
    cursor: pointer;
    font-size: 13px;
    font-weight: 600;
    transition: all 0.3s;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
}
.modern-duration-btn i { font-size: 16px; }
.modern-duration-btn:hover {
    background: rgba(139,92,246,0.15);
    border-color: rgba(139,92,246,0.5);
    color: var(--text);
    transform: translateY(-3px);
}
.modern-duration-btn.active {
    background: linear-gradient(135deg, #00d4ff, #8b5cf6);
    color: white;
    border-color: transparent;
    box-shadow: 0 10px 30px rgba(139,92,246,0.4);
}
.modern-quantity-input {
    width: 100%;
    padding: 16px 20px;
    background: rgba(0,0,0,0.3);
    border: 2px solid var(--border);
    border-radius: 14px;
    color: var(--text);
    font-size: 16px;
    font-weight: 600;
    outline: none;
    margin-bottom: 24px;
    transition: all 0.3s;
    position: relative;
    z-index: 1;
    box-sizing: border-box;
}
.modern-quantity-input:focus {
    border-color: #8b5cf6;
    box-shadow: 0 0 0 4px rgba(139,92,246,0.15);
}
.modern-generate-btn {
    width: 100%;
    padding: 18px;
    background: linear-gradient(135deg, #00d4ff, #8b5cf6);
    border: none;
    border-radius: 14px;
    color: white;
    font-size: 16px;
    font-weight: 800;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    transition: all 0.3s;
    position: relative;
    z-index: 1;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.modern-generate-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 20px 50px rgba(139,92,246,0.5);
}
.modern-generate-btn:active { transform: translateY(0); }
"""

if "</style>" in content:
    content = content.replace("</style>", modern_css + "\n</style>", 1)
    print("✅ Modern Modal CSS waa lagu daray!")

# ===== 2. KU DAR MODAL CUSUB (ka hor </body>) =====
modern_modal_html = '''
<!-- MODERN GENERATE LICENSE MODAL -->
<div id="modern-license-modal" class="modern-modal-overlay">
    <div class="modern-modal">
        <div class="modern-modal-header">
            <h2 class="modern-modal-title"><i class="fa-solid fa-key"></i> Generate License</h2>
            <button class="modern-modal-close" onclick="closeModernModal()">
                <i class="fa-solid fa-xmark"></i>
            </button>
        </div>
        
        <label class="modern-label">Duration</label>
        <div class="modern-duration-grid">
            <button type="button" class="modern-duration-btn active" data-days="1" onclick="selectModernDuration(this, 1)">
                <i class="fa-solid fa-calendar-day"></i>1 Day
            </button>
            <button type="button" class="modern-duration-btn" data-days="7" onclick="selectModernDuration(this, 7)">
                <i class="fa-solid fa-calendar-week"></i>7 Days
            </button>
            <button type="button" class="modern-duration-btn" data-days="30" onclick="selectModernDuration(this, 30)">
                <i class="fa-solid fa-calendar"></i>30 Days
            </button>
            <button type="button" class="modern-duration-btn" data-days="90" onclick="selectModernDuration(this, 90)">
                <i class="fa-solid fa-calendar-plus"></i>90 Days
            </button>
            <button type="button" class="modern-duration-btn" data-days="365" onclick="selectModernDuration(this, 365)">
                <i class="fa-solid fa-calendar-check"></i>1 Year
            </button>
            <button type="button" class="modern-duration-btn" data-days="custom" onclick="selectModernDuration(this, 'custom')">
                <i class="fa-solid fa-sliders"></i>Custom
            </button>
        </div>
        
        <input type="number" id="modern-custom-days" class="modern-quantity-input" placeholder="Enter custom days" style="display:none;">
        
        <label class="modern-label">Quantity</label>
        <input type="number" id="modern-quantity" class="modern-quantity-input" value="1" min="1" max="100">
        
        <button class="modern-generate-btn" onclick="generateModernLicenses()">
            <i class="fa-solid fa-bolt"></i> Generate Now
        </button>
    </div>
</div>
'''

if "</body>" in content:
    content = content.replace("</body>", modern_modal_html + "\n</body>", 1)
    print("✅ Modern Modal HTML waa lagu daray!")

# ===== 3. KU DAR JAVASCRIPT =====
modern_js = """
    // ===== MODERN MODAL FUNCTIONS =====
    var modernSelectedDays = 1;
    
    function showModernLicenseModal() {
        document.getElementById('modern-license-modal').classList.add('active');
        document.getElementById('modern-quantity').value = 1;
        document.getElementById('modern-custom-days').style.display = 'none';
        modernSelectedDays = 1;
        document.querySelectorAll('.modern-duration-btn').forEach(function(b) {
            b.classList.remove('active');
            if (b.getAttribute('data-days') === '1') b.classList.add('active');
        });
    }
    
    function closeModernModal() {
        document.getElementById('modern-license-modal').classList.remove('active');
    }
    
    function selectModernDuration(btn, days) {
        document.querySelectorAll('.modern-duration-btn').forEach(function(b) { b.classList.remove('active'); });
        btn.classList.add('active');
        modernSelectedDays = days;
        var customInput = document.getElementById('modern-custom-days');
        if (days === 'custom') {
            customInput.style.display = 'block';
            customInput.focus();
        } else {
            customInput.style.display = 'none';
        }
    }
    
    async function generateModernLicenses() {
        var days = modernSelectedDays;
        if (days === 'custom') {
            days = parseInt(document.getElementById('modern-custom-days').value);
            if (!days || days < 1) { alert('Fadlan geli tirada maalmood ee saxda ah'); return; }
        }
        var qty = parseInt(document.getElementById('modern-quantity').value) || 1;
        try {
            var token = localStorage.getItem('token');
            var res = await fetch('/api/admin/licenses/bulk', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
                body: JSON.stringify({ days: days, quantity: qty })
            });
            var data = await res.json();
            if (data.ok || data.success) {
                closeModernModal();
                alert(qty + ' license(s) waa la abuuray!');
                loadLicenses();
                if (typeof fetchStats === 'function') fetchStats();
            } else {
                alert('Error: ' + (data.error || 'Unknown'));
            }
        } catch(e) { alert('Error: ' + e.message); }
    }
"""

if "function handleLogout()" in content:
    content = content.replace("function handleLogout()", modern_js + "\n    function handleLogout()", 1)
    print("✅ Modern Modal JS waa lagu daray!")

# ===== 4. BEDDEL BOTTON-KA "Generate License" =====
content = content.replace('onclick="showGenerateLicenseModal()"', 'onclick="showModernLicenseModal()"')
print("✅ Botton-ka Generate License waa la beddelay!")

with open("public/index.html", "w") as f:
    f.write(content)
print("✅ Faylka waa la keydiyay!")
print("🔥 MODERN MODAL waa dhammaatay!")
