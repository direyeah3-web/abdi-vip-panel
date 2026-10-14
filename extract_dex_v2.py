import zipfile
import re
import os

work_dir = os.path.expanduser('~/apk_tmp')
apk_files = [f for f in os.listdir(work_dir) if f.endswith('.apk')]
apk_path = os.path.join(work_dir, apk_files[-1])
print(f"📦 APK: {apk_path}")

with zipfile.ZipFile(apk_path, 'r') as z:
    # Dhammaan DEX files
    dex_files = sorted([n for n in z.namelist() if n.endswith('.dex')])
    print(f"📄 DEX files: {dex_files}")

    all_classes = set()
    all_urls = set()
    all_methods = set()

    for dex_name in dex_files:
        data = z.read(dex_name)
        text = data.decode('latin1', errors='ignore')

        # Classes
        classes = re.findall(r'Lcom/[a-zA-Z0-9_$]+(?:/[a-zA-Z0-9_$]+)+;', text)
        for c in classes:
            all_classes.add(c)

        # Methods
        methods = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]{2,40}\(', text)
        for m in methods:
            all_methods.add(m)

        # URLs (ka saar google/curl/github useless)
        urls = re.findall(r'https?://[a-zA-Z0-9._\-/~:?#@!$&\'()*+,;=%]+', text)
        for u in urls:
            if any(h in u for h in ['schemas.android.com', 'crbug.com', 'curl.se', 'llvm.org', 'DeNA', 'googleapis.com', 'android.googlesource.com', 'play.google.com', 'github.com']):
                continue
            if '%s' in u or '%d' in u:
                continue
            if u.endswith(('.', '/', ',')):
                continue
            all_urls.add(u)

    # Print dhammaan classes
    print(f"\n📋 Classes ({len(all_classes)}):")
    for c in sorted(all_classes):
        print(f"  {c}")

    # Print dhammaan URLs
    print(f"\n🔗 URLs ({len(all_urls)}):")
    for u in sorted(all_urls):
        print(f"  {u}")

    # Print license/panel classes
    print(f"\n🔑 License/Panel classes:")
    for c in sorted(all_classes):
        if any(k in c for k in ['License', 'Login', 'Panel', 'BuildSeal', 'Auth', 'Verify', 'Seal', 'Activation']):
            print(f"  {c}")
