with open("app/src/main/java/com/example/UserPreferencesRepository.kt", "r") as f:
    text = f.read()

text = text.replace('private val IMAGE_KEY = stringPreferencesKey("user_image")', 'private val IMAGE_KEY = stringPreferencesKey("user_image")\n    private val CITY_KEY = stringPreferencesKey("user_city")')

text = text.replace('val userImage: Flow<String> = dataStore.data.map {\n        preferences[IMAGE_KEY] ?: ""\n    }', 'val userImage: Flow<String> = dataStore.data.map {\n        preferences[IMAGE_KEY] ?: ""\n    }\n\n    val userCity: Flow<String> = dataStore.data.map {\n        preferences[CITY_KEY] ?: ""\n    }')

text = text.replace('suspend fun saveUserImage(base64: String) {\n        dataStore.edit { preferences ->\n            preferences[IMAGE_KEY] = base64\n        }\n    }', 'suspend fun saveUserImage(base64: String) {\n        dataStore.edit { preferences ->\n            preferences[IMAGE_KEY] = base64\n        }\n    }\n\n    suspend fun saveUserCity(city: String) {\n        dataStore.edit { preferences ->\n            preferences[CITY_KEY] = city\n        }\n    }')

with open("app/src/main/java/com/example/UserPreferencesRepository.kt", "w") as f:
    f.write(text)
