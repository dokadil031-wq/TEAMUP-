import re

with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    content = f.read()

target = """    init {
        listenToMatches()
    }"""
replacement = """    init {
        auth.firebaseAuthSettings.setAppVerificationDisabledForTesting(true)
        listenToMatches()
    }"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MaidanViewModel.kt", "w") as f:
    f.write(content)
