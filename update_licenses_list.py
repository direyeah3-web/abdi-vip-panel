# update_licenses_list.py - Cusboonaysii loadLicenses si uu u muujiyo Copy button

with open("public/index.html", "r") as f:
    content = f.read()

# Hel loadLicenses function
old_start = content.find("async function loadLicenses()")
old_end = content.find("async function deleteLicense(id)")

if old_start != -1 and old_end != -1:
    new_loadlicenses = '''async function loadLicenses() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/licenses', {
                headers: { 'Authorization': 'Bearer ' + token }
            });
            const licenses = await response.json();
            const tbody = document.getElementById('licenses-tbody');
            if (!tbody) return;
            
            if (!Array.isArray(licenses) || licenses.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" style="padding: 20px; text-align: center;">Ma jiro license</td></tr>';
                return;
            }
            
            tbody.innerHTML = licenses.map(function(l) {
                var statusColor = l.status === 'unused' ? '#10b981' : (l.status === 'used' ? '#f59e0b' : '#ef4444');
                return '<tr style="border-bottom: 1px solid #2a2a35;">' +
                    '<td style="padding: 12px;"><code style="background: #1e1e28; padding: 4px 8px; border-radius: 4px; font-size: 12px;">' + l.license_key + '</code></td>' +
                    '<td style="padding: 12px;">' + (l.user_id || '-') + '</td>' +
                    '<td style="padding: 12px;">' + (l.duration || '-') + '</td>' +
                    '<td style="padding: 12px;"><span style="padding: 4px 10px; border-radius: 20px; background: ' + statusColor + '20; color: ' + statusColor + '; font-size: 12px; font-weight: 600;">' + l.status + '</span></td>' +
                    '<td style="padding: 12px;">' +
                        '<button onclick="copyLicense(\\'' + l.license_key + '\\')" style="background: #8b5cf6; border: none; color: white; padding: 6px 10px; border-radius: 6px; cursor: pointer; margin-right: 5px;" title="Copy">' +
                            '<i class="fa-solid fa-copy"></i>' +
                        '</button>' +
                        '<button onclick="deleteLicense(' + l.id + ')" style="background: #ef4444; border: none; color: white; padding: 6px 10px; border-radius: 6px; cursor: pointer;" title="Delete">' +
                            '<i class="fa-solid fa-trash"></i>' +
                        '</button>' +
                    '</td>' +
                    '</tr>';
            }).join('');
        } catch (error) {
            console.error('Error loading licenses:', error);
        }
    }
    
    '''
    new_content = content[:old_start] + new_loadlicenses + content[old_end:]
    
    with open("public/index.html", "w") as f:
        f.write(new_content)
    print("✅ loadLicenses function waa la cusboonaysiiyay!")
else:
    print("❌ Ma helin loadLicenses function")
