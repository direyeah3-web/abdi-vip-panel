import shutil

shutil.copy('public/index.html', 'public/index.html.backup_helper')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Nav item — ka dib APK Analyzer
old_nav = """<a class="nav-item" onclick="loadPage('apk',this)"><i class="fa-solid fa-file-code"></i> <span>APK Analyzer</span></a>"""
new_nav = old_nav + """
        <a class="nav-item" onclick="loadPage('helper',this)"><i class="fa-solid fa-wand-magic-sparkles"></i> <span>Loader Helper</span></a>"""

if old_nav in c:
    c = c.replace(old_nav, new_nav, 1)
    print("1. Nav item: OK")
else:
    print("1. Nav item: LAMA HELIN")

# 2. Page logic — ka dib APK page
old_page = """await loadWorkerPage();
        }
        else if(p==='apk'){"""
new_page = """await loadWorkerPage();
        }
        else if(p==='helper'){
            c.innerHTML='<div class="panel-header" style="margin-bottom:20px;"><h1 style="font-size:24px;font-weight:800;">Loader Helper</h1></div>'+
            '<div class="panel"><h3><i class="fa-solid fa-upload"></i> Upload APK</h3>'+
                '<input type="file" id="helper-apk" accept=".apk" style="width:100%;padding:12px;background:var(--input-bg);border:1px solid var(--border);border-radius:10px;color:var(--text);margin-bottom:15px;">'+
                '<input type="text" id="helper-server-url" placeholder="Server URL (tusaale: https://a.dirxx.workers.dev)" style="width:100%;padding:12px;background:var(--input-bg);border:1px solid var(--border);border-radius:10px;color:var(--text);margin-bottom:15px;">'+
                '<button class="btn-primary" onclick="runLoaderHelper()" id="helper-btn" style="width:100%;justify-content:center;"><i class="fa-solid fa-wand-magic-sparkles"></i> Generate Helper Guide</button>'+
                '<div id="helper-progress" style="margin-top:15px;"></div>'+
            '</div>'+
            '<div id="helper-results" style="margin-top:20px;"></div>';
        }
        else if(p==='apk'){"""

if old_page in c:
    c = c.replace(old_page, new_page, 1)
    print("2. Page logic: OK")
else:
    print("2. Page logic: LAMA HELIN")

