import re
with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Let's use regex to strip all trailing non-alphanumeric except braces, but wait, let's just find `@Composable` near the end and truncate.
last_composable = content.rfind("@Composable")
# If it's very close to the end, truncate it.
if len(content) - last_composable < 50:
    content = content[:last_composable].strip() + "\n"

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
