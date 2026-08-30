import re

# 1. Fix UserPreferencesRepository
with open("app/src/main/java/com/example/UserPreferencesRepository.kt", "r") as f:
    repo = f.read()

repo = re.sub(r'    private val CITY_KEY = stringPreferencesKey\("user_city"\)\n    private val CITY_KEY = stringPreferencesKey\("user_city"\)', '    private val CITY_KEY = stringPreferencesKey("user_city")', repo)
repo = re.sub(r'    suspend fun saveUserCity\(city: String\) \{\n        dataStore.edit \{ preferences ->\n            preferences\[CITY_KEY\] = city\n        \}\n    \}\n    suspend fun saveUserCity\(city: String\) \{\n        dataStore.edit \{ preferences ->\n            preferences\[CITY_KEY\] = city\n        \}\n    \}', '    suspend fun saveUserCity(city: String) {\n        dataStore.edit { preferences ->\n            preferences[CITY_KEY] = city\n        }\n    }', repo)

with open("app/src/main/java/com/example/UserPreferencesRepository.kt", "w") as f:
    f.write(repo)

# 2. Fix MaidanViewModel (Initial Data and other duplicate saveUserCity)
with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    vm = f.read()

vm = re.sub(r'MatchEntity\("", "Sports", "Cricket", "Sunday morning cricket, need 3 more", "DLF Ground, Sector 14", "Tomorrow, 7:00 AM", 5, 8, "All", "Rahul Verma", "", 4.8\)', 'MatchEntity("", "Sports", "", "Cricket", "Sunday morning cricket, need 3 more", "DLF Ground, Sector 14", "Tomorrow, 7:00 AM", 5, 8, "All", "Rahul Verma", "", 4.8)', vm)
vm = re.sub(r'MatchEntity\("", "Sports", "Badminton", "Evening doubles, casual level", "Indoor Court, Sector 21", "Today, 6:30 PM", 2, 4, "Female", "Priya Sharma", "", 4.9\)', 'MatchEntity("", "Sports", "", "Badminton", "Evening doubles, casual level", "Indoor Court, Sector 21", "Today, 6:30 PM", 2, 4, "Female", "Priya Sharma", "", 4.9)', vm)
vm = re.sub(r'MatchEntity\("", "Sports", "Football", "5-a-side, need a keeper", "Turf Arena, Sector 29", "Sat, 5:00 PM", 8, 10, "All", "Arjun Mehta", "", 3.9\)', 'MatchEntity("", "Sports", "", "Football", "5-a-side, need a keeper", "Turf Arena, Sector 29", "Sat, 5:00 PM", 8, 10, "All", "Arjun Mehta", "", 3.9)', vm)
vm = re.sub(r'MatchEntity\("", "Online gaming", "BGMI", "Squad push, ranked grind tonight", "Online", "Today, 9:00 PM", 2, 4, "All", "Arjun Mehta", "", 3.9\)', 'MatchEntity("", "Online gaming", "", "BGMI", "Squad push, ranked grind tonight", "Online", "Today, 9:00 PM", 2, 4, "All", "Arjun Mehta", "", 3.9)', vm)
vm = re.sub(r'MatchEntity\("", "Exercise", "Running", "5K morning run, easy pace", "City Park, Gate 2", "Tomorrow, 6:00 AM", 4, 12, "All", "Sneha Kulkarni", "", 4.6\)', 'MatchEntity("", "Exercise", "", "Running", "5K morning run, easy pace", "City Park, Gate 2", "Tomorrow, 6:00 AM", 4, 12, "All", "Sneha Kulkarni", "", 4.6)', vm)

vm = re.sub(r'    fun updateUserCity\(city: String\) \{\n        viewModelScope.launch \{\n            userPrefsRepo.saveUserCity\(city\)\n        \}\n        val uid = auth.currentUser\?\.uid \?\: return\n        db.collection\("users"\).document\(uid\).update\("city", city\)\n    \}\n\n    fun updateUserCity\(city: String\) \{\n        viewModelScope.launch \{\n            userPrefsRepo.saveUserCity\(city\)\n        \}\n        val uid = auth.currentUser\?\.uid \?\: return\n        db.collection\("users"\).document\(uid\).update\("city", city\)\n    \}', '    fun updateUserCity(city: String) {\n        viewModelScope.launch {\n            userPrefsRepo.saveUserCity(city)\n        }\n        val uid = auth.currentUser?.uid ?: return\n        db.collection("users").document(uid).update("city", city)\n    }', vm)

with open("app/src/main/java/com/example/MaidanViewModel.kt", "w") as f:
    f.write(vm)

# 3. Fix MainActivity OptIn and Context
with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    main = f.read()

main = main.replace('val locationPermissions = com.google.accompanist.permissions.rememberMultiplePermissionsState(', '@OptIn(com.google.accompanist.permissions.ExperimentalPermissionsApi::class)\n    val locationPermissions = com.google.accompanist.permissions.rememberMultiplePermissionsState(')

main = main.replace('androidx.compose.runtime.LaunchedEffect(locationPermissions.allPermissionsGranted, currentScreen)', 'val contextForLocation = androidx.compose.ui.platform.LocalContext.current\n    androidx.compose.runtime.LaunchedEffect(locationPermissions.allPermissionsGranted, currentScreen)')
main = main.replace('val city = LocationHelper.getCurrentCity(context)', 'val city = LocationHelper.getCurrentCity(contextForLocation)')

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(main)

