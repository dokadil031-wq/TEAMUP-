import re
with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    content = f.read()

# find all indices of "private fun listenToMatches()"
matches = [m.start() for m in re.finditer(r"private fun listenToMatches\(\) \{", content)]
print(matches)
