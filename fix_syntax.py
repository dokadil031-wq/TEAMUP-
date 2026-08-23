import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# I will find currentScreen == "profileSetup" -> ProfileSetupScreen( and replace until currentScreen == "postDetail"
start_idx = content.find('            currentScreen == "profileSetup" -> ProfileSetupScreen(')
end_idx = content.find('            currentScreen == "postDetail" && selectedMatch != null -> {')

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
            )
"""

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + target_caller + content[end_idx:]

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
