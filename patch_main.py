import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                            "Profile" -> ProfileScreen(viewModel, onEditProfileClick = { currentScreen = "editProfile" }, onLogoutClick = { viewModel.auth.signOut(); currentScreen = "auth" })
                            "userProfile" -> if (targetUserId != null) UserProfileScreen(targetUserId = targetUserId!!, viewModel = viewModel, onBack = { currentScreen = "main" })
                        }
                    }"""

replacement = """                            "Profile" -> ProfileScreen(viewModel, onEditProfileClick = { currentScreen = "editProfile" }, onLogoutClick = { viewModel.auth.signOut(); currentScreen = "auth" })
                        }
                    }"""

content = content.replace(target, replacement)

target2 = """            currentScreen == "main" -> {"""

replacement2 = """            currentScreen == "userProfile" && targetUserId != null -> {
                UserProfileScreen(targetUserId = targetUserId!!, viewModel = viewModel, onBack = { currentScreen = "main" })
            }
            currentScreen == "main" -> {"""

content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
