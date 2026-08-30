import re

with open("app/src/main/AndroidManifest.xml", "r") as f:
    text = f.read()

permissions = """    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
    <uses-feature android:name="android.hardware.camera" android:required="true" />"""

text = text.replace('    <uses-feature android:name="android.hardware.camera" android:required="true" />', permissions)

with open("app/src/main/AndroidManifest.xml", "w") as f:
    f.write(text)
