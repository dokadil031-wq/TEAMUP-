with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

content = content.replace("location.isNotEmpty() && time.isNotEmpty()", "location.isNotEmpty() && dateStr.isNotEmpty() && timeStr.isNotEmpty()")

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
