import shutil

shutil.copy('public/index.html', 'public/index.html.backup_loader_config_page')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Nav item — ka dib Loader Helper
old_nav = """<a class="nav-item" onclick="loadPage('helper',this)"><i class="fa-solid fa-wand-magic-sparkles"></i> <span>Loader Helper</span></a>"""
new_nav = old_nav + """
        <a class="nav-item" onclick="loadPage('loader-config',this)"><i class="fa-solid fa-sliders"></i> <span>Loader Config</span></a>"""

if old_nav in c:
    c = c.replace(old_nav, new_nav, 1)
    print("1. Nav item: OK")
else:
    print("1. Nav item: LAMA HELIN")

# 2. Page logic — ka dib Loader Helper page
old_page = """await loadWorkerPage();
        }
        else if(p==='helper'){"""
new_page = """await loadWorkerPage();
        }
        else if(p==='loader-config'){
            c.innerHTML='<div class="panel-header" style="margin-bottom:20px;"><h1 style="font-size:24px;font-weight:800;"><i class="fa-solid fa-sliders" style="color:var(--primary);"></i> Loader Config</h1><button class="btn-secondary" onclick="loadLoaderConfig()"><i class="fa-solid fa-refresh"></i> Refresh</button></div>'+
            '<div id="loader-config-content">Loading...</div>';
            loadLoaderConfig();
        }
        else if(p==='helper'){"""

if old_page in c:
    c = c.replace(old_page, new_page, 1)
    print("2. Page logic: OK")
else:
    print("2. Page logic: LAMA HELIN")

