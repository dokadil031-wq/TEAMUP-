import re

with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

if "import androidx.compose.material.icons.filled.Close" not in content:
    content = content.replace("import androidx.compose.material.icons.filled.Check", "import androidx.compose.material.icons.filled.Check\nimport androidx.compose.material.icons.filled.Close")

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
