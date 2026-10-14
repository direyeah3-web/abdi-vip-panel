import shutil
import re

shutil.copy('public/index.html', 'public/index.html.backup_render')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Raadi function-ka renderApkResults oo dhan
pattern = r"function renderApkResults\(d\)\{.*?\n\}"
match = re.search(pattern, c, re.DOTALL)

new_render = """function renderApkResults(d){
    var el=document.getElementById('apk-results');
    var html='';

    // 1. Summary
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-chart-simple"></i> Summary</h3>'+
        '<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:10px;font-size:13px;">'+
        '<div>📦 Entries: <b>'+d.total_entries+'</b></div>'+
        '<div>📄 Smali: <b>'+d.smali_files_count+'</b></div>'+
        '<div>⚙️ Native libs: <b>'+d.native_libs_count+'</b></div>'+
        '<div>📱 DEX: <b>'+d.dex_files_count+'</b></div>'+
        '<div>🔗 URLs: <b>'+d.urls_count+'</b></div>'+
        '<div>🔑 Licenses: <b>'+d.licenses_count+'</b></div>'+
        '</div></div>';

    // 2. URLs (file -> line -> URL)
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-link"></i> URLs ('+d.urls_count+')</h3>';
    if(d.urls && d.urls.length>0){
        html+='<div style="max-height:400px;overflow-y:auto;font-size:11px;font-family:monospace;">';
        d.urls.forEach(function(u){
            html+='<div style="padding:6px;border-bottom:1px solid var(--border);word-break:break-all;">'+
                '<span style="color:var(--green);">'+u.file+'</span> → <span style="color:var(--yellow);">L'+u.line+'</span> → <span style="color:var(--primary);">'+u.url+'</span></div>';
        });
        html+='</div>';
    } else { html+='<p style="color:var(--muted);">Ma jiro URLs.</p>'; }
    html+='</div>';

    // 3. License/Auth/Verification routines
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-key"></i> License Routines ('+(d.license_routines||[]).length+')</h3>';
    if(d.license_routines && d.license_routines.length>0){
        html+='<div style="max-height:400px;overflow-y:auto;font-size:11px;font-family:monospace;">';
        d.license_routines.forEach(function(l){
            html+='<div style="padding:8px;border-bottom:1px solid var(--border);">'+
                '<div><b>'+l.file+'</b> : L'+l.line+'</div>'+
                (l.class_name ? '<div>Class: <code>'+l.class_name+'</code></div>' : '')+
                (l.method_name ? '<div>Method: <code>'+l.method_name+'</code></div>' : '')+
                (l.smali_line ? '<div style="color:var(--muted);">'+l.smali_line+'</div>' : '')+
                (l.match ? '<div style="color:var(--red);">'+l.match+'</div>' : '')+
                '</div>';
        });
        html+='</div>';
    } else { html+='<p style="color:var(--muted);">Ma jiro license routines.</p>'; }
    html+='</div>';

    // 4. Signature checks
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-fingerprint"></i> Signature Checks ('+(d.signature_checks||[]).length+')</h3>';
    if(d.signature_checks && d.signature_checks.length>0){
        html+='<div style="max-height:300px;overflow-y:auto;font-size:11px;font-family:monospace;">';
        d.signature_checks.forEach(function(s){
            html+='<div style="padding:6px;border-bottom:1px solid var(--border);"><b>'+s.file+'</b> : L'+s.line+' → <code>'+s.match+'</code></div>';
        });
        html+='</div>';
    } else { html+='<p style="color:var(--muted);">Ma jiro signature checks.</p>'; }
    html+='</div>';

    // 5. Integrity checks
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-shield-halved"></i> Integrity Checks ('+(d.integrity_checks||[]).length+')</h3>';
    if(d.integrity_checks && d.integrity_checks.length>0){
        html+='<div style="max-height:300px;overflow-y:auto;font-size:11px;font-family:monospace;">';
        d.integrity_checks.forEach(function(i){
            html+='<div style="padding:6px;border-bottom:1px solid var(--border);"><b>'+i.file+'</b> : L'+i.line+' → <code>'+i.match+'</code></div>';
        });
        html+='</div>';
    } else { html+='<p style="color:var(--muted);">Ma jiro integrity checks.</p>'; }
    html+='</div>';

    // 6. Startup calls
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-rocket"></i> Startup Calls ('+(d.startup_calls||[]).length+')</h3>';
    if(d.startup_calls && d.startup_calls.length>0){
        html+='<div style="max-height:200px;overflow-y:auto;font-size:11px;font-family:monospace;">';
        d.startup_calls.forEach(function(s){
            html+='<div style="padding:6px;border-bottom:1px solid var(--border);"><b>'+s.file+'</b> : L'+s.line+' → '+s.method+'</div>';
        });
        html+='</div>';
    } else { html+='<p style="color:var(--muted);">Ma jiro startup calls.</p>'; }
    html+='</div>';

    // 7. DB licenses
    html+='<div class="panel"><h3><i class="fa-solid fa-database"></i> DB Licenses ('+(d.db_licenses||[]).length+')</h3>';
    if(d.db_licenses && d.db_licenses.length>0){
        html+='<div style="max-height:200px;overflow-y:auto;font-size:11px;font-family:monospace;">';
        d.db_licenses.forEach(function(l){
            html+='<div style="padding:4px;border-bottom:1px solid var(--border);">'+l+'</div>';
        });
        html+='</div>';
    } else { html+='<p style="color:var(--muted);">Ma jiro DB licenses.</p>'; }
    html+='</div>';

    el.innerHTML=html;
    showToast('Success','APK la baadhay!','success');
}"""

if match:
    c = c[:match.start()] + new_render + c[match.end():]
    print("1. renderApkResults: OK")
else:
    print("1. renderApkResults: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_render")
