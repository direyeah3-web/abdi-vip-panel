# fix_status_frontend.py - Hagaaji frontend-ka System Status

with open("public/index.html", "r") as f:
    content = f.read()

# Hel loadSystemStatus function
start = content.find("async function loadSystemStatus()")
end = content.find("async function testWorkerConnection()")

if start != -1 and end != -1:
    new_func = '''async function loadSystemStatus() {
    try {
        // 1. Hubi Server-ka
        var serverStart = Date.now();
        var serverRes = await fetch('/api/health');
        var serverTime = Date.now() - serverStart;
        var serverData = await serverRes.json();
        
        document.getElementById('server-status').innerHTML = '<span style="color:var(--green);font-size:16px;">●</span> Online';
        document.getElementById('response-time').textContent = serverTime + 'ms';
        
        // 2. Server Details
        document.getElementById('server-details').innerHTML = 
            '<div style="font-size:13px;line-height:2;">' +
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Status:</span><strong style="color:var(--green);">' + (serverData.status || 'ok') + '</strong></div>' +
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Version:</span><strong>' + (serverData.version || 'N/A') + '</strong></div>' +
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Node:</span><strong>' + (serverData.node_version || 'N/A') + '</strong></div>' +
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Environment:</span><strong>' + (serverData.environment || 'N/A') + '</strong></div>' +
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Users:</span><strong>' + (serverData.database?.users || 0) + '</strong></div>' +
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Licenses:</span><strong>' + (serverData.database?.licenses || 0) + '</strong></div>' +
                '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Uptime:</span><strong>' + Math.floor(serverData.uptime || 0) + 's</strong></div>' +
            '</div>';
        
        // 3. Hubi Worker-ka
        var workerUrl = 'https://a.dirxx.workers.dev';
        try {
            var workerRes = await fetch('/api/worker-check?worker_url=' + encodeURIComponent(workerUrl));
            var workerData = await workerRes.json();
            
            if (workerData.reachable) {
                document.getElementById('worker-status').innerHTML = '<span style="color:var(--green);font-size:16px;">●</span> Online';
                document.getElementById('connection-status').innerHTML = '<span style="color:var(--green);font-size:16px;">●</span> Connected';
                document.getElementById('worker-details').innerHTML = 
                    '<div style="font-size:13px;line-height:2;">' +
                        '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Status:</span><strong style="color:var(--green);">Online</strong></div>' +
                        '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">URL:</span><strong style="font-size:11px;">' + workerUrl + '</strong></div>' +
                        '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">HTTP:</span><strong>' + (workerData.http_status || 'N/A') + '</strong></div>' +
                        '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Type:</span><strong>' + (workerData.content_type || 'N/A') + '</strong></div>' +
                        '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Proxied:</span><strong style="color:var(--green);">' + (workerData.is_proxied ? 'Yes' : 'No') + '</strong></div>' +
                        '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Response:</span><strong>' + (workerData.response_time || 'N/A') + '</strong></div>' +
                        '<div style="margin-top:10px;padding:10px;background:rgba(16,185,129,.1);border-radius:8px;font-size:12px;color:var(--green);">' + (workerData.message || '') + '</div>' +
                    '</div>';
            } else {
                document.getElementById('worker-status').innerHTML = '<span style="color:var(--yellow);font-size:16px;">●</span> Warning';
                document.getElementById('connection-status').innerHTML = '<span style="color:var(--yellow);font-size:16px;">●</span> Partial';
                document.getElementById('worker-details').innerHTML = 
                    '<div style="font-size:13px;line-height:2;">' +
                        '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Status:</span><strong style="color:var(--yellow);">Warning</strong></div>' +
                        '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">URL:</span><strong style="font-size:11px;">' + workerUrl + '</strong></div>' +
                        '<div style="display:flex;justify-content:space-between;"><span style="color:var(--muted);">Error:</span><strong style="color:var(--red);font-size:11px;">' + (workerData.error || 'Unknown') + '</strong></div>' +
                    '</div>';
            }
        } catch (workerError) {
            document.getElementById('worker-status').textContent = 'Error';
            document.getElementById('connection-status').textContent = 'Error';
        }
    } catch (error) {
        console.error('Status error:', error);
        document.getElementById('server-status').textContent = 'Error';
    }
}

'''
    content = content[:start] + new_func + content[end:]
    with open("public/index.html", "w") as f:
        f.write(content)
    print("✅ System Status frontend waa la hagaajiyay!")
else:
    print("❌ Ma helin loadSystemStatus")
