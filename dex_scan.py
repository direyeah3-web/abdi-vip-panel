#!/usr/bin/env python3
import re, pathlib, sys

OLD_APP = b"183662681739"
NEW_APP = b"375479493350"
OLD_PROJ = b"wolf-e99fb"
NEW_PROJ = b"abdi-vip-panel"

def scan_dex(path):
    data = path.read_bytes()
    return {
        "old_app_id":  len(re.findall(re.escape(OLD_APP), data)),
        "new_app_id":  len(re.findall(re.escape(NEW_APP), data)),
        "old_project": len(re.findall(re.escape(OLD_PROJ), data)),
        "new_project": len(re.findall(re.escape(NEW_PROJ), data)),
        "old_app_utf16": len(re.findall(re.escape(OLD_APP.decode().encode("utf-16-le")), data)),
        "new_app_utf16": len(re.findall(re.escape(NEW_APP.decode().encode("utf-16-le")), data)),
    }

def main(root):
    base = pathlib.Path(root)
    dexes = sorted(base.glob("classes*.dex"))
    if not dexes:
        print("[!] No classes*.dex in", base)
        sys.exit(1)
    grand = {k: 0 for k in ["old_app_id","new_app_id","old_project","new_project","old_app_utf16","new_app_utf16"]}
    for d in dexes:
        h = scan_dex(d)
        print(f"\n=== {d.name} ({d.stat().st_size:,} bytes) ===")
        for k, v in h.items():
            print(f"  {k:18s}: {v}")
            grand[k] += v
    print("\n" + "=" * 50)
    print("TOTAL:")
    for k, v in grand.items():
        print(f"  {k:18s}: {v}")
    print("\nVERDICT:")
    if grand["old_app_id"] or grand["old_app_utf16"] or grand["old_project"]:
        print("  >>> wolf-e99fb references FOUND — dex patch needed")
    elif grand["new_app_id"] or grand["new_app_utf16"] or grand["new_project"]:
        print("  >>> abdi-vip-panel references FOUND — dex is correct")
    else:
        print("  >>> no Firebase IDs hardcoded in dex — reads from res/raw/google-services.json")
        print("      -> Replace that file and rebuild APK")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
