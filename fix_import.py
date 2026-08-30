import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    text = f.read()

if "import kotlinx.coroutines.launch" not in text:
    text = text.replace("import android.os.Bundle", "import android.os.Bundle\nimport kotlinx.coroutines.launch")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(text)

