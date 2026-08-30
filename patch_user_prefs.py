import re

with open("app/src/main/java/com/example/UserPreferencesRepository.kt", "r") as f:
    content = f.read()

clear_func = """    suspend fun saveUserImage(base64: String) {
        dataStore.edit { preferences ->
            preferences[IMAGE_KEY] = base64
        }
    }
    
    suspend fun clearProfile() {
        dataStore.edit { preferences ->
            preferences.clear()
        }
    }"""

content = content.replace("""    suspend fun saveUserImage(base64: String) {
        dataStore.edit { preferences ->
            preferences[IMAGE_KEY] = base64
        }
    }""", clear_func)

with open("app/src/main/java/com/example/UserPreferencesRepository.kt", "w") as f:
    f.write(content)
