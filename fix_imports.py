with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

content = content.replace("import androidx.compose.ui.text.font.FontWeight\\nimport androidx.compose.ui.text.input.PasswordVisualTransformation", "import androidx.compose.ui.text.font.FontWeight")

imports = """
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.material.icons.automirrored.filled.ArrowBack
"""

content = content.replace("import androidx.compose.ui.text.font.FontWeight", "import androidx.compose.ui.text.font.FontWeight" + imports)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
