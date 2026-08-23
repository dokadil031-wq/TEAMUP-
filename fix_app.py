import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                password = setupPassword,
                onPasswordChange = { setupPassword = it },"""
content = content.replace(target, "")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
print("Removed password arg")
