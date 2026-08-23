with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """            currentScreen == "notifications" -> NotificationsScreen(onBack = { currentScreen = "main" })"""
replacement = """            currentScreen == "notifications" -> NotificationsScreen(viewModel = viewModel, onBack = { currentScreen = "main" })"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