# 3. Functions — ka hor loadTelegramStatus
old_func = "async function loadTelegramStatus(){"
new_func = """async function runLoaderHelper(){
    var fileInput=document.getElementById('helper-apk');
    var serverInput=document.getElementById('helper-server-url');
    var btn=document.getElementById('helper-btn');
    var progress=document.getElementById('helper-progress');
    var results=document.getElementById('helper-results');
    if(!fileInput.files[0]){showToast('Warning','APK soo geli','info');return;}
    var file=fileInput.files[0];
    if(file.size>50*1024*1024){showToast('Warning','APK waa weyn (max 50MB)','info');return;}
    var serverUrl=serverInput.value.trim()||'https://a.dirxx.workers.dev';
    btn.disabled=true;
    btn.innerHTML='<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';
    progress.innerHTML='<p style="color:var(--muted);">1/3 — APK soo gelin...</p>';
    try{
        var reader=new FileReader();
        reader.onload=async function(e){
            var base64=e.target.result.split(',')[1];
            var t=localStorage.getItem('token');
            progress.innerHTML='<p style="color:var(--muted);">2/3 — APK keydi...</p>';
            var r=await fetch('/api/apk/upload',{method:'POST',headers:{'Authorization':'Bearer '+t,'Content-Type':'application/json'},body:JSON.stringify({filename:file.name,data:base64})});
            var d=await r.json();
            if(!d.success){progress.innerHTML='<p style="color:var(--red);">❌ '+d.error+'</p>';btn.disabled=false;btn.innerHTML='<i class="fa-solid fa-wand-magic-sparkles"></i> Generate Helper Guide';return;}
            progress.innerHTML='<p style="color:var(--muted);">3/3 — APK baadh...</p>';
            var r2=await fetch('/api/apk/analyze',{method:'POST',headers:{'Authorization':'Bearer '+t,'Content-Type':'application/json'},body:JSON.stringify({apkPath:d.path,filename:d.filename})});
            var d2=await r2.json();
            if(!d2.success){progress.innerHTML='<p style="color:var(--red);">❌ '+d2.error+'</p>';btn.disabled=false;btn.innerHTML='<i class="fa-solid fa-wand-magic-sparkles"></i> Generate Helper Guide';return;}
            progress.innerHTML='<p style="color:var(--muted);">Helper guide...</p>';
            var r3=await fetch('/api/loader/helper',{method:'POST',headers:{'Authorization':'Bearer '+t,'Content-Type':'application/json'},body:JSON.stringify({analysis:d2,serverUrl:serverUrl})});
            var d3=await r3.json();
            if(d3.success){
                progress.innerHTML='<p style="color:var(--green);">✅ Helper guide la diyaariyay!</p>';
                renderHelperResults(d3.helper,d2);
            }else{
                progress.innerHTML='<p style="color:var(--red);">❌ '+d3.error+'</p>';
            }
            btn.disabled=false;
            btn.innerHTML='<i class="fa-solid fa-wand-magic-sparkles"></i> Generate Helper Guide';
        };
        reader.readAsDataURL(file);
    }catch(e){
        progress.innerHTML='<p style="color:var(--red);">❌ '+e.message+'</p>';
        btn.disabled=false;
        btn.innerHTML='<i class="fa-solid fa-wand-magic-sparkles"></i> Generate Helper Guide';
    }
}

function renderHelperResults(h,analysis){
    var el=document.getElementById('helper-results');
    var html='';

    // 1. Server Location
    html+='<div class="panel" style="margin-bottom:20px;border:2px solid var(--primary);">'+
        '<h3 style="color:var(--primary);"><i class="fa-solid fa-server"></i> Server Location</h3>'+
        '<div style="font-size:14px;line-height:2;">'+
        '<div>📍 <b>Location:</b> <code>'+(h.server_location||'unknown')+'</code></div>'+
        '<div>🔧 <b>Patch Method:</b> <code>'+(h.patch_method||'N/A')+'</code></div>'+
        '</div></div>';

    // 2. License Flow
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-key"></i> License Flow</h3>'+
        '<div style="font-size:13px;line-height:2;">';
    (h.license_flow||[]).forEach(function(step){html+='<div>'+step+'</div>';});
    html+='</div></div>';

    // 3. Response Format
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-code"></i> Response Format</h3>'+
        '<div style="font-size:11px;font-family:monospace;background:var(--input-bg);padding:15px;border-radius:10px;overflow-x:auto;">'+
        '<pre>'+JSON.stringify(h.response_format,null,2)+'</pre></div></div>';

    // 4. Code Snippet
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-terminal"></i> Loader Code Snippet</h3>'+
        '<div style="font-size:11px;font-family:monospace;background:#0a0a0f;color:#e6f1ff;padding:15px;border-radius:10px;overflow-x:auto;">'+
        '<pre>'+(h.code_snippet||'N/A')+'</pre></div></div>';

    // 5. Worker Template
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-brands fa-cloudflare"></i> Cloudflare Worker Template</h3>'+
        '<div style="font-size:11px;font-family:monospace;background:#0a0a0f;color:#e6f1ff;padding:15px;border-radius:10px;overflow-x:auto;">'+
        '<pre>'+(h.worker_template||'N/A')+'</pre></div></div>';

    // 6. Steps
    html+='<div class="panel"><h3><i class="fa-solid fa-list-check"></i> Steps</h3>'+
        '<div style="font-size:13px;line-height:2;">';
    (h.steps||[]).forEach(function(s){html+='<div>'+s+'</div>';});
    html+='</div></div>';

    el.innerHTML=html;
    showToast('Success','Helper guide la diyaariyay!','success');
}

async function loadTelegramStatus(){"""

if old_func in c:
    c = c.replace(old_func, new_func, 1)
    print("3. Functions: OK")
else:
    print("3. Functions: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_helper")
