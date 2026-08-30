import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

if "import android.graphics.BitmapFactory" not in content:
    content = content.replace("import android.os.Bundle", "import android.os.Bundle\nimport android.graphics.BitmapFactory\nimport android.util.Base64")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
