with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target_postdetail = """            currentScreen == "postDetail" && selectedMatch != null -> {
                PostDetailScreen(
                    match = selectedMatch!!,
                    viewModel = viewModel,
                    onBack = { currentScreen = "main" },
                    onMessageClick = {
                        currentTab = "Messages"
                        currentScreen = "main"
                    }
                )
            }"""

replacement_postdetail = """            currentScreen == "postDetail" && selectedMatch != null -> {
                PostDetailScreen(
                    match = selectedMatch!!,
                    viewModel = viewModel,
                    onBack = { currentScreen = "main" },
                    onMessageClick = {
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
                )
            }"""
content = content.replace(target_postdetail, replacement_postdetail)

target_notif = """            currentScreen == "notifications" -> {
                NotificationsScreen(onBack = { currentScreen = "main" })
            }"""
replacement_notif = """            currentScreen == "notifications" -> {
                NotificationsScreen(viewModel = viewModel, onBack = { currentScreen = "main" })
            }"""
content = content.replace(target_notif, replacement_notif)

target_chat = """            currentScreen == "main" -> {"""
replacement_chat = """            currentScreen == "chat" && selectedRequest != null -> {
                ChatScreen(request = selectedRequest!!, viewModel = viewModel, onBack = { currentScreen = "main" })
            }
            currentScreen == "main" -> {"""
content = content.replace(target_chat, replacement_chat)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

