import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """    selectedSports: List<String>, onToggleSport: (String) -> Unit,
    password: String = "", onPasswordChange: (String) -> Unit = {},
    onBack: () -> Unit, onNext: () -> Unit
)"""
replacement = """    selectedSports: List<String>, onToggleSport: (String) -> Unit,
    onBack: () -> Unit, onNext: () -> Unit
)"""
if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
        f.write(content)
    print("Success")
else:
    print("Not found")

