with open("gradle/libs.versions.toml", "r") as f:
    content = f.read()

content = content.replace('playServicesLocation = "21.3.0"', 'playServicesLocation = "21.3.0"\nplayServicesMaps = "19.0.0"\nmapsCompose = "6.1.2"')

content = content.replace('play-services-location = { group = "com.google.android.gms", name = "play-services-location", version.ref = "playServicesLocation" }', 'play-services-location = { group = "com.google.android.gms", name = "play-services-location", version.ref = "playServicesLocation" }\nplay-services-maps = { group = "com.google.android.gms", name = "play-services-maps", version.ref = "playServicesMaps" }\nmaps-compose = { group = "com.google.maps.android", name = "maps-compose", version.ref = "mapsCompose" }')

with open("gradle/libs.versions.toml", "w") as f:
    f.write(content)
