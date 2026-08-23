with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """fun MatchCard(m: MatchEntity, onClick: () -> Unit, onJoinClick: (() -> Unit)? = null, currentStatus: String = "none") {"""
replacement = """fun MatchCard(m: MatchEntity, onClick: () -> Unit, onJoinClick: (() -> Unit)? = null, currentStatus: String = "none", onPosterClick: (() -> Unit)? = null) {"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

