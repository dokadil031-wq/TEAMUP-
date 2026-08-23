with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target_vars = """    var selectedRequest by remember { mutableStateOf<MatchRequest?>(null) }"""
replacement_vars = target_vars + """
    var targetUserId by remember { mutableStateOf<String?>(null) }"""
content = content.replace(target_vars, replacement_vars)

target_nav = """                            "Profile" -> ProfileScreen(viewModel, onEditProfileClick = { currentScreen = "editProfile" }, onLogoutClick = { viewModel.auth.signOut(); currentScreen = "auth" })
                        }"""
replacement_nav = """                            "Profile" -> ProfileScreen(viewModel, onEditProfileClick = { currentScreen = "editProfile" }, onLogoutClick = { viewModel.auth.signOut(); currentScreen = "auth" })
                            "userProfile" -> if (targetUserId != null) UserProfileScreen(targetUserId = targetUserId!!, viewModel = viewModel, onBack = { currentScreen = "main" })
                        }"""
content = content.replace(target_nav, replacement_nav)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
