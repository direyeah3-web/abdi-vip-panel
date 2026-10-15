import shutil
import re

shutil.copy('public/index.html', 'public/index.html.backup_loader_config_js')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Raadi function-ka loadLoaderConfig oo dhan
pattern = r"async function loadLoaderConfig\(\)\{.*?\n\}"
match = re.search(pattern, c, re.DOTALL)

# Function cusub — syntax sax (double quotes onclick)
new_func = """async function loadLoaderConfig(){
    try{
        var t=localStorage.getItem('token');
        var r=await fetch('/api/loader/remote-config',{headers:{'Authorization':'Bearer '+t}});
        var d=await r.json();
        if(!d.success){document.getElementById('loader-config-content').innerHTML='<p style="color:var(--red);">Error: '+(d.error||'Unknown')+'</p>';return;}
        var cfg=d.config||{};
        var html='';

        // 1. LOADER STATE
        html+='<div class="panel" style="margin-bottom:20px;"><h3><i class="fa-solid fa-power-off" style="color:var(--green);"></i> Loader State</h3>'+
        '<div style="font-size:13px;line-height:2;">'+
        '<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border);"><span>Maintenance Mode</span>'+
        '<button data-key="maintenance_mode" data-val="'+(cfg.maintenance_mode?'true':'false')+'" onclick="toggleConfigBtn(this)" style="padding:6px 16px;border-radius:20px;border:none;cursor:pointer;background:'+(cfg.maintenance_mode?'var(--red)':'var(--green)')+';color:#fff;font-size:12px;font-weight:600;">'+(cfg.maintenance_mode?'ON':'OFF')+'</button></div>'+
        '<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border);"><span>Update Required</span>'+
        '<button data-key="update_required" data-val="'+(cfg.update_required?'true':'false')+'" onclick="toggleConfigBtn(this)" style="padding:6px 16px;border-radius:20px;border:none;cursor:pointer;background:'+(cfg.update_required?'var(--yellow)':'var(--green)')+';color:#fff;font-size:12px;font-weight:600;">'+(cfg.update_required?'ON':'OFF')+'</button></div>'+
        '<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border);"><span>Crash Fix</span>'+
        '<button data-key="crash_fix" data-val="'+(cfg.crash_fix?'true':'false')+'" onclick="toggleConfigBtn(this)" style="padding:6px 16px;border-radius:20px;border:none;cursor:pointer;background:'+(cfg.crash_fix?'var(--green)':'var(--muted)')+';color:#fff;font-size:12px;font-weight:600;">'+(cfg.crash_fix?'ON':'OFF')+'</button></div>'+
        '<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;"><span>Floating Menu</span>'+
        '<button data-key="floating_menu_enabled" data-val="'+(cfg.floating_menu_enabled?'true':'false')+'" onclick="toggleConfigBtn(this)" style="padding:6px 16px;border-radius:20px;border:none;cursor:pointer;background:'+(cfg.floating_menu_enabled?'var(--green)':'var(--muted)')+';color:#fff;font-size:12px;font-weight:600;">'+(cfg.floating_menu_enabled?'ON':'OFF')+'</button></div>'+
        '</div></div>';

        // 2. APP VERSION
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

        // 3. GAME VERSION
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

        // 4. BAN LIST
        var banList = cfg.ban_list || [];
        html+='<div class="panel"><h3><i class="fa-solid fa-ban" style="color:var(--red);"></i> Ban List ('+banList.length+')</h3>';
        if(banList.length===0){
            html+='<p style="color:var(--muted);font-size:13px;">Ma jiro user la ban-gareeyay.</p>';
        } else {
            html+='<div style="max-height:300px;overflow-y:auto;" id="ban-list-container">';
            banList.forEach(function(b){
                html+='<div style="display:flex;justify-content:space-between;padding:8px;border-bottom:1px solid var(--border);font-size:12px;"><span><code>'+(b.key||b.serial||'N/A')+'</code>'+(b.reason?' — '+b.reason:'')+'</span><button data-unban="'+(b.key||b.serial||'')+'" onclick="unbanUserBtn(this)" style="background:transparent;border:none;color:var(--green);cursor:pointer;font-size:12px;"><i class="fa-solid fa-check"></i> Unban</button></div>';
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

function toggleConfigBtn(btn){
    var key = btn.getAttribute('data-key');
    var current = btn.getAttribute('data-val') === 'true';
    toggleConfig(key, current);
}

function unbanUserBtn(btn){
    var key = btn.getAttribute('data-unban');
    unbanUser(key);
}"""

if match:
    c = c[:match.start()] + new_func + c[match.end():]
    print("1. loadLoaderConfig: OK")
else:
    print("1. loadLoaderConfig: LAMA HELIN")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_loader_config_js")
