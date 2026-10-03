# fix_dashboard_stats.py - Cusboonaysii fetchStats function

with open("public/index.html", "r") as f:
    content = f.read()

# Hel fetchStats function hore
old_start = content.find("async function fetchStats()")
old_end = content.find("function renderCharts(data)")

if old_start != -1 and old_end != -1:
    new_fetchstats = '''async function fetchStats() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/stats', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (!response.ok) {
                throw new Error('HTTP ' + response.status);
            }
            
            const data = await response.json();
            console.log('Stats data:', data);
            
            const statsGrid = document.getElementById('stats-grid');
            if (!statsGrid) return;
            
            statsGrid.innerHTML = `
                <div class="stat-card">
                    <span class="title">Total Users</span>
                    <span class="value">${data.totalUsers || 0}</span>
                    <span class="trend"><i class="fa-solid fa-arrow-up"></i> Live</span>
                </div>
                <div class="stat-card">
                    <span class="title">Total Licenses</span>
                    <span class="value">${data.totalLicenses || 0}</span>
                    <span class="trend"><i class="fa-solid fa-arrow-up"></i> Live</span>
                </div>
                <div class="stat-card">
                    <span class="title">Used Licenses</span>
                    <span class="value">${data.usedLicenses || 0}</span>
                    <span class="trend"><i class="fa-solid fa-arrow-up"></i> Live</span>
                </div>
                <div class="stat-card">
                    <span class="title">Referrals</span>
                    <span class="value">${data.totalReferrals || 0}</span>
                    <span class="trend"><i class="fa-solid fa-arrow-up"></i> Live</span>
                </div>
            `;
            
            renderCharts(data);
        } catch (error) {
            console.error('Error fetching stats:', error);
            const statsGrid = document.getElementById('stats-grid');
            if (statsGrid) {
                statsGrid.innerHTML = '<div class="stat-card"><span class="title">Error</span><span class="value">—</span></div>';
            }
        }
    }
    
    '''
    new_content = content[:old_start] + new_fetchstats + content[old_end:]
    
    with open("public/index.html", "w") as f:
        f.write(new_content)
    print("✅ fetchStats function waa la cusboonaysiiyay!")
else:
    print("❌ Ma helin fetchStats function")
