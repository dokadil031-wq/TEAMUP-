import re

def fix_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    content = content.replace("androidx.compose.ui.graphics.asImageBitmap(bitmap)", "bitmap.asImageBitmap()")
            
    with open(file_path, "w") as f:
        f.write(content)

fix_file("app/src/main/java/com/example/AppScreens.kt")
fix_file("app/src/main/java/com/example/MainActivity.kt")
