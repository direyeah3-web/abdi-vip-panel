import shutil
import re

shutil.copy('public/index.html', 'public/index.html.backup_essential_render')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Raadi renderApkResults
pattern = r"function renderApkResults\(d\)\{.*?\n\}"
match = re.search(pattern, c, re.DOTALL)

new_render = """function renderApkResults(d){
    var el=document.getElementById('apk-results');
    var html='';

    // ⭐ ESSENTIAL SECTION — muhiimka kaliya
    var e=d.essential||{};
    html+='<div class="panel" style="margin-bottom:20px;border:2px solid var(--primary);background:linear-gradient(135deg,rgba(0,212,255,0.05),rgba(139,92,246,0.05));">'+
        '<h3 style="color:var(--primary);"><i class="fa-solid fa-star"></i> ESSENTIAL INFO</h3>'+
        '<div style="font-size:14px;line-height:2.2;">'+
        '<div>🌐 <b>Server URL:</b> <code style="background:var(--input-bg);padding:4px 8px;border-radius:6px;color:var(--green);">'+(e.server_url||'N/A')+'</code></div>'+
        '<div>📍 <b>Endpoint:</b> <code style="color:var(--yellow);">'+(e.endpoint||'N/A')+'</code></div>'+
        '<div>📡 <b>Full URL:</b> <code style="word-break:break-all;">'+(e.full_url||'N/A')+'</code></div>'+
        '<div>🔑 <b>License Methods:</b> '+((e.license_methods||[]).join(', ')||'N/A')+'</div>'+
        '<div>📋 <b>Response Fields:</b> '+((e.json_fields||[]).join(', ')||'N/A')+'</div>'+
        '</div>'+
        '</div>';

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

    // 2. License Routines (top 5 muhiim ah)
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-key"></i> License Routines ('+(d.license_count||0)+')</h3>';
    if(d.license_routines && d.license_routines.length>0){
        html+='<div style="max-height:250px;overflow-y:auto;font-size:11px;font-family:monospace;">';
        d.license_routines.forEach(function(l){
            html+='<div style="padding:5px;border-bottom:1px solid var(--border);word-break:break-all;">'+
                '<b style="color:var(--green);">'+l.file+'</b> : L'+l.line+' → <span style="color:var(--yellow);">'+l.match+'</span></div>';
        });
        html+='</div>';
    } else { html+='<p style="color:var(--muted);">Ma jiro license routines.</p>'; }
    html+='</div>';

    // 3. URLs (kaliya kuwa muhiim ah — ma aha schemas.android.com)
    var filteredUrls=(d.urls||[]).filter(function(u){
        var url=u.url||'';
        return url.startsWith('http') && !url.includes('schemas.android.com') && !url.includes('crbug.com') && !url.includes('google.com') && !url.includes('github.com') && !url.includes('curl.se') && !url.includes('llvm.org') && !url.includes('DeNA');
    });
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-link"></i> Loader URLs ('+filteredUrls.length+')</h3>';
    if(filteredUrls.length>0){
        html+='<div style="max-height:300px;overflow-y:auto;font-size:12px;font-family:monospace;">';
        var seen=new Set();
        filteredUrls.forEach(function(u){
            if(seen.has(u.url))return; seen.add(u.url);
            html+='<div style="padding:5px;border-bottom:1px solid var(--border);word-break:break-all;">'+
                '<span style="color:var(--green);">'+u.file+'</span> → <span style="color:var(--primary);">'+u.url+'</span></div>';
        });
        html+='</div>';
    } else { html+='<p style="color:var(--muted);">Ma jiro loader URLs.</p>'; }
    html+='</div>';

    // 4. Signature Checks (top 10)
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-fingerprint"></i> Signature Checks ('+(d.signature_count||0)+')</h3>';
    if(d.signature_checks && d.signature_checks.length>0){
        html+='<div style="max-height:250px;overflow-y:auto;font-size:11px;font-family:monospace;">';
        d.signature_checks.slice(0,15).forEach(function(s){
            html+='<div style="padding:4px;border-bottom:1px solid var(--border);word-break:break-all;"><b>'+s.file+'</b> : L'+s.line+' → <code>'+s.match+'</code></div>';
        });
        html+='</div>';
    } else { html+='<p style="color:var(--muted);">Ma jiro signature checks.</p>'; }
    html+='</div>';

    // 5. Integrity Checks
    html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-shield-halved"></i> Integrity / Anti-Tamper ('+(d.integrity_count||0)+')</h3>';
    if(d.integrity_checks && d.integrity_checks.length>0){
        html+='<div style="max-height:200px;overflow-y:auto;font-size:11px;font-family:monospace;">';
        d.integrity_checks.slice(0,15).forEach(function(i){
            html+='<div style="padding:4px;border-bottom:1px solid var(--border);word-break:break-all;"><b>'+i.file+'</b> : L'+i.line+' → <code>'+i.match+'</code></div>';
        });
        html+='</div>';
    } else { html+='<p style="color:var(--muted);">Ma jiro integrity checks.</p>'; }
    html+='</div>';

    el.innerHTML=html;
    showToast('Success','APK la baadhay!','success');
}"""

if match:
    c = c[:match.start()] + new_render + c[match.end():]
    print("1. renderApkResults essential: OK")
else:
    print("1. renderApkResults: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_essential_render")
