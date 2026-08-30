with open("app/src/main/java/com/example/MatchEntity.kt", "r") as f:
    text = f.read()

text = text.replace('val category: String = "",', 'val category: String = "",\n    val city: String = "",')

with open("app/src/main/java/com/example/MatchEntity.kt", "w") as f:
    f.write(text)
