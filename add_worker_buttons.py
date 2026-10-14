import shutil

shutil.copy('public/index.html', 'public/index.html.safe8')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Ku dar saddex button — ka hor Deploy button
old_btn = """<button class="btn-primary" onclick="saveWorkerCode()" id="cw-save-btn"><i class="fa-solid fa-save"></i> Deploy</button>"""
new_btn = """<button class="btn-secondary" onclick="copyWorkerCode()" style="margin-right:8px;"><i class="fa-solid fa-copy"></i> Copy</button>
                    <button class="btn-secondary" onclick="selectAllWorkerCode()" style="margin-right:8px;"><i class="fa-solid fa-check-double"></i> Select All</button>
                    <button class="btn-secondary" onclick="backupWorkerCode()" style="margin-right:8px;"><i class="fa-solid fa-download"></i> Backup</button>
                    <button class="btn-primary" onclick="saveWorkerCode()" id="cw-save-btn"><i class="fa-solid fa-save"></i> Deploy</button>"""

if old_btn in c:
    c = c.replace(old_btn, new_btn, 1)
    print("1. Buttons: OK")
else:
    print("1. Buttons: LAMA HELIN")

# 2. Ku dar functions-ka cusub — ka hor async function saveWorkerCode()
old_func = "async function saveWorkerCode(){"
new_func = """function copyWorkerCode(){
    var code=document.getElementById('cw-code').value;
    if(!code){showToast('Warning','Code ma jiro','info');return;}
    if(navigator.clipboard && navigator.clipboard.writeText){
        navigator.clipboard.writeText(code).then(function(){
            showToast('Success','Code-ka waa la koobiyay!','success');
        }).catch(function(){
            // Fallback: textarea select + execCommand
            var ta=document.getElementById('cw-code');
            ta.select();
            document.execCommand('copy');
            showToast('Success','Code-ka waa la koobiyay!','success');
        });
    } else {
        var ta=document.getElementById('cw-code');
        ta.select();
        document.execCommand('copy');
        showToast('Success','Code-ka waa la koobiyay!','success');
    }
}

function selectAllWorkerCode(){
    var ta=document.getElementById('cw-code');
    if(!ta||!ta.value){showToast('Warning','Code ma jiro','info');return;}
    ta.focus();
    ta.select();
    showToast('Success','Code-ka oo dhan waa la doortay!','success');
}

async function backupWorkerCode(){
    var code=document.getElementById('cw-code').value;
    if(!code){showToast('Warning','Code ma jiro','info');return;}
    try{
        var t=localStorage.getItem('token');
        var r=await fetch('/api/worker/backup',{
            method:'POST',
            headers:{'Authorization':'Bearer '+t,'Content-Type':'application/json'},
            body:JSON.stringify({code:code})
        });
        var d=await r.json();
        if(d.success){
            showToast('Success','Backup la keydiyay!','success');
        } else {
            showToast('Error',d.error||'Backup wuu guuldareystay','error');
        }
    }catch(e){
        showToast('Error',e.message,'error');
    }
}

async function saveWorkerCode(){"""

if old_func in c:
    c = c.replace(old_func, new_func, 1)
    print("2. Functions: OK")
else:
    print("2. Functions: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.safe8")
