import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """        Row(modifier = Modifier.padding(start = 18.dp, top = 14.dp, end = 18.dp, bottom = 10.dp).clickable { onPosterClick?.invoke() }, verticalAlignment = Alignment.CenterVertically) {"""

replacement = """        Row(modifier = Modifier.fillMaxWidth().clickable { onPosterClick?.invoke() }.padding(start = 18.dp, top = 14.dp, end = 18.dp, bottom = 10.dp), verticalAlignment = Alignment.CenterVertically) {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
