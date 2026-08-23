import re
with open("app/build.gradle.kts", "r") as f:
    content = f.read()

content = re.sub(r"[ \t]*implementation\(libs\.play\.services\.maps\)\n", "", content)
content = re.sub(r"[ \t]*implementation\(libs\.maps\.compose\)\n", "", content)

with open("app/build.gradle.kts", "w") as f:
    f.write(content)
