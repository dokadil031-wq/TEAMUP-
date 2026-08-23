with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

content = content.replace("import androidx.compose.ui.text.font.FontWeight", "import androidx.compose.ui.text.font.FontWeight\\nimport androidx.compose.ui.text.input.PasswordVisualTransformation")

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
