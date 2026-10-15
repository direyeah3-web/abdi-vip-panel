import shutil
import sqlite3

shutil.copy('abdi.db', 'abdi.db.backup_remote_config')

conn = sqlite3.connect('abdi.db')
cur = conn.cursor()

# Table cusub — remote config
cur.execute("""
CREATE TABLE IF NOT EXISTS loader_remote_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_key TEXT UNIQUE,
    config_value TEXT,
    config_type TEXT DEFAULT 'string',
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Config-ka default
defaults = [
    ('app_version', '4.6.0', 'string', 'App version-ka loader-ku isticmaalo'),
    ('update_required', 'false', 'boolean', 'Loader-ku update ma u baahan yahay?'),
    ('update_url', '', 'string', 'URL-ka APK-ga cusub (haddii update loo baahdo)'),
    ('update_message', 'Update cusub ayaa jira. Fadlan APK-ga cusub soo deji.', 'string', 'Fariinta update-ka'),
    ('maintenance_mode', 'false', 'boolean', 'Loader-ku ma joojisan yahay?'),
    ('maintenance_message', 'Loader-ku waa la hagaajinayaa. Fadlan 5 daqiiqo kadib dib u tijaabi.', 'string', 'Fariinta maintenance-ka'),
    ('game_version', 'GL', 'string', 'Game version-ka (GL, KR, TW, VN, BGMI)'),
    ('shizuku_mode', 'ADB Process / Rootless', 'string', 'Shizuku mode'),
    ('floating_menu_enabled', 'true', 'boolean', 'Floating menu ha shaqeeyo?'),
    ('cheat_engine_enabled', 'true', 'boolean', 'Cheat engine ha shaqeeyo?'),
    ('copy_fist_enabled', 'true', 'boolean', 'Copy FIST ha shaqeeyo?'),
    ('custom_message', '', 'string', 'Fariin gaar ah oo loader-ku soo bandhigo'),
    ('ban_list', '', 'string', 'Liiska user-ka la ban-gareeyay (JSON array)'),
    ('crash_fix', 'false', 'boolean', 'Crash fix ha shaqeeyo?')
]

for key, value, type_, desc in defaults:
    cur.execute("INSERT OR IGNORE INTO loader_remote_config (config_key, config_value, config_type, description) VALUES (?, ?, ?, ?)",
                [key, value, type_, desc])

conn.commit()
conn.close()
print("✅ Table loader_remote_config la abuuray + config default")
