import shutil

shutil.copy('public/index.html', 'public/index.html.safe7')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Ku dar functions-ka — ka hor async function loadTelegramStatus()
old = "async function loadTelegramStatus(){"

new = """async function loadWorkerPage(){
    try{
        var t=localStorage.getItem('token');
        var r=await fetch('/api/worker/status',{headers:{'Authorization':'Bearer '+t}});
        var d=await r.json();
        var statusEl=document.getElementById('cw-status');
        var sizeEl=document.getElementById('cw-code-size');
        var respEl=document.getElementById('cw-response');
        var urlEl=document.getElementById('cw-url');
        if(!statusEl)return;
        if(d.success && d.online){
            statusEl.innerHTML='<span style="color:var(--green);font-size:16px;">●</span> Online';
            sizeEl.textContent=(d.code_length||0)+' bytes';
            respEl.textContent=(d.response_time||'N/A');
            urlEl.textContent=(d.worker_url||'N/A');
        } else {
            statusEl.innerHTML='<span style="color:var(--red);font-size:16px;">●</span> Offline';
            sizeEl.textContent='0 bytes';
            respEl.textContent='N/A';
            urlEl.textContent='N/A';
        }
        // Soo qaado code-ka worker-ka
        var cr=await fetch('/api/worker/code',{headers:{'Authorization':'Bearer '+t}});
        var cd=await cr.json();
        var codeEl=document.getElementById('cw-code');
        if(cd.success && codeEl){
            codeEl.value=cd.code||'';
        } else if(codeEl){
            codeEl.value='// Khalad: '+(cd.error||'Code lama helin');
        }
    }catch(e){console.error('Worker page error:',e);}
}

async function saveWorkerCode(){
    var btn=document.getElementById('cw-save-btn');
    var code=document.getElementById('cw-code').value;
    var result=document.getElementById('cw-result');
    if(!code){showToast('Warning','Code ma jiro','info');return;}
    btn.disabled=true;
    btn.innerHTML='<i class="fa-solid fa-spinner fa-spin"></i> Deploying...';
    result.innerHTML='<p style="color:var(--muted);">Worker-ka waa la deploy-gareynayaa...</p>';
    try{
        var t=localStorage.getItem('token');
        var r=await fetch('/api/worker/code',{
            method:'POST',
            headers:{'Authorization':'Bearer '+t,'Content-Type':'application/json'},
            body:JSON.stringify({code:code})
        });
        var d=await r.json();
        if(d.success){
            result.innerHTML='<div style="padding:15px;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);border-radius:10px;">'+
                '<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;"><i class="fa-solid fa-check-circle" style="color:var(--green);font-size:20px;"></i><strong style="color:var(--green);">Deploy Successful!</strong></div>'+
                '<div style="font-size:13px;color:var(--muted);">'+(d.message||'Worker la cusboonaysiiyay')+'</div>'+
                '</div>';
            showToast('Success','Worker la deploy-gareeyay!','success');
            setTimeout(function(){loadWorkerPage();},1500);
        } else {
            result.innerHTML='<div style="padding:15px;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:10px;">'+
                '<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;"><i class="fa-solid fa-times-circle" style="color:var(--red);font-size:20px;"></i><strong style="color:var(--red);">Deploy Failed!</strong></div>'+
                '<div style="font-size:13px;color:var(--muted);word-break:break-all;">'+(d.error||'Unknown error')+'</div>'+
                '</div>';
            showToast('Error','Deploy wuu guuldareystay','error');
        }
    }catch(e){
        result.innerHTML='<div style="padding:15px;background:rgba(239,68,68,0.1);border-radius:10px;"><strong style="color:var(--red);">Error: '+e.message+'</strong></div>';
    }
    btn.disabled=false;
    btn.innerHTML='<i class="fa-solid fa-save"></i> Deploy';
}

async function loadTelegramStatus(){"""

if old in c:
    c = c.replace(old, new, 1)
    print("1. Worker functions: OK")
else:
    print("1. Worker functions: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.safe7")
