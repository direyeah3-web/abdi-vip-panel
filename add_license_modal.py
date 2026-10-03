# add_license_modal.py - Ku dar modal casri ah oo lagu abuuro license

with open("public/index.html", "r") as f:
    content = f.read()

# Hubi haddii modal-ku horey u jiro
if 'id="license-modal"' in content:
    print("⚠️ Modal-ka horey ayuu u jiray!")
else:
    # Modal-ka HTML
    modal_html = '''
<!-- LICENSE MODAL -->
<div id="license-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 9999; justify-content: center; align-items: center;">
    <div style="background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 20px; padding: 30px; width: 90%; max-width: 500px; box-shadow: 0 20px 60px rgba(0,0,0,0.5);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
            <h2 style="font-size: 22px; font-weight: 700;">Generate License</h2>
            <button onclick="closeLicenseModal()" style="background: transparent; border: none; color: var(--text-muted); font-size: 24px; cursor: pointer;">
                <i class="fa-solid fa-xmark"></i>
            </button>
        </div>
        
        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 10px; font-size: 14px; font-weight: 500;">Duration</label>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px;">
                <button type="button" class="duration-btn active" data-days="1" onclick="selectDuration(this, 1)">1 Day</button>
                <button type="button" class="duration-btn" data-days="7" onclick="selectDuration(this, 7)">7 Days</button>
                <button type="button" class="duration-btn" data-days="30" onclick="selectDuration(this, 30)">30 Days</button>
                <button type="button" class="duration-btn" data-days="90" onclick="selectDuration(this, 90)">90 Days</button>
                <button type="button" class="duration-btn" data-days="365" onclick="selectDuration(this, 365)">1 Year</button>
                <button type="button" class="duration-btn" data-days="custom" onclick="selectDuration(this, 'custom')">Custom</button>
            </div>
            <input type="number" id="custom-days" placeholder="Geli tirada maalmood" style="display: none; width: 100%; padding: 12px; margin-top: 10px; background: var(--input-bg); border: 1px solid var(--border-color); border-radius: 10px; color: var(--text-color); outline: none;">
        </div>
        
        <div style="margin-bottom: 25px;">
            <label style="display: block; margin-bottom: 10px; font-size: 14px; font-weight: 500;">Quantity</label>
            <input type="number" id="license-quantity" value="1" min="1" max="100" style="width: 100%; padding: 12px; background: var(--input-bg); border: 1px solid var(--border-color); border-radius: 10px; color: var(--text-color); outline: none;">
        </div>
        
        <button onclick="generateLicenses()" class="submit-btn" style="width: 100%;">
            <i class="fa-solid fa-plus"></i> Generate
        </button>
    </div>
</div>

<style>
.duration-btn {
    padding: 10px;
    background: var(--input-bg);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    color: var(--text-muted);
    cursor: pointer;
    font-size: 13px;
    font-weight: 600;
    transition: 0.2s;
}
.duration-btn:hover {
    background: rgba(139, 92, 246, 0.1);
    color: var(--primary-color);
}
.duration-btn.active {
    background: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
}
</style>
'''
    
    # Ku dar ka hor </body>
    body_pos = content.find("</body>")
    if body_pos != -1:
        new_content = content[:body_pos] + modal_html + "\n" + content[body_pos:]
        with open("public/index.html", "w") as f:
            f.write(new_content)
        print("✅ Modal-ka license waa lagu daray!")
    else:
        print("❌ Ma helin </body>")
