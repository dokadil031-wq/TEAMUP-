with open("app/src/main/java/com/example/MatchEntity.kt", "r") as f:
    content = f.read()

target = """    val posterTrust: Double = 0.0,
    val lat: Double = 0.0,
    val lng: Double = 0.0
)"""
replacement = """    val posterTrust: Double = 0.0
)"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MatchEntity.kt", "w") as f:
    f.write(content)
