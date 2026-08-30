import re

with open("app/src/main/java/com/example/MatchEntity.kt", "r") as f:
    content = f.read()

target = """    val posterTrust: Double = 0.0,
    val timestamp: Long = 0L,
    val fullAtTimestamp: Long? = null"""
    
repl = """    val posterTrust: Double = 0.0,
    val timestamp: Long = 0L,
    val fullAtTimestamp: Long? = null,
    val posterImageBase64: String = \"\""""

content = content.replace(target, repl)

with open("app/src/main/java/com/example/MatchEntity.kt", "w") as f:
    f.write(content)
