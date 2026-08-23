with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target_vars = """    var selectedMatch by remember { mutableStateOf<MatchEntity?>(null) }"""
replacement_vars = target_vars + """
    var selectedRequest by remember { mutableStateOf<MatchRequest?>(null) }"""
content = content.replace(target_vars, replacement_vars)

target_nav = """                            "Messages" -> MessagesScreen()"""
replacement_nav = """                            "Messages" -> MessagesScreen(viewModel = viewModel, onChatClick = { req -> selectedRequest = req; currentScreen = "chat" })
                            "chat" -> if (selectedRequest != null) ChatScreen(request = selectedRequest!!, viewModel = viewModel, onBack = { currentScreen = "Messages" })"""
content = content.replace(target_nav, replacement_nav)

target_postdetail_nav = """onMessageClick = { currentScreen = "messages" }"""
replacement_postdetail_nav = """onMessageClick = { 
                    val req = viewModel.myRequests.value.find { it.matchId == selectedMatch!!.id } ?: viewModel.myNotifications.value.find { it.matchId == selectedMatch!!.id }
                    if (req != null) {
                        selectedRequest = req
                        currentScreen = "chat"
                    } else {
                        currentTab = "Messages"
                        currentScreen = "Messages"
                    }
                }"""
content = content.replace(target_postdetail_nav, replacement_postdetail_nav)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
