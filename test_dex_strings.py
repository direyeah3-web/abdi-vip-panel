import subprocess
import os

apk_path = '/tmp/apk_analysis_test.apk'

# Soo qaado APK-ga
print("APK path:", apk_path)
print("Ma jiro?" , not os.path.exists(apk_path))
