with open("app/src/main/AndroidManifest.xml", "r") as f:
    content = f.read()

target = """    <application"""
replace = """    <uses-feature android:name="android.hardware.camera" android:required="true" />
    <uses-permission android:name="android.permission.CAMERA" />

    <application"""
content = content.replace(target, replace)

with open("app/src/main/AndroidManifest.xml", "w") as f:
    f.write(content)
