with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                    onMessageClick = {
                        val req = viewModel.myRequests.value.find { it.matchId == selectedMatch!!.id } ?: viewModel.myNotifications.value.find { it.matchId == selectedMatch!!.id }
                        if (req != null) {
                            selectedRequest = req
                            currentScreen = "chat"
                        } else {
                            currentTab = "Messages"
                            currentScreen = "main"
                        }
                    },
                    userName = name
                )"""

replacement = """                    onMessageClick = {
                        val req = viewModel.myRequests.value.find { it.matchId == selectedMatch!!.id } ?: viewModel.myNotifications.value.find { it.matchId == selectedMatch!!.id }
                        if (req != null) {
                            selectedRequest = req
                            currentScreen = "chat"
                        } else {
                            currentTab = "Messages"
                            currentScreen = "main"
                        }
                    },
                    userName = name,
                    onPosterClick = {
                        targetUserId = it
                        currentScreen = "userProfile"
                    }
                )"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
