with open("app/src/main/java/com/example/UserPreferencesRepository.kt", "r") as f:
    content = f.read()

target1 = """    private val SPORTS_KEY = stringPreferencesKey("user_sports")"""
replacement1 = """    private val SPORTS_KEY = stringPreferencesKey("user_sports")
    private val IMAGE_KEY = stringPreferencesKey("user_image")"""

target2 = """    val userSports: Flow<List<String>> = dataStore.data.map { preferences ->
        val sportsString = preferences[SPORTS_KEY] ?: ""
        if (sportsString.isEmpty()) emptyList() else sportsString.split(",")
    }"""
replacement2 = """    val userSports: Flow<List<String>> = dataStore.data.map { preferences ->
        val sportsString = preferences[SPORTS_KEY] ?: ""
        if (sportsString.isEmpty()) emptyList() else sportsString.split(",")
    }
    
    val userImage: Flow<String> = dataStore.data.map { preferences ->
        preferences[IMAGE_KEY] ?: ""
    }"""

target3 = """    suspend fun saveUserProfile(name: String, age: String, gender: String, sports: List<String>) {
        dataStore.edit { preferences ->
            preferences[NAME_KEY] = name
            preferences[AGE_KEY] = age
            preferences[GENDER_KEY] = gender
            preferences[SPORTS_KEY] = sports.joinToString(",")
        }
    }"""
replacement3 = """    suspend fun saveUserProfile(name: String, age: String, gender: String, sports: List<String>) {
        dataStore.edit { preferences ->
            preferences[NAME_KEY] = name
            preferences[AGE_KEY] = age
            preferences[GENDER_KEY] = gender
            preferences[SPORTS_KEY] = sports.joinToString(",")
        }
    }
    
    suspend fun saveUserImage(base64: String) {
        dataStore.edit { preferences ->
            preferences[IMAGE_KEY] = base64
        }
    }"""

content = content.replace(target1, replacement1)
content = content.replace(target2, replacement2)
content = content.replace(target3, replacement3)

with open("app/src/main/java/com/example/UserPreferencesRepository.kt", "w") as f:
    f.write(content)
