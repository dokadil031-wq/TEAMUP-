import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Fix imports
imports_to_add = """
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.foundation.Image
"""
if "import androidx.compose.foundation.verticalScroll" not in content:
    content = content.replace("import androidx.compose.ui.unit.sp", "import androidx.compose.ui.unit.sp" + imports_to_add)

# There is a stray `@Composable` at the end of ProfileSetupScreen because of my replacement:
# `    }\n}\n@Composable\n`
# Let's clean it up.
content = content.replace("}\n@Composable\n@Composable\nfun AuthScreen", "}\n\n@Composable\nfun AuthScreen")
content = content.replace("}\n}\n@Composable\n\n@Composable\nfun StepDots", "}\n\n@Composable\nfun StepDots")
content = content.replace("}\n@Composable\n\n@Composable\nfun StepDots", "}\n\n@Composable\nfun StepDots")
# just remove `@Composable` before `@Composable`
content = re.sub(r"@Composable\s+@Composable", "@Composable", content)
content = re.sub(r"@Composable\s+$", "", content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
