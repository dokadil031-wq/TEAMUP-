import re

with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target = """    val userSports by viewModel.userSports.collectAsStateWithLifecycle()
    val userImage by viewModel.userImage.collectAsStateWithLifecycle()"""

repl = """    val userSports by viewModel.userSports.collectAsStateWithLifecycle()"""

content = content.replace(target, repl)

# Also remove the invalid imports at line 62 if they were accidentally placed at the top? Wait, when did I add imports to AppScreens?
# Earlier I accidentally printed `import androidx...` before `@Composable fun PostDetailScreen` ?
# Ah, maybe they were placed at the very top of `AppScreens.kt`...
# Let's clean up any randomly placed imports in AppScreens.kt that are not at the top.

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
