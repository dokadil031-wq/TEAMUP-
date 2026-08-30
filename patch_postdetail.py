import re

with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target = """        Row(modifier = Modifier.padding(bottom = 18.dp), verticalAlignment = Alignment.CenterVertically) {"""

replacement = """        Row(modifier = Modifier.fillMaxWidth().clickable { if (match.posterId.isNotEmpty()) onPosterClick(match.posterId) }.padding(bottom = 18.dp, top = 8.dp), verticalAlignment = Alignment.CenterVertically) {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
