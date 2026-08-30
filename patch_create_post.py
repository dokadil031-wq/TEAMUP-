import re

with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target = """    val userName by viewModel.userName.collectAsStateWithLifecycle()"""
repl = """    val userName by viewModel.userName.collectAsStateWithLifecycle()
    val userImage by viewModel.userImage.collectAsStateWithLifecycle()"""
content = content.replace(target, repl)

target_match = """                    posterName = if (userName.isNotEmpty()) userName else "You",
                    posterTrust = 0.0,
                    timestamp = matchTimestamp
                )"""
repl_match = """                    posterName = if (userName.isNotEmpty()) userName else "You",
                    posterTrust = 0.0,
                    timestamp = matchTimestamp,
                    posterImageBase64 = userImage
                )"""
content = content.replace(target_match, repl_match)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
