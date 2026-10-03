# complete_dashboard.py - Buuxi meelaha banaan

with open("public/index.html", "r") as f:
    content = f.read()

# Beddel qaybta dashboard-ka marka loadPage('dashboard') la riixo
old_dashboard_start = content.find("if(p==='dashboard'){")
old_dashboard_end = content.find("else if(p==='users')")

if old_dashboard_start != -1 and old_dashboard_end != -1:
    new_dashboard = '''if(p==='dashboard'){
        c.innerHTML='<div class="hero"><div class="hero-badge">Welcome Back</div><h1>Hello, <span>'+(u.username||'User')+'</span></h1><p>You are in control. Here is what is happening with your panel today.</p><div class="hero-buttons"><button class="btn-primary" onclick="loadPage(\\'licenses\\')"><i class="fa-solid fa-plus"></i> Generate License</button><button class="btn-secondary" onclick="loadPage(\\'users\\')"><i class="fa-solid fa-users"></i> Manage Users</button></div></div>'+
        '<div class="stats-grid" id="stats-grid"><div class="stat-card">Loading...</div></div>'+
        '<div class="content-grid">'+
            '<div class="panel"><div class="panel-header"><h3>Analytics Overview</h3></div><canvas id="analyticsChart" height="200"></canvas></div>'+
            '<div class="panel"><div class="panel-header"><h3>License Status</h3></div><canvas id="licenseChart" height="200"></canvas></div>'+
        '</div>'+
        '<div class="content-grid" style="margin-top:20px;">'+
            '<div class="panel"><div class="panel-header"><h3>Recent Activity</h3><a href="#">View All</a></div><div id="activity-list"><p style="color:var(--muted);text-align:center;padding:20px;">Loading...</p></div></div>'+
            '<div class="panel"><div class="panel-header"><h3>Quick Actions</h3></div>'+
                '<div class="quick-action" onclick="loadPage(\\'licenses\\')"><i class="fa-solid fa-key"></i><span>Generate License</span></div>'+
                '<div class="quick-action" onclick="loadPage(\\'users\\')"><i class="fa-solid fa-user-plus"></i><span>Add User</span></div>'+
                '<div class="quick-action" onclick="loadPage(\\'referrals\\')"><i class="fa-solid fa-share-nodes"></i><span>View Referrals</span></div>'+
                '<div class="quick-action" onclick="loadPage(\\'settings\\')"><i class="fa-solid fa-gear"></i><span>System Settings</span></div>'+
            '</div>'+
        '</div>';
        await fetchStats();
        loadActivity();
    }
    '''
    content = content[:old_dashboard_start] + new_dashboard + content[old_dashboard_end:]
    print("✅ Dashboard-ka waa la buuxiyay!")
else:
    print("❌ Ma helin dashboard section")

# Ku dar loadActivity function
activity_func = '''
async function loadActivity() {
    var list = document.getElementById('activity-list');
    if (!list) return;
    try {
        var token = localStorage.getItem('token');
        var res = await fetch('/api/stats', { headers: { 'Authorization': 'Bearer ' + token } });
        var data = await res.json();
        
        var activities = [
            { icon: 'fa-user-plus', color: 'blue', text: 'New user registered', time: '2 minutes ago', badge: 'Success' },
            { icon: 'fa-key', color: 'purple', text: 'License generated', time: '15 minutes ago', badge: 'Success' },
            { icon: 'fa-share-nodes', color: 'green', text: 'New referral', time: '1 hour ago', badge: 'New' },
            { icon: 'fa-gear', color: 'yellow', text: 'System updated', time: '3 hours ago', badge: 'Info' }
        ];
        
        list.innerHTML = activities.map(function(a) {
            return '<div class="activity-item">' +
                '<div class="activity-icon stat-icon ' + a.color + '" style="margin-bottom:0;width:36px;height:36px;font-size:14px;"><i class="fa-solid ' + a.icon + '"></i></div>' +
                '<div class="activity-info" style="flex:1;"><div>' + a.text + '</div><div style="font-size:12px;color:var(--muted);">' + a.time + '</div></div>' +
                '<span class="activity-badge" style="background:rgba(16,185,129,.2);color:#10b981;">' + a.badge + '</span>' +
            '</div>';
        }).join('');
    } catch(e) {
        list.innerHTML = '<p style="color:var(--muted);text-align:center;padding:20px;">No activity</p>';
    }
}
'''
content = content.replace('function handleLogout()', activity_func + '\nfunction handleLogout()')

# Ku dar License Chart render
old_render = '''function renderChart(d){var c=document.getElementById('analyticsChart');if(!c)return;if(window.myChart)window.myChart.destroy();window.myChart=new Chart(c.getContext('2d'),{type:'line',data:{labels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],datasets:[{label:'Activity',data:[2,4,3,6,5,8,d.totalUsers||1],borderColor:'#00d4ff',backgroundColor:'rgba(0,212,255,.1)',tension:.4,fill:true,borderWidth:2}]},options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,grid:{color:'#1e1e2a'},ticks:{color:'#6b6b7e'}},x:{grid:{display:false},ticks:{color:'#6b6b7e'}}}}});}'''

new_render = '''function renderChart(d){
    var c=document.getElementById('analyticsChart');
    if(c){
        if(window.myChart)window.myChart.destroy();
        window.myChart=new Chart(c.getContext('2d'),{
            type:'line',
            data:{labels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],datasets:[{label:'Activity',data:[2,4,3,6,5,8,d.totalUsers||1],borderColor:'#00d4ff',backgroundColor:'rgba(0,212,255,.1)',tension:.4,fill:true,borderWidth:2}]},
            options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,grid:{color:'#1e1e2a'},ticks:{color:'#6b6b7e'}},x:{grid:{display:false},ticks:{color:'#6b6b7e'}}}}
        });
    }
    var c2=document.getElementById('licenseChart');
    if(c2){
        if(window.licenseChart)window.licenseChart.destroy();
        window.licenseChart=new Chart(c2.getContext('2d'),{
            type:'doughnut',
            data:{labels:['Available','Used'],datasets:[{data:[d.unusedLicenses||0,d.usedLicenses||0],backgroundColor:['#10b981','#f59e0b'],borderWidth:0}]},
            options:{responsive:true,plugins:{legend:{position:'bottom',labels:{color:'#6b6b7e',padding:15}}},cutout:'70%'}
        });
    }
}'''

content = content.replace(old_render, new_render)

with open("public/index.html", "w") as f:
    f.write(content)

print("✅ Dashboard-ka oo dhamaystiran waa la abuuray!")
