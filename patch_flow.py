with open("app/src/main/java/com/example/UserPreferencesRepository.kt", "r") as f:
    text = f.read()

target = '    val userImage: Flow<String> = dataStore.data.map {\n        preferences[IMAGE_KEY] ?: ""\n    }'
repl = '    val userImage: Flow<String> = dataStore.data.map {\n        preferences[IMAGE_KEY] ?: ""\n    }\n\n    val userCity: Flow<String> = dataStore.data.map {\n        preferences[CITY_KEY] ?: ""\n    }'

text = text.replace(target, repl)

with open("app/src/main/java/com/example/UserPreferencesRepository.kt", "w") as f:
    f.write(text)
