import re
with open("gradle/libs.versions.toml", "r") as f:
    content = f.read()

content = re.sub(r"playServicesMaps = \"19\.0\.0\"\n", "", content)
content = re.sub(r"mapsCompose = \"6\.1\.2\"\n", "", content)
content = re.sub(r"play-services-maps = \{ group = \"com\.google\.android\.gms\", name = \"play-services-maps\", version\.ref = \"playServicesMaps\" \}\n", "", content)
content = re.sub(r"maps-compose = \{ group = \"com\.google\.maps\.android\", name = \"maps-compose\", version\.ref = \"mapsCompose\" \}\n", "", content)

with open("gradle/libs.versions.toml", "w") as f:
    f.write(content)
