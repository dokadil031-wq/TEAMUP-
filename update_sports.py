import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = 'val sportsList = listOf("Cricket", "Football", "Badminton", "Basketball", "Volleyball", "Table tennis", "Running", "Gym")'
replacement = 'val sportsList = listOf("Cricket", "Football", "Badminton", "Basketball", "Volleyball", "Table tennis", "Running", "Gym", "Online gaming")'

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
        f.write(content)
    print("Success")
else:
    print("Not found")

