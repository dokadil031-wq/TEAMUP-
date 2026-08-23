with open("app/src/main/AndroidManifest.xml", "r") as f:
    content = f.read()

target = """        <meta-data
            android:name="com.google.android.geo.API_KEY"
            android:value="${MAPS_API_KEY}" />
    </application>"""
replacement = """    </application>"""
content = content.replace(target, replacement)

with open("app/src/main/AndroidManifest.xml", "w") as f:
    f.write(content)
