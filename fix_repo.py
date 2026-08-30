with open("app/src/main/java/com/example/UserPreferencesRepository.kt", "r") as f:
    text = f.read()

# Remove the second saveUserCity block
text = text.replace('    suspend fun saveUserCity(city: String) {\n        dataStore.edit { preferences ->\n            preferences[CITY_KEY] = city\n        }\n    }\n    suspend fun saveUserCity(city: String) {\n        dataStore.edit { preferences ->\n            preferences[CITY_KEY] = city\n        }\n    }', '    suspend fun saveUserCity(city: String) {\n        dataStore.edit { preferences ->\n            preferences[CITY_KEY] = city\n        }\n    }')

# Check for userCity flow
if 'val userCity: Flow<String>' not in text:
    target = '    val userImage: Flow<String> = dataStore.data.map {\n        preferences[IMAGE_KEY] ?: ""\n    }'
    repl = '    val userImage: Flow<String> = dataStore.data.map {\n        preferences[IMAGE_KEY] ?: ""\n    }\n\n    val userCity: Flow<String> = dataStore.data.map {\n        preferences[CITY_KEY] ?: ""\n    }'
    text = text.replace(target, repl)

with open("app/src/main/java/com/example/UserPreferencesRepository.kt", "w") as f:
    f.write(text)
