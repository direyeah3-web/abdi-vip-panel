import shutil

shutil.copy('public/index.html', 'public/index.html.backup_apk')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Nav item
old_nav = """<a class="nav-item" onclick="loadPage('worker',this)"><i class="fa-solid fa-cloud"></i> <span>Cloudflare Worker</span></a>"""
new_nav = old_nav + """
        <a class="nav-item" onclick="loadPage('apk',this)"><i class="fa-solid fa-file-code"></i> <span>APK Analyzer</span></a>"""

if old_nav in c:
    c = c.replace(old_nav, new_nav, 1)
    print("1. Nav item: OK")
else:
    print("1. Nav item: LAMA HELIN")

# 2. Page logic
old_page = """await loadWorkerPage();
        }"""
new_page = """await loadWorkerPage();
        }
        else if(p==='apk'){
            c.innerHTML='<div class="panel-header" style="margin-bottom:20px;"><h1 style="font-size:24px;font-weight:800;">APK Analyzer</h1></div>'+
            '<div class="panel"><h3 style="margin-bottom:15px;font-size:16px;"><i class="fa-solid fa-upload" style="color:var(--primary);margin-right:8px;"></i> Upload APK</h3>'+
                '<input type="file" id="apk-file" accept=".apk" style="width:100%;padding:12px;background:var(--input-bg);border:1px solid var(--border);border-radius:10px;color:var(--text);margin-bottom:15px;">'+
                '<button class="btn-primary" onclick="analyzeApk()" id="apk-analyze-btn" style="width:100%;justify-content:center;"><i class="fa-solid fa-magnifying-glass"></i> Analyze APK</button>'+
                '<div id="apk-progress" style="margin-top:15px;"></div>'+
            '</div>'+
            '<div id="apk-results" style="margin-top:20px;"></div>';
        }"""

if old_page in c:
    c = c.replace(old_page, new_page, 1)
    print("2. Page: OK")
else:
    print("2. Page: LAMA HELIN")

# 3. Functions
old_func = "async function loadTelegramStatus(){"
new_func = """async function analyzeApk(){
    var fileInput=document.getElementById('apk-file');
    var btn=document.getElementById('apk-analyze-btn');
    var progress=document.getElementById('apk-progress');
    var results=document.getElementById('apk-results');
    if(!fileInput.files[0]){showToast('Warning','APK soo geli','info');return;}
    var file=fileInput.files[0];
    if(file.size>50*1024*1024){showToast('Warning','APK waa weyn (max 50MB)','info');return;}
    btn.disabled=true;
    btn.innerHTML='<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';
    progress.innerHTML='<p style="color:var(--muted);">1/3 — APK soo gelin...</p>';
    try{
        var reader=new FileReader();
        reader.onload=async function(e){
            var base64=e.target.result.split(',')[1];
            var t=localStorage.getItem('token');
            progress.innerHTML='<p style="color:var(--muted);">2/3 — APK keydi...</p>';
            var r=await fetch('/api/apk/upload',{
                method:'POST',
                headers:{'Authorization':'Bearer '+t,'Content-Type':'application/json'},
                body:JSON.stringify({filename:file.name,data:base64})
            });
            var d=await r.json();
            if(!d.success){progress.innerHTML='<p style="color:var(--red);">❌ '+d.error+'</p>';btn.disabled=false;btn.innerHTML='<i class="fa-solid fa-magnifying-glass"></i> Analyze APK';return;}
            progress.innerHTML='<p style="color:var(--muted);">3/3 — APK baadh...</p>';
            var r2=await fetch('/api/apk/analyze',{
                method:'POST',
                headers:{'Authorization':'Bearer '+t,'Content-Type':'application/json'},
                body:JSON.stringify({apkPath:d.path,filename:d.filename})
            });
            var d2=await r2.json();
            if(d2.success){
                progress.innerHTML='<p style="color:var(--green);">✅ Analysis dhamaystiran!</p>';
                renderApkResults(d2);
            }else{
                progress.innerHTML='<p style="color:var(--red);">❌ '+d2.error+'</p>';
            }
            btn.disabled=false;
            btn.innerHTML='<i class="fa-solid fa-magnifying-glass"></i> Analyze APK';
        };
        reader.readAsDataURL(file);
    }catch(e){
        progress.innerHTML='<p style="color:var(--red);">❌ '+e.message+'</p>';
        btn.disabled=false;
        btn.innerHTML='<i class="fa-solid fa-magnifying-glass"></i> Analyze APK';
    }
}

function renderApkResults(d){
    var el=document.getElementById('apk-results');
    var html='';
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-link"></i> URLs ('+d.urls_count+')</h3>';
    if(d.urls && d.urls.length>0){
        html+='<div style="max-height:300px;overflow-y:auto;font-size:12px;font-family:monospace;">';
        d.urls.forEach(function(u){html+='<div style="padding:6px;border-bottom:1px solid var(--border);word-break:break-all;">'+u+'</div>';});
        html+='</div>';
    } else { html+='<p style="color:var(--muted);">Ma jiro URLs.</p>'; }
    html+='</div>';

    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-key"></i> Licenses ('+d.licenses_count+')</h3>';
    if(d.licenses && d.licenses.length>0){
        html+='<div style="max-height:200px;overflow-y:auto;font-size:12px;font-family:monospace;">';
        d.licenses.slice(0,50).forEach(function(l){html+='<div style="padding:6px;border-bottom:1px solid var(--border);">'+l+'</div>';});
        html+='</div>';
    } else { html+='<p style="color:var(--muted);">Ma jiro licenses.</p>'; }
    html+='</div>';

    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-shield"></i> Protections</h3>';
    if(d.protection_signs && d.protection_signs.length>0){
        d.protection_signs.forEach(function(p){html+='<div style="padding:6px;font-size:12px;font-family:monospace;">⚠️ '+p+'</div>';});
    } else { html+='<p style="color:var(--muted);">Ma jiro protections la aqoonsaday.</p>'; }
    html+='</div>';

    html+='<div class="panel"><h3><i class="fa-solid fa-code"></i> Smali / Native / Response</h3>';
    html+='<p style="font-size:12px;color:var(--muted);"><b>Smali files:</b> '+(d.smali_files||[]).length+'</p>';
    html+='<p style="font-size:12px;color:var(--muted);"><b>Native libs:</b> '+(d.native_libs||[]).length+'</p>';
    html+='<p style="font-size:12px;color:var(--muted);"><b>Response format:</b> '+(d.response_format||'N/A')+'</p>';
    html+='</div>';

    el.innerHTML=html;
    showToast('Success','APK la baadhay!','success');
}

async function loadTelegramStatus(){"""

if old_func in c:
    c = c.replace(old_func, new_func, 1)
    print("3. Functions: OK")
else:
    print("3. Functions: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_apk")
