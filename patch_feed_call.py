with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                            "Home" -> FeedScreen(viewModel, onMatchClick = { 
                                selectedMatch = it
                                currentScreen = "postDetail"
                            }, onNotificationsClick = {
                                currentScreen = "notifications"
                            })"""
replacement = """                            "Home" -> FeedScreen(viewModel, onMatchClick = { 
                                selectedMatch = it
                                currentScreen = "postDetail"
                            }, onNotificationsClick = {
                                currentScreen = "notifications"
                            }, userName = name)"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
