with open("app/build.gradle.kts", "r") as f:
    text = f.read()

text = text.replace('implementation(libs.kotlinx.coroutines.core)', 'implementation(libs.kotlinx.coroutines.core)\n  implementation("org.jetbrains.kotlinx:kotlinx-coroutines-play-services:1.7.3")')

with open("app/build.gradle.kts", "w") as f:
    f.write(text)
