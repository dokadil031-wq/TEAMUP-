import re

with open("app/build.gradle.kts", "r") as f:
    text = f.read()

text = text.replace("signingConfig = signingConfigs.getByName(\"release\")", "signingConfig = signingConfigs.getByName(\"debugConfig\")")

with open("app/build.gradle.kts", "w") as f:
    f.write(text)

