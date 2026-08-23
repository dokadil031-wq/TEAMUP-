with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target_feed = """fun FeedScreen(viewModel: MaidanViewModel, onMatchClick: (MatchEntity) -> Unit, onNotificationsClick: () -> Unit) {
    val matches by viewModel.allMatches.collectAsStateWithLifecycle()"""
replacement_feed = """fun FeedScreen(viewModel: MaidanViewModel, onMatchClick: (MatchEntity) -> Unit, onNotificationsClick: () -> Unit, userName: String) {
    val matches by viewModel.allMatches.collectAsStateWithLifecycle()
    val myRequests by viewModel.myRequests.collectAsStateWithLifecycle()
    val uid = viewModel.auth.currentUser?.uid"""
content = content.replace(target_feed, replacement_feed)

target_item = """            items(filtered) { match ->
                MatchCard(match, onClick = { onMatchClick(match) }, onJoinClick = { viewModel.joinMatch(match) })
            }"""
replacement_item = """            items(filtered) { match ->
                val req = myRequests.find { it.matchId == match.id }
                val status = if (match.posterId == uid) "mine" else req?.status ?: "none"
                MatchCard(
                    m = match, 
                    onClick = { onMatchClick(match) }, 
                    onJoinClick = { viewModel.requestToJoinMatch(match, userName) },
                    currentStatus = status
                )
            }"""
content = content.replace(target_item, replacement_item)

target_carddef = """fun MatchCard(m: MatchEntity, onClick: () -> Unit, onJoinClick: (() -> Unit)? = null) {
    var requestStatus by remember(m.id) { mutableStateOf("none") }"""
replacement_carddef = """fun MatchCard(m: MatchEntity, onClick: () -> Unit, onJoinClick: (() -> Unit)? = null, currentStatus: String = "none") {"""
content = content.replace(target_carddef, replacement_carddef)

target_card_btn_cond = """            if (requestStatus == "none") {"""
replacement_card_btn_cond = """            if (currentStatus == "mine") {
                Button(
                    onClick = { },
                    colors = ButtonDefaults.buttonColors(containerColor = Turf2, contentColor = Bench),
                    shape = RoundedCornerShape(20.dp),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    modifier = Modifier.height(32.dp)
                ) {
                    Text("My Post", fontSize = 13.sp, fontWeight = FontWeight.Bold)
                }
            } else if (currentStatus == "none") {"""
content = content.replace(target_card_btn_cond, replacement_card_btn_cond)

target_card_btn_req = """                        requestStatus = "requested"
                        onJoinClick?.invoke() """
replacement_card_btn_req = """                        onJoinClick?.invoke() """
content = content.replace(target_card_btn_req, replacement_card_btn_req)

target_card_btn_requested = """            } else {
                Button(
                    onClick = { },
                    colors = ButtonDefaults.buttonColors(containerColor = Turf2, contentColor = Bench),
                    shape = RoundedCornerShape(20.dp),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    modifier = Modifier.height(32.dp)
                ) {
                    Text("Requested", fontSize = 13.sp, fontWeight = FontWeight.Bold)
                }
            }"""
replacement_card_btn_requested = """            } else if (currentStatus == "requested" || currentStatus == "pending") {
                Button(
                    onClick = { },
                    colors = ButtonDefaults.buttonColors(containerColor = Turf2, contentColor = Bench),
                    shape = RoundedCornerShape(20.dp),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    modifier = Modifier.height(32.dp)
                ) {
                    Text("Requested", fontSize = 13.sp, fontWeight = FontWeight.Bold)
                }
            } else if (currentStatus == "accepted") {
                Button(
                    onClick = { },
                    colors = ButtonDefaults.buttonColors(containerColor = Turf2, contentColor = Floodlight),
                    shape = RoundedCornerShape(20.dp),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    modifier = Modifier.height(32.dp)
                ) {
                    Text("Joined", fontSize = 13.sp, fontWeight = FontWeight.Bold)
                }
            }"""
content = content.replace(target_card_btn_requested, replacement_card_btn_requested)

target_feed_call = """            currentScreen == "main" -> FeedScreen(
                viewModel = viewModel,
                onMatchClick = { match -> selectedMatch = match; currentScreen = "postDetail" },
                onNotificationsClick = { currentScreen = "notifications" }
            )"""
replacement_feed_call = """            currentScreen == "main" -> FeedScreen(
                viewModel = viewModel,
                onMatchClick = { match -> selectedMatch = match; currentScreen = "postDetail" },
                onNotificationsClick = { currentScreen = "notifications" },
                userName = name
            )"""
content = content.replace(target_feed_call, replacement_feed_call)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
