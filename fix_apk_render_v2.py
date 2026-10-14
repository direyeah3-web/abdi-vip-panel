import shutil
import re

shutil.copy('public/index.html', 'public/index.html.backup_render_v2')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

pattern = r"function renderApkResults\(d\)\{.*?\n\}"
match = re.search(pattern, c, re.DOTALL)

new_render = """function renderApkResults(d){
    var el=document.getElementById('apk-results');
    var html='';

    // 1. APK Identification
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-mobile-screen"></i> APK Identification</h3>'+
        '<div style="font-size:13px;line-height:2;">'+
        '<div>📦 <b>Package:</b> <code>'+(d.package_name||'N/A')+'</code></div>'+
        '<div>🚀 <b>Launcher:</b> <code>'+(d.launcher_activity||'N/A')+'</code></div>'+
        '<div>📱 <b>Application:</b> <code>'+(d.application_class||'N/A')+'</code></div>'+
        '<div>📄 <b>DEX files:</b> '+((d.dex_files||[]).join(', ')||'N/A')+'</div>'+
        '<div>⚙️ <b>Native libs:</b> '+((d.native_libs||[]).join(', ')||'N/A')+'</div>'+
        '<div>📁 <b>Assets:</b> '+((d.assets||[]).slice(0,5).join(', ')||'N/A')+((d.assets||[]).length>5?' ...':'')+'</div>'+
        '</div></div>';

    // 2. License routines
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-key"></i> License Routines ('+(d.license_count||0)+')</h3>';
    if(d.license_routines && d.license_routines.length>0){
        html+='<div style="max-height:400px;overflow-y:auto;font-size:11px;font-family:monospace;">';
        d.license_routines.forEach(function(l){
            html+='<div style="padding:6px;border-bottom:1px solid var(--border);word-break:break-all;">'+
                '<b style="color:var(--green);">'+l.file+'</b> : L'+l.line+' → <span style="color:var(--yellow);">'+l.match+'</span></div>';
        });
        html+='</div>';
    } else { html+='<p style="color:var(--muted);">Ma jiro license routines.</p>'; }
    html+='</div>';

    // 3. URLs
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-link"></i> URLs ('+(d.urls_count||0)+')</h3>';
    if(d.urls && d.urls.length>0){
        html+='<div style="max-height:400px;overflow-y:auto;font-size:11px;font-family:monospace;">';
        var seen=new Set();
        d.urls.forEach(function(u){
            var key=u.url;
            if(seen.has(key))return; seen.add(key);
            html+='<div style="padding:4px;border-bottom:1px solid var(--border);word-break:break-all;">'+
                '<span style="color:var(--green);">'+u.file+'</span> → <span style="color:var(--primary);">'+u.url+'</span></div>';
        });
        html+='</div>';
    } else { html+='<p style="color:var(--muted);">Ma jiro URLs.</p>'; }
    html+='</div>';

    // 4. Signature checks
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-fingerprint"></i> Signature Checks ('+(d.signature_count||0)+')</h3>';
    if(d.signature_checks && d.signature_checks.length>0){
        html+='<div style="max-height:300px;overflow-y:auto;font-size:11px;font-family:monospace;">';
        d.signature_checks.forEach(function(s){
            html+='<div style="padding:4px;border-bottom:1px solid var(--border);word-break:break-all;"><b>'+s.file+'</b> : L'+s.line+' → <code>'+s.match+'</code></div>';
        });
        html+='</div>';
    } else { html+='<p style="color:var(--muted);">Ma jiro signature checks.</p>'; }
    html+='</div>';

    // 5. Integrity checks
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-shield-halved"></i> Integrity / Anti-Tamper ('+(d.integrity_count||0)+')</h3>';
    if(d.integrity_checks && d.integrity_checks.length>0){
        html+='<div style="max-height:300px;overflow-y:auto;font-size:11px;font-family:monospace;">';
        d.integrity_checks.forEach(function(i){
            html+='<div style="padding:4px;border-bottom:1px solid var(--border);word-break:break-all;"><b>'+i.file+'</b> : L'+i.line+' → <code>'+i.match+'</code></div>';
        });
        html+='</div>';
    } else { html+='<p style="color:var(--muted);">Ma jiro integrity checks.</p>'; }
    html+='</div>';

    // 6. Native methods + JNI
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-brands fa-java"></i> Native / JNI ('+(d.jni_count||0)+')</h3>';
    if(d.native_methods && d.native_methods.length>0){
        html+='<div style="max-height:200px;overflow-y:auto;font-size:11px;font-family:monospace;">';
        d.native_methods.forEach(function(n){
            html+='<div style="padding:4px;border-bottom:1px solid var(--border);"><b>'+n.file+'</b> : L'+n.line+' → <code>'+n.match+'</code></div>';
        });
        html+='</div>';
    } else { html+='<p style="color:var(--muted);">Ma jiro native methods.</p>'; }
    if(d.jni_exports && d.jni_exports.length>0){
        html+='<div style="margin-top:10px;font-size:11px;font-family:monospace;">';
        d.jni_exports.slice(0,30).forEach(function(j){
            html+='<div style="padding:4px;"><span style="color:var(--green);">'+j.file+'</span> → <code>'+j.symbol+'</code></div>';
        });
        html+='</div>';
    }
    html+='</div>';

    // 7. Hermes bytecode
    if(d.hermes){
        html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-brands fa-react"></i> Hermes Bytecode</h3>'+
            '<div style="font-size:13px;line-height:2;">'+
            '<div>📦 <b>Magic:</b> <code>'+d.hermes.magic+'</code></div>'+
            '<div>🔢 <b>Version:</b> <code>'+d.hermes.version+'</code></div>'+
            '<div>📊 <b>Size:</b> '+d.hermes.size+' bytes</div>'+
            '<div>🔑 <b>License hits:</b> '+(d.hermes.license_hits||[]).join(', ')+'</div>'+
            '</div></div>';
    }

    el.innerHTML=html;
    showToast('Success','APK la baadhay!','success');
}"""

if match:
    c = c[:match.start()] + new_render + c[match.end():]
    print("1. renderApkResults v2: OK")
else:
    print("1. renderApkResults v2: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_render_v2")
