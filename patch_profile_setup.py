import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Add var profilePhotoBase64 in MainActivity
target_state = """    val selectedSports = remember(userSports) { mutableStateListOf(*userSports.toTypedArray()) }"""
replace_state = """    val selectedSports = remember(userSports) { mutableStateListOf(*userSports.toTypedArray()) }
    var profilePhotoBase64 by remember { mutableStateOf("") }"""
content = content.replace(target_state, replace_state)

# 2. Add photo capture requirement and saving in ProfileSetupScreen caller
target_caller = """            currentScreen == "profileSetup" -> ProfileSetupScreen(
                name = name,
                onNameChange = { name = it },
                age = age,
                onAgeChange = { age = it },
                gender = gender,
                onGenderChange = { gender = it },
                selectedSports = selectedSports,
                onToggleSport = {
                    if (selectedSports.contains(it)) selectedSports.remove(it)
                    else selectedSports.add(it)
                },
                password = setupPassword,
                onPasswordChange = { setupPassword = it },
                onBack = { currentScreen = "otp" },
                onNext = { 
                    val actualEmail = if (contact.contains("@")) contact else "$${contact}@maidan.app"
                    val actualPass = if (setupPassword.isNotBlank()) setupPassword else "maidan123"
                    viewModel.signUp(
                        email = actualEmail,
                        pass = actualPass,
                        onSuccess = {
                            viewModel.saveUserProfile(name, age, gender, selectedSports.toList())
                            if (profilePhotoBase64.isNotEmpty()) viewModel.updateProfilePhoto(profilePhotoBase64)
                            currentScreen = "main"
                        },
                        onError = {
                            // If user exists or failed, just login and proceed
                            viewModel.signIn(
                                email = actualEmail,
                                pass = actualPass,
                                onSuccess = {
                                    viewModel.saveUserProfile(name, age, gender, selectedSports.toList())
                                    if (profilePhotoBase64.isNotEmpty()) viewModel.updateProfilePhoto(profilePhotoBase64)
                                    currentScreen = "main"
                                },
                                onError = {
                                    viewModel.signInAnonymously(
                                        onSuccess = {
                                            viewModel.saveUserProfile(name, age, gender, selectedSports.toList())
                                            if (profilePhotoBase64.isNotEmpty()) viewModel.updateProfilePhoto(profilePhotoBase64)
                                            currentScreen = "main"
                                        },
                                        onError = {
                                            viewModel.saveUserProfile(name, age, gender, selectedSports.toList())
                                            if (profilePhotoBase64.isNotEmpty()) viewModel.updateProfilePhoto(profilePhotoBase64)
                                            currentScreen = "main"
                                        }
                                    )
                                }
                            )
                        }
                    )
                },
                photoBase64 = profilePhotoBase64,
                onPhotoCaptured = { profilePhotoBase64 = it }
            )"""

# I need to use regex to replace the caller because we don't know the exact current string format
pattern = r'currentScreen == "profileSetup" -> ProfileSetupScreen\([\s\S]*?onNext = \{[\s\S]*?\}[\s\S]*?\n\s*\)'

content = re.sub(pattern, target_caller, content)

# 3. Modify ProfileSetupScreen signature and add UI
target_fun = """@Composable
fun ProfileSetupScreen(
    name: String, onNameChange: (String) -> Unit,
    age: String, onAgeChange: (String) -> Unit,
    gender: String, onGenderChange: (String) -> Unit,
    selectedSports: List<String>, onToggleSport: (String) -> Unit,
    password: String = "", onPasswordChange: (String) -> Unit = {},
    onBack: () -> Unit, onNext: () -> Unit
) {"""
replace_fun = """@Composable
fun ProfileSetupScreen(
    name: String, onNameChange: (String) -> Unit,
    age: String, onAgeChange: (String) -> Unit,
    gender: String, onGenderChange: (String) -> Unit,
    selectedSports: List<String>, onToggleSport: (String) -> Unit,
    password: String = "", onPasswordChange: (String) -> Unit = {},
    onBack: () -> Unit, onNext: () -> Unit,
    photoBase64: String = "", onPhotoCaptured: (String) -> Unit = {}
) {"""
content = content.replace(target_fun, replace_fun)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
