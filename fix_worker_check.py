# fix_worker_check.py - Hagaaji worker check si uu u hubiyo content-type

with open("server.js", "r") as f:
    content = f.read()

# Hel endpoint-ka worker-check hore
import re
pattern = r"app\.get\('/api/worker-check'.*?\}\);\s*\}\);"
match = re.search(pattern, content, re.DOTALL)

if match:
    new_worker = '''app.get('/api/worker-check', async (req, res) => {
    try {
        const startTime = Date.now();
        const workerUrl = req.query.worker_url || 'https://a.dirxx.workers.dev';
        
        try {
            const response = await fetch(workerUrl, { 
                method: 'GET',
                headers: { 'Accept': 'application/json' }
            });
            const responseTime = Date.now() - startTime;
            const contentType = response.headers.get('content-type') || '';
            
            // Hubi haddii jawaabtu tahay JSON
            const isJson = contentType.includes('application/json');
            
            // Hubi haddii Worker-ku uu leeyahay 'x-railway-edge' (taas macneheedu waa Worker-ku wuxuu u gudbiyaa Railway)
            const isProxied = response.headers.get('x-railway-edge') !== null;
            
            res.json({
                status: response.ok ? 'online' : 'error',
                worker_url: workerUrl,
                response_time: responseTime + 'ms',
                http_status: response.status,
                content_type: contentType,
                is_json: isJson,
                is_proxied: isProxied,
                reachable: response.ok,
                message: isProxied 
                    ? 'Worker-ku wuxuu u gudbiyaa Railway si guul leh!' 
                    : (isJson ? 'Worker-ku wuu shaqeynayaa (JSON)' : 'Worker-ku wuxuu soo celiyaa HTML'),
                timestamp: new Date().toISOString()
            });
        } catch (fetchError) {
            const responseTime = Date.now() - startTime;
            res.json({
                status: 'offline',
                worker_url: workerUrl,
                response_time: responseTime + 'ms',
                reachable: false,
                error: fetchError.message,
                timestamp: new Date().toISOString()
            });
        }
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});'''
    
    content = content[:match.start()] + new_worker + content[match.end():]
    
    with open("server.js", "w") as f:
        f.write(content)
    print("✅ /api/worker-check waa la hagaajiyay!")
else:
    print("❌ Ma helin /api/worker-check")
