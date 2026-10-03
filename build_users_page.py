# build_users_page.py - Dhis qaybta Users Management

with open("public/index.html", "r") as f:
    content = f.read()

# Hel loadPage function
old_start = content.find("async function loadPage(pageName")
old_end = content.find("async function fetchStats()")

if old_start != -1 and old_end != -1:
    new_loadpage = '''async function loadPage(pageName, element = null) {
        if (element) {
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
            element.classList.add('active');
        }
        
        const contentArea = document.getElementById('page-content');
        
        if (pageName === 'dashboard') {
            contentArea.innerHTML = `
                <h1 style="margin-bottom: 20px;">Dashboard Overview</h1>
                <div class="stats-grid" id="stats-grid">
                    <div class="stat-card"><span class="title">Loading...</span></div>
                </div>
                <div class="charts-grid">
                    <div class="chart-box">
                        <h3>Analytics Overview</h3>
                        <canvas id="analyticsChart"></canvas>
                    </div>
                    <div class="chart-box">
                        <h3>License Status</h3>
                        <canvas id="licenseChart"></canvas>
                    </div>
                </div>
            `;
            await fetchStats();
        } 
        else if (pageName === 'users') {
            contentArea.innerHTML = `
                <h1 style="margin-bottom: 20px;">Users Management</h1>
                <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                    <div class="search-bar" style="flex: 1; max-width: 400px;">
                        <i class="fa-solid fa-search"></i>
                        <input type="text" id="user-search" placeholder="Search users..." onkeyup="filterUsers()">
                    </div>
                    <button class="submit-btn" style="max-width: 200px;" onclick="showAddUserModal()">
                        <i class="fa-solid fa-plus"></i> Add User
                    </button>
                </div>
                <div class="chart-box" style="overflow-x: auto;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <thead>
                            <tr style="border-bottom: 1px solid #2a2a35;">
                                <th style="padding: 12px; text-align: left;">ID</th>
                                <th style="padding: 12px; text-align: left;">Username</th>
                                <th style="padding: 12px; text-align: left;">Full Name</th>
                                <th style="padding: 12px; text-align: left;">Role</th>
                                <th style="padding: 12px; text-align: left;">License</th>
                                <th style="padding: 12px; text-align: left;">Actions</th>
                            </tr>
                        </thead>
                        <tbody id="users-tbody">
                            <tr><td colspan="6" style="padding: 20px; text-align: center;">Loading...</td></tr>
                        </tbody>
                    </table>
                </div>
            `;
            await loadUsers();
        }
        else if (pageName === 'licenses') {
            contentArea.innerHTML = `
                <h1 style="margin-bottom: 20px;">Licenses Management</h1>
                <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                    <button class="submit-btn" style="max-width: 250px;" onclick="showGenerateLicenseModal()">
                        <i class="fa-solid fa-plus"></i> Generate License
                    </button>
                </div>
                <div class="chart-box" style="overflow-x: auto;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <thead>
                            <tr style="border-bottom: 1px solid #2a2a35;">
                                <th style="padding: 12px; text-align: left;">License Key</th>
                                <th style="padding: 12px; text-align: left;">User ID</th>
                                <th style="padding: 12px; text-align: left;">Duration</th>
                                <th style="padding: 12px; text-align: left;">Status</th>
                                <th style="padding: 12px; text-align: left;">Actions</th>
                            </tr>
                        </thead>
                        <tbody id="licenses-tbody">
                            <tr><td colspan="5" style="padding: 20px; text-align: center;">Loading...</td></tr>
                        </tbody>
                    </table>
                </div>
            `;
            await loadLicenses();
        }
        else if (pageName === 'referrals') {
            contentArea.innerHTML = `
                <h1 style="margin-bottom: 20px;">Referrals</h1>
                <div class="chart-box">
                    <p style="color: #8b8b9e;">Referral system wali lama dhisin.</p>
                </div>
            `;
        }
        else if (pageName === 'settings') {
            contentArea.innerHTML = `
                <h1 style="margin-bottom: 20px;">Settings</h1>
                <div class="chart-box">
                    <h3>Profile</h3>
                    <p style="color: #8b8b9e; margin-top: 10px;">Username: <strong>${JSON.parse(localStorage.getItem('user') || '{}').username || 'N/A'}</strong></p>
                    <p style="color: #8b8b9e;">Role: <strong>${JSON.parse(localStorage.getItem('user') || '{}').role || 'N/A'}</strong></p>
                </div>
            `;
        }
    }
    
    '''
    new_content = content[:old_start] + new_loadpage + content[old_end:]
    
    with open("public/index.html", "w") as f:
        f.write(new_content)
    print("✅ loadPage function waa la cusboonaysiiyay!")
else:
    print("❌ Ma helin loadPage function")
