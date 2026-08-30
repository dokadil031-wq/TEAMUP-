with open("app/src/main/java/com/example/Models.kt", "r") as f:
    text = f.read()

text = text.replace('val profileImageBase64: String = ""', 'val profileImageBase64: String = "",\n    val city: String = ""')

with open("app/src/main/java/com/example/Models.kt", "w") as f:
    f.write(text)
