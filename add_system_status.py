# add_system_status.py - Ku dar System Status page

with open("public/index.html", "r") as f:
    content = f.read()

# ===== 1. KU DAR NAV ITEM =====
old_nav = '''<div class="nav-section">System</div>
<a class="nav-item" onclick="loadPage('settings',this)"><i class="fa-solid fa-gear"></i> <span>Settings</span></a>'''

new_nav = '''<div class="nav-section">System</div>
<a class="nav-item" onclick="loadPage('status',this)"><i class="fa-solid fa-signal"></i> <span>System Status</span></a>
<a class="nav-item" onclick="loadPage('settings',this)"><i class="fa-solid fa-gear"></i> <span>Settings</span></a>'''

content = content.replace(old_nav, new_nav)

# ===== 2. KU DAR PAGE-KA STATUS =====
old_settings = '''else if(p==='settings'){'''

new_status = '''else if(p==='status'){
        c.innerHTML='<div class="panel-header" style="margin-bottom:20px;"><h1 style="font-size:24px;font-weight:800;">System Status</h1><button class="btn-secondary" onclick="loadPage(\\'status\\')"><i class="fa-solid fa-refresh"></i> Refresh</button></div>'+
        '<div class="stats-grid" id="status-grid">'+
            '<div class="stat-card"><div class="stat-icon blue"><i class="fa-solid fa-server"></i></div><div class="stat-value" id="server-status">...</div><div class="stat-label">Railway Server</div></div>'+
            '<div class="stat-card"><div class="stat-icon purple"><i class="fa-solid fa-cloud"></i></div><div class="stat-value" id="worker-status">...</div><div class="stat-label">Cloudflare Worker</div></div>'+
            '<div class="stat-card"><div class="stat-icon green"><i class="fa-solid fa-link"></i></div><div class="stat-value" id="connection-status">...</div><div class="stat-label">Connection</div></div>'+
            '<div class="stat-card"><div class="stat-icon yellow"><i class="fa-solid fa-clock"></i></div><div class="stat-value" id="response-time">...</div><div class="stat-label">Response Time</div></div>'+
        '</div>'+
        '<div class="content-grid" style="margin-top:20px;">'+
            '<div class="panel"><div class="panel-header"><h3>Server Details</h3></div><div id="server-details"><p style="color:var(--muted);text-align:center;padding:20px;">Loading...</p></div></div>'+
            '<div class="panel"><div class="panel-header"><h3>Worker Details</h3></div><div id="worker-details"><p style="color:var(--muted);text-align:center;padding:20px;">Loading...</p></div></div>'+
        '</div>'+
        '<div class="panel" style="margin-top:20px;"><div class="panel-header"><h3>Connection Test</h3></div>'+
            '<p style="color:var(--muted);margin-bottom:15px;">Test the connection between Cloudflare Worker and Railway Server.</p>'+
            '<input type="text" id="worker-url-input" value="https://a.dirxx.workers.dev" placeholder="Enter Worker URL" style="margin-bottom:15px;">'+
            '<button class="btn-primary" onclick="testWorkerConnection()"><i class="fa-solid fa-play"></i> Test Connection</button>'+
            '<div id="test-result" style="margin-top:20px;"></div>'+
        '</div>';
        await loadSystemStatus();
    }
    else if(p==='settings'){'''

content = content.replace(old_settings, new_status)