# 3. Functions — ka hor loadTelegramStatus
old_func = "async function loadTelegramStatus(){"
new_func = """async function loadLoaderConfig(){
    try{
        var t=localStorage.getItem('token');
        var r=await fetch('/api/loader/remote-config',{headers:{'Authorization':'Bearer '+t}});
        var d=await r.json();
        if(!d.success){document.getElementById('loader-config-content').innerHTML='<p style="color:var(--red);">Error: '+(d.error||'Unknown')+'</p>';return;}
        var cfg=d.config||{};
        var html='';

        // ===== 1. LOADER STATE =====
        html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-power-off" style="color:var(--green);"></i> Loader State</h3>'+
        '<div style="font-size:13px;line-height:2;">'+
        '<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border);"><span>Maintenance Mode</span>'+
        '<button onclick="toggleConfig(\\'maintenance_mode\\','+(cfg.maintenance_mode?'true':'false')+')" style="padding:6px 16px;border-radius:20px;border:none;cursor:pointer;background:'+(cfg.maintenance_mode?'var(--red)':'var(--green)')+';color:#fff;font-size:12px;font-weight:600;">'+(cfg.maintenance_mode?'ON':'OFF')+'</button></div>'+
        '<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border);"><span>Update Required</span>'+
        '<button onclick="toggleConfig(\\'update_required\\','+(cfg.update_required?'true':'false')+')" style="padding:6px 16px;border-radius:20px;border:none;cursor:pointer;background:'+(cfg.update_required?'var(--yellow)':'var(--green)')+';color:#fff;font-size:12px;font-weight:600;">'+(cfg.update_required?'ON':'OFF')+'</button></div>'+
        '<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border);"><span>Crash Fix</span>'+
        '<button onclick="toggleConfig(\\'crash_fix\\','+(cfg.crash_fix?'true':'false')+')" style="padding:6px 16px;border-radius:20px;border:none;cursor:pointer;background:'+(cfg.crash_fix?'var(--green)':'var(--muted)')+';color:#fff;font-size:12px;font-weight:600;">'+(cfg.crash_fix?'ON':'OFF')+'</button></div>'+
        '<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;"><span>Floating Menu</span>'+
        '<button onclick="toggleConfig(\\'floating_menu_enabled\\','+(cfg.floating_menu_enabled?'true':'false')+')" style="padding:6px 16px;border-radius:20px;border:none;cursor:pointer;background:'+(cfg.floating_menu_enabled?'var(--green)':'var(--muted)')+';color:#fff;font-size:12px;font-weight:600;">'+(cfg.floating_menu_enabled?'ON':'OFF')+'</button></div>'+
        '</div></div>';

        // ===== 2. LOADER VERSION =====
        html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-code-branch"></i> App Version</h3>'+
        '<div style="margin-bottom:10px;"><label style="font-size:12px;color:var(--muted);">App Version</label>'+
        '<input type="text" id="cfg_app_version" value="'+(cfg.app_version||'')+'" style="width:100%;padding:12px;background:var(--input-bg);border:1px solid var(--border);border-radius:10px;color:var(--text);margin-top:6px;"></div>'+
        '<div style="margin-bottom:10px;"><label style="font-size:12px;color:var(--muted);">Update URL</label>'+
        '<input type="text" id="cfg_update_url" value="'+(cfg.update_url||'')+'" placeholder="https://..." style="width:100%;padding:12px;background:var(--input-bg);border:1px solid var(--border);border-radius:10px;color:var(--text);margin-top:6px;"></div>'+
        '<div style="margin-bottom:10px;"><label style="font-size:12px;color:var(--muted);">Update Message</label>'+
        '<input type="text" id="cfg_update_message" value="'+(cfg.update_message||'')+'" style="width:100%;padding:12px;background:var(--input-bg);border:1px solid var(--border);border-radius:10px;color:var(--text);margin-top:6px;"></div>'+
        '<div style="margin-bottom:10px;"><label style="font-size:12px;color:var(--muted);">Maintenance Message</label>'+
        '<input type="text" id="cfg_maintenance_message" value="'+(cfg.maintenance_message||'')+'" style="width:100%;padding:12px;background:var(--input-bg);border:1px solid var(--border);border-radius:10px;color:var(--text);margin-top:6px;"></div>'+
        '<button class="btn-primary" onclick="saveLoaderConfig()" style="width:100%;justify-content:center;"><i class="fa-solid fa-save"></i> Save Config</button></div>';

        // ===== 3. GAME VERSION =====
        html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-gamepad"></i> Game Version</h3>'+
        '<select id="cfg_game_version" style="width:100%;padding:12px;background:var(--input-bg);border:1px solid var(--border);border-radius:10px;color:var(--text);">'+
        ['GL','KR','TW','VN','BGMI'].map(function(g){
            return '<option value="'+g+'"'+(cfg.game_version===g?' selected':'')+'>'+g+'</option>';
        }).join('')+
        '</select>'+
        '<div style="margin-top:10px;"><label style="font-size:12px;color:var(--muted);">Shizuku Mode</label>'+
        '<select id="cfg_shizuku_mode" style="width:100%;padding:12px;background:var(--input-bg);border:1px solid var(--border);border-radius:10px;color:var(--text);margin-top:6px;">'+
        '<option value="ADB Process / Rootless"'+(cfg.shizuku_mode==='ADB Process / Rootless'?' selected':'')+'>ADB Process / Rootless</option>'+
        '<option value="Root"'+(cfg.shizuku_mode==='Root'?' selected':'')+'>Root</option>'+
        '<option value="Shizuku"'+(cfg.shizuku_mode==='Shizuku'?' selected':'')+'>Shizuku</option>'+
        '</select></div></div>';

        // ===== 4. BAN LIST =====
        var banList = cfg.ban_list || [];
        html+='<div class="panel"><h3><i class="fa-solid fa-ban" style="color:var(--red);"></i> Ban List ('+banList.length+')</h3>';
        if(banList.length===0){
            html+='<p style="color:var(--muted);font-size:13px;">Ma jiro user la ban-gareeyay.</p>';
        } else {
            html+='<div style="max-height:300px;overflow-y:auto;">';
            banList.forEach(function(b,i){
                html+='<div style="display:flex;justify-content:space-between;padding:8px;border-bottom:1px solid var(--border);font-size:12px;"><span><code>'+(b.key||b.serial||'N/A')+'</code>'+(b.reason?' — '+b.reason:'')+'</span><button onclick="unbanUser(\\''+(b.key||b.serial||'')+'\\')" style="background:transparent;border:none;color:var(--green);cursor:pointer;font-size:12px;"><i class="fa-solid fa-check"></i> Unban</button></div>';
            });
            html+='</div>';
        }
        html+='<div style="margin-top:15px;"><input type="text" id="ban_key" placeholder="License key ama serial" style="width:100%;padding:12px;background:var(--input-bg);border:1px solid var(--border);border-radius:10px;color:var(--text);margin-bottom:8px;">'+
        '<input type="text" id="ban_reason" placeholder="Sababta (ikhtiyaari)" style="width:100%;padding:12px;background:var(--input-bg);border:1px solid var(--border);border-radius:10px;color:var(--text);margin-bottom:8px;">'+
        '<button onclick="banUser()" style="width:100%;padding:12px;background:var(--red);border:none;border-radius:10px;color:#fff;font-weight:600;cursor:pointer;"><i class="fa-solid fa-ban"></i> Ban User</button></div>';
        html+='</div>';

        document.getElementById('loader-config-content').innerHTML=html;
    }catch(e){
        document.getElementById('loader-config-content').innerHTML='<p style="color:var(--red);">Error: '+e.message+'</p>';
    }
}

async function saveLoaderConfig(){
    try{
        var t=localStorage.getItem('token');
        var updates={
            app_version: document.getElementById('cfg_app_version').value,
            update_url: document.getElementById('cfg_update_url').value,
            update_message: document.getElementById('cfg_update_message').value,
            maintenance_message: document.getElementById('cfg_maintenance_message').value,
            game_version: document.getElementById('cfg_game_version').value,
            shizuku_mode: document.getElementById('cfg_shizuku_mode').value
        };
        var r=await fetch('/api/loader/remote-config',{method:'POST',headers:{'Authorization':'Bearer '+t,'Content-Type':'application/json'},body:JSON.stringify({updates:updates})});
        var d=await r.json();
        if(d.success){showToast('Success','Config la keydiyay!','success');}else{showToast('Error',d.error,'error');}
    }catch(e){showToast('Error',e.message,'error');}
}

async function toggleConfig(key,current){
    try{
        var t=localStorage.getItem('token');
        var updates={}; updates[key]=!current;
        var r=await fetch('/api/loader/remote-config',{method:'POST',headers:{'Authorization':'Bearer '+t,'Content-Type':'application/json'},body:JSON.stringify({updates:updates})});
        var d=await r.json();
        if(d.success){showToast('Success','La beddelay!','success');loadLoaderConfig();}
    }catch(e){showToast('Error',e.message,'error');}
}

async function banUser(){
    var key=document.getElementById('ban_key').value.trim();
    var reason=document.getElementById('ban_reason').value.trim();
    if(!key){showToast('Warning','Key ama serial geli','info');return;}
    try{
        var t=localStorage.getItem('token');
        var r=await fetch('/api/loader/ban',{method:'POST',headers:{'Authorization':'Bearer '+t,'Content-Type':'application/json'},body:JSON.stringify({key:key,reason:reason})});
        var d=await r.json();
        if(d.success){showToast('Success','User la ban-gareeyay!','success');loadLoaderConfig();}
    }catch(e){showToast('Error',e.message,'error');}
}

async function unbanUser(key){
    try{
        var t=localStorage.getItem('token');
        var r=await fetch('/api/loader/unban',{method:'POST',headers:{'Authorization':'Bearer '+t,'Content-Type':'application/json'},body:JSON.stringify({key:key})});
        var d=await r.json();
        if(d.success){showToast('Success','User la unban-gareeyay!','success');loadLoaderConfig();}
    }catch(e){showToast('Error',e.message,'error');}
}

async function loadTelegramStatus(){"""

if old_func in c:
    c = c.replace(old_func, new_func, 1)
    print("3. Functions: OK")
else:
    print("3. Functions: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_loader_config_page")
