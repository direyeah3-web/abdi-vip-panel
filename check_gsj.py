#!/usr/bin/env python3
import json, pathlib, zipfile

def inspect_gsj_file(path):
    try:
        cfg = json.loads(pathlib.Path(path).read_text())
    except Exception as e:
        return {"path": str(path), "error": str(e)}
    pi = cfg.get("project_info", {})
    clients = cfg.get("client", [])
    return {
        "path": str(path),
        "project_id": pi.get("project_id"),
        "project_number": pi.get("project_number"),
        "firebase_url": pi.get("firebase_url"),
        "storage_bucket": pi.get("storage_bucket"),
        "app_ids": [c.get("client_info", {}).get("mobilesdk_app_id") for c in clients],
        "packages": [c.get("client_info", {}).get("android_client_info", {}).get("package_name") for c in clients],
    }

def inspect_apk(apk_path):
    print(f"\n[*] APK: {apk_path}")
    try:
        with zipfile.ZipFile(apk_path) as z:
            for name in z.namelist():
                if "google-services" in name.lower() or ("res/raw" in name and name.endswith(".json")):
                    try:
                        cfg = json.loads(z.read(name))
                        pi = cfg.get("project_info", {})
                        clients = cfg.get("client", [])
                        print(f"    === {name} ===")
                        print(f"      project_id:   {pi.get('project_id')}")
                        print(f"      firebase_url: {pi.get('firebase_url')}")
                        for c in clients:
                            ci = c.get("client_info", {})
                            print(f"      app_id:  {ci.get('mobilesdk_app_id')}")
                            print(f"      pkg:     {ci.get('android_client_info', {}).get('package_name')}")
                    except Exception as e:
                        print(f"      [!] parse error {name}: {e}")
    except Exception as e:
        print(f"    [!] APK error: {e}")

def main():
    root = pathlib.Path.home() / "abdi-panel"
    print("=" * 60)
    print("  ZOON 4.6 — GSJ INSPECTOR")
    print("=" * 60)
    print("\n[1] Files on disk:")
    for p in root.rglob("google-services.json"):
        print(f"\n  >>> {p}")
        for k, v in inspect_gsj_file(p).items():
            print(f"      {k}: {v}")
    print("\n[2] APKs:")
    for apk in list(root.glob("*.apk")) + list((root / "zoon_original").glob("*.apk")):
        inspect_apk(str(apk))
    print("\n" + "=" * 60)
    print(" VERDICT")
    print("=" * 60)
    print("""
  Haddii APK-gu leeyahay google-services.json oo project_id = wolf-e99fb
  -> waa inaad ku beddeshaa tan cusub (abdi-vip-panel) gudaha res/raw/
  -> kadib dib u dhis APK-ga.

  Haddii APK-gu leeyahay google-services.json oo project_id = abdi-vip-panel
  -> APK-gu wuu saxan yahay, dhibaatadu waa:
     a) Firebase DB aan la buuxin (/aplikasi)
     b) Adapter smali oo aan si sax ah u akhrin Game fields
     c) SHA-1 fingerprint aan la xidhin Firebase Console

  Haddii APK-gu aanu lahayn google-services.json gudaha res/raw/
  -> waa inaad ku dartaa gudaha zoon_modified/res/raw/ kadib dib u dhis.
""")

if __name__ == "__main__":
    main()
