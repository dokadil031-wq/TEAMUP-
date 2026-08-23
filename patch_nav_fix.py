with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                            "chat" -> if (selectedRequest != null) ChatScreen(request = selectedRequest!!, viewModel = viewModel, onBack = { currentScreen = "Messages" })
                            "Profile" -> ProfileScreen"""
replacement = """                            "Profile" -> ProfileScreen"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