# ===== 3. KU DAR FUNCTIONS-KA =====
status_funcs = '''
async function loadSystemStatus() {
    try {
        // 1. Hubi Server-ka
        var serverStart = Date.now();
        var serverRes = await fetch('/api/health');
        var serverTime = Date.now() - serverStart;
        var serverData = await serverRes.json();
        
        document.getElementById('server-status').innerHTML = '<span style="color:var(--green);font-size:16px;">●</span> Online';
        document.getElementById('server-status').style.color = 'var(--green)';
        document.getElementById('response-time').textContent = serverTime + 'ms';
        
        // 2. Server Details
        document.getElementById('server-details').innerHTML = 
            '<div style="font-size:13px;line-height:2;">' +
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Status:</span><strong style="color:var(--green);">' + (serverData.status || 'online') + '</strong></div>' +
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Version:</span><strong>' + (serverData.version || 'N/A') + '</strong></div>' +
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Node:</span><strong>' + (serverData.node_version || 'N/A') + '</strong></div>' +
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Environment:</span><strong>' + (serverData.environment || 'N/A') + '</strong></div>' +
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Users:</span><strong>' + (serverData.database?.users || 0) + '</strong></div>' +
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Licenses:</span><strong>' + (serverData.database?.licenses || 0) + '</strong></div>' +
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Uptime:</span><strong>' + Math.floor(serverData.uptime || 0) + 's</strong></div>' +
            '</div>';
        
        // 3. Hubi Worker-ka
        var workerUrl = 'https://a.dirxx.workers.dev';
        var workerStart = Date.now();
        try {
            var workerRes = await fetch('/api/worker-check?worker_url=' + encodeURIComponent(workerUrl));
            var workerData = await workerRes.json();
            var workerTime = Date.now() - workerStart;
            
            if (workerData.reachable) {
                document.getElementById('worker-status').innerHTML = '<span style="color:var(--green);font-size:16px;">●</span> Online';
                document.getElementById('worker-status').style.color = 'var(--green)';
                document.getElementById('connection-status').innerHTML = '<span style="color:var(--green);font-size:16px;">●</span> Connected';
                document.getElementById('connection-status').style.color = 'var(--green)';
                document.getElementById('worker-details').innerHTML = 
                    '<div style="font-size:13px;line-height:2;">' +
                        '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Status:</span><strong style="color:var(--green);">Online</strong></div>' +
                        '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">URL:</span><strong style="font-size:11px;">' + workerUrl + '</strong></div>' +
                        '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">HTTP Status:</span><strong>' + (workerData.http_status || 'N/A') + '</strong></div>' +
                        '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Response:</span><strong>' + (workerData.response_time || workerTime + 'ms') + '</strong></div>' +
                    '</div>';
            } else {
                document.getElementById('worker-status').innerHTML = '<span style="color:var(--red);font-size:16px;">●</span> Offline';
                document.getElementById('worker-status').style.color = 'var(--red)';
                document.getElementById('connection-status').innerHTML = '<span style="color:var(--red);font-size:16px;">●</span> Disconnected';
                document.getElementById('connection-status').style.color = 'var(--red)';
                document.getElementById('worker-details').innerHTML = 
                    '<div style="font-size:13px;line-height:2;">' +
                        '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Status:</span><strong style="color:var(--red);">Offline</strong></div>' +
                        '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">URL:</span><strong style="font-size:11px;">' + workerUrl + '</strong></div>' +
                        '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Error:</span><strong style="color:var(--red);font-size:11px;">' + (workerData.error || 'Unknown') + '</strong></div>' +
                    '</div>';
            }
        } catch (workerError) {
            document.getElementById('worker-status').textContent = 'Error';
            document.getElementById('worker-status').style.color = 'var(--red)';
            document.getElementById('connection-status').textContent = 'Error';
            document.getElementById('connection-status').style.color = 'var(--red)';
        }
    } catch (error) {
        console.error('Status error:', error);
        document.getElementById('server-status').textContent = 'Error';
        document.getElementById('server-status').style.color = 'var(--red)';
    }
}

async function testWorkerConnection() {
    var url = document.getElementById('worker-url-input').value.trim();
    var result = document.getElementById('test-result');
    if (!url) { alert('Enter Worker URL'); return; }
    
    result.innerHTML = '<p style="color:var(--muted);">Testing connection...</p>';
    
    try {
        var start = Date.now();
        var res = await fetch('/api/worker-check?worker_url=' + encodeURIComponent(url));
        var data = await res.json();
        var time = Date.now() - start;
        
        if (data.reachable) {
            result.innerHTML = 
                '<div style="padding:15px;background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.3);border-radius:10px;">' +
                    '<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">' +
                        '<i class="fa-solid fa-check-circle" style="color:var(--green);font-size:20px;"></i>' +
                        '<strong style="color:var(--green);">Connection Successful!</strong>' +
                    '</div>' +
                    '<div style="font-size:13px;color:var(--muted);">' +
                        '<div>Worker: <strong style="color:var(--text);">' + url + '</strong></div>' +
                        '<div>Response Time: <strong style="color:var(--text);">' + (data.response_time || time + 'ms') + '</strong></div>' +
                        '<div>HTTP Status: <strong style="color:var(--text);">' + (data.http_status || 'N/A') + '</strong></div>' +
                    '</div>' +
                '</div>';
        } else {
            result.innerHTML = 
                '<div style="padding:15px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:10px;">' +
                    '<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">' +
                        '<i class="fa-solid fa-times-circle" style="color:var(--red);font-size:20px;"></i>' +
                        '<strong style="color:var(--red);">Connection Failed!</strong>' +
                    '</div>' +
                    '<div style="font-size:13px;color:var(--muted);">' +
                        '<div>Worker: <strong style="color:var(--text);">' + url + '</strong></div>' +
                        '<div>Error: <strong style="color:var(--red);">' + (data.error || 'Unknown') + '</strong></div>' +
                        '<div style="margin-top:10px;">Hubi in Worker-kaagu uu jiro oo uu si fiican u shaqeynayo.</div>' +
                    '</div>' +
                '</div>';
        }
    } catch (error) {
        result.innerHTML = 
            '<div style="padding:15px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:10px;">' +
                '<strong style="color:var(--red);">Error: ' + error.message + '</strong>' +
            '</div>';
    }
}
'''
content = content.replace('function handleLogout()', status_funcs + '\nfunction handleLogout()')

with open("public/index.html", "w") as f:
    f.write(content)

print("✅ System Status page waa lagu daray!")
