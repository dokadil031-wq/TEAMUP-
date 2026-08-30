with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    text = f.read()

target = 'val matches by viewModel.allMatches.collectAsStateWithLifecycle()'
repl = 'val allMatches by viewModel.allMatches.collectAsStateWithLifecycle()\n    val userCity by viewModel.userCity.collectAsStateWithLifecycle()\n    val matches = allMatches.filter { it.city.equals(userCity, ignoreCase = true) || it.city.isEmpty() || userCity.isEmpty() }'

text = text.replace(target, repl)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(text)
