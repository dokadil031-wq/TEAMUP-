import re

with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target = """    Column(modifier = Modifier.fillMaxSize().padding(horizontal = 22.dp, vertical = 16.dp).verticalScroll(rememberScrollState())) {"""
repl = """    Column(modifier = Modifier.fillMaxSize().padding(horizontal = 22.dp, vertical = 16.dp)) {"""

content = content.replace(target, repl)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
