with open("app/build.gradle.kts", "r") as f:
    content = f.read()

content = content.replace('implementation(libs.play.services.location)', 'implementation(libs.play.services.location)\n    implementation(libs.play.services.maps)\n    implementation(libs.maps.compose)')

with open("app/build.gradle.kts", "w") as f:
    f.write(content)
