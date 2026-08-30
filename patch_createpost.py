with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    text = f.read()

target1 = 'val userImage by viewModel.userImage.collectAsStateWithLifecycle()'
repl1 = 'val userImage by viewModel.userImage.collectAsStateWithLifecycle()\n    val userCity by viewModel.userCity.collectAsStateWithLifecycle()'
text = text.replace(target1, repl1)

target2 = 'category = category,\n                    sport = sport,'
repl2 = 'category = category,\n                    city = userCity,\n                    sport = sport,'
text = text.replace(target2, repl2)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(text)
