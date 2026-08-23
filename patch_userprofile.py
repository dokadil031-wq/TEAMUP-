with open("app/src/main/java/com/example/UserProfileScreen.kt", "r") as f:
    content = f.read()

content = content.replace("import kotlinx.coroutines.flow.collectAsState", "import androidx.lifecycle.compose.collectAsStateWithLifecycle")
content = content.replace("collectAsState(initial = \"\")", "collectAsStateWithLifecycle()")

with open("app/src/main/java/com/example/UserProfileScreen.kt", "w") as f:
    f.write(content)
