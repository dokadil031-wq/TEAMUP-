with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """            currentScreen == "profileSetup" -> ProfileSetupScreen("""
replacement = """            currentScreen == "editProfile" -> EditProfileScreen(
                name = name,
                onNameChange = { name = it },
                age = age,
                onAgeChange = { age = it },
                gender = gender,
                onGenderChange = { gender = it },
                viewModel = viewModel,
                onBack = { currentScreen = "main" },
                onSave = {
                    viewModel.saveUserProfile(name, age, gender, selectedSports.toList())
                    currentScreen = "main"
                }
            )
            currentScreen == "profileSetup" -> ProfileSetupScreen("""
content = content.replace(target, replacement)

target_profile = '"Profile" -> ProfileScreen(viewModel, onEditProfileClick = { currentScreen = "profileSetup" }, onLogoutClick = { viewModel.auth.signOut(); currentScreen = "auth" })'
replacement_profile = '"Profile" -> ProfileScreen(viewModel, onEditProfileClick = { currentScreen = "editProfile" }, onLogoutClick = { viewModel.auth.signOut(); currentScreen = "auth" })'
content = content.replace(target_profile, replacement_profile)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
