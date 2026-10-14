import zipfile
import re
import os
import sys

# Isticmaal folder-ka guriga
work_dir = os.path.expanduser('~/apk_tmp')
os.makedirs(work_dir, exist_ok=True)

# Raadi APK
apk_files = [f for f in os.listdir(work_dir) if f.endswith('.apk')]
if not apk_files:
    # Raadi /storage/emulated/0/Download/Telegram
    download_dir = '/storage/emulated/0/Download/Telegram'
    if os.path.exists(download_dir):
        for f in os.listdir(download_dir):
            if f.endswith('.apk'):
                apk_files.append(f)
                import shutil
                shutil.copy(os.path.join(download_dir, f), work_dir)
                print(f"✅ APK la soo qaaday: {f}")
        if not apk_files:
            print("❌ APK ma jiro. Soo geli:")
            print("   cp /storage/emulated/0/Download/Telegram/GameBlaster*.apk ~/apk_tmp/")
            sys.exit(1)
    else:
        print("❌ APK ma jiro. Soo geli:")
        print("   cp <apk_path> ~/apk_tmp/")
        sys.exit(1)

apk_path = os.path.join(work_dir, apk_files[-1])
print(f"📦 APK: {apk_path}")

# Fur APK-ga
with zipfile.ZipFile(apk_path, 'r') as z:
    dex_files = [n for n in z.namelist() if n.endswith('.dex')]
    so_files = [n for n in z.namelist() if n.endswith('.so')]
    print(f"📄 DEX files: {dex_files}")
    print(f"⚙️  .so files: {so_files}")

    for dex_name in dex_files:
        print(f"\n===== {dex_name} =====")
        data = z.read(dex_name)
        text = data.decode('latin1', errors='ignore')

        classes = re.findall(r'Lcom/[a-zA-Z0-9_/]+;', text)
        unique_classes = sorted(set(classes))
        print(f"\n📋 Classes ({len(unique_classes)}):")
        for cls in unique_classes[:50]:
            print(f"  {cls}")

        urls = re.findall(r'https?://[a-zA-Z0-9._\-/~:?#@!$&\'()*+,;=%]+', text)
        urls = [u for u in urls if not u.endswith(('.', '/'))]
        unique_urls = sorted(set(urls))
        print(f"\n🔗 URLs ({len(unique_urls)}):")
        for u in unique_urls:
            print(f"  {u}")

        license_kw = ['PanelLicense', 'BuildSeal', 'LoginActivity', 'statusTrue', 'performLogin', 'getConfigKey', 'getDailyToken', 'nativeEnforce', 'GetKey', 'FixCrash']
        print(f"\n🔑 License keywords:")
        for kw in license_kw:
            count = text.count(kw)
            if count > 0:
                print(f"  {kw}: {count} hit(s)")

    for so_name in so_files:
        print(f"\n===== {so_name} =====")
        data = z.read(so_name)
        text = data.decode('latin1', errors='ignore')

        jni = re.findall(r'Java_[a-zA-Z0-9_]+', text)
        unique_jni = sorted(set(jni))
        print(f"\n⚙️  JNI exports ({len(unique_jni)}):")
        for j in unique_jni[:30]:
            print(f"  {j}")

        urls = re.findall(r'https?://[a-zA-Z0-9._\-/~:?#@!$&\'()*+,;=%]+', text)
        urls = [u for u in urls if not u.endswith(('.', '/')) and '%s' not in u]
        unique_urls = sorted(set(urls))
        print(f"\n🔗 URLs ({len(unique_urls)}):")
        for u in unique_urls[:20]:
            print(f"  {u}")
