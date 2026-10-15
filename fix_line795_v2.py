import shutil
import re

shutil.copy('public/index.html', 'public/index.html.backup_line795_v2')

with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Raadi dhammaan meelaha onclick='...' ee ku jira c.innerHTML strings
# Beddel onclick='xxx' → onclick="xxx"
pattern = r"onclick='([^']+)'"

def replace_onclick(m):
    return 'onclick="' + m.group(1) + '"'

# Beddel — laakiin kaliya kuwa ku jira c.innerHTML (line 795)
# Waxaan u baahanahay in aan helo line 795 oo dhan
lines = c.split('\n')
for i, line in enumerate(lines):
    if 'p===\'loader-config\'' in line:
        # Line 795 oo dhan — beddel onclick=' → onclick="
        lines[i] = re.sub(r"onclick='([^']+)'", r'onclick="\1"', line)
        print(f"1. Line {i+1} (loader-config): OK")
        break
else:
    print("1. Line: LAMA HELIN")

c = '\n'.join(lines)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: public/index.html.backup_line795_v2")
