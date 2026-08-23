with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace('keyboardOptions = KeyboardOptions', 'singleLine = true, keyboardOptions = KeyboardOptions')

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
