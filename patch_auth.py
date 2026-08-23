import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target_init = 'var currentScreen by remember { mutableStateOf("auth") }'
replacement_init = 'var currentScreen by remember { mutableStateOf(if (viewModel.auth.currentUser != null) "main" else "auth") }'
content = content.replace(target_init, replacement_init)

target_profile = '"Profile" -> ProfileScreen(viewModel, onEditProfileClick = { currentScreen = "profileSetup" })'
replacement_profile = '"Profile" -> ProfileScreen(viewModel, onEditProfileClick = { currentScreen = "profileSetup" }, onLogoutClick = { viewModel.auth.signOut(); currentScreen = "auth" })'
content = content.replace(target_profile, replacement_profile)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
