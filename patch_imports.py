import re

def fix_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    imports = [
        "import androidx.compose.ui.graphics.asImageBitmap",
        "import androidx.compose.foundation.Image",
        "import androidx.compose.ui.layout.ContentScale",
        "import android.util.Base64",
        "import android.graphics.BitmapFactory"
    ]
    
    for imp in imports:
        if imp not in content:
            content = content.replace("import androidx.compose.runtime.*", f"import androidx.compose.runtime.*\n{imp}")
            
    with open(file_path, "w") as f:
        f.write(content)

fix_file("app/src/main/java/com/example/AppScreens.kt")
fix_file("app/src/main/java/com/example/MainActivity.kt")
