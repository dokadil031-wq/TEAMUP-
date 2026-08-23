with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """            currentScreen == "editProfile" -> EditProfileScreen(
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
            )"""

replacement = """            currentScreen == "editProfile" -> EditProfileScreen(
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
                viewModel = viewModel,
                onBack = { currentScreen = "main" },
                onSave = {
                    viewModel.saveUserProfile(name, age, gender, selectedSports.toList())
                    currentScreen = "main"
                }
            )"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
