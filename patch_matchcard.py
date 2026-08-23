with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target_card = """fun MatchCard(m: MatchEntity, onClick: () -> Unit, onJoinClick: (() -> Unit)? = null, currentStatus: String = "none") {
    var requestStatus by remember(m.id) { mutableStateOf("none") }
    Column(
        modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(16.dp)).background(Turf).border(1.dp, Line, RoundedCornerShape(16.dp)).clickable { onClick() }
    ) {"""
replacement_card = """fun MatchCard(m: MatchEntity, onClick: () -> Unit, onJoinClick: (() -> Unit)? = null, currentStatus: String = "none", onPosterClick: (() -> Unit)? = null) {
    var requestStatus by remember(m.id) { mutableStateOf("none") }
    Column(
        modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(16.dp)).background(Turf).border(1.dp, Line, RoundedCornerShape(16.dp)).clickable { onClick() }
    ) {"""
content = content.replace(target_card, replacement_card)

target_poster_row = """        Row(modifier = Modifier.padding(start = 18.dp, top = 14.dp, end = 18.dp, bottom = 10.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.size(26.dp).clip(CircleShape).background(Turf2), contentAlignment = Alignment.Center) {
                Text(m.posterName.first().toString(), color = Floodlight, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }
            Spacer(modifier = Modifier.width(8.dp))
            Text(m.posterName, color = Chalk, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.width(8.dp))
            Icon(Icons.Default.Star, contentDescription = null, tint = Floodlight, modifier = Modifier.size(11.dp))
            Text(m.posterTrust.toString(), color = Floodlight, fontSize = 11.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
        }"""
replacement_poster_row = """        Row(modifier = Modifier.padding(start = 18.dp, top = 14.dp, end = 18.dp, bottom = 10.dp).clickable { onPosterClick?.invoke() }, verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.size(26.dp).clip(CircleShape).background(Turf2), contentAlignment = Alignment.Center) {
                Text(m.posterName.firstOrNull()?.toString() ?: "?", color = Floodlight, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }
            Spacer(modifier = Modifier.width(8.dp))
            Text(m.posterName, color = Chalk, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.width(8.dp))
            Icon(Icons.Default.Star, contentDescription = null, tint = Floodlight, modifier = Modifier.size(11.dp))
            val ratingDisplay = if (m.posterTrust > 0) String.format("%.1f", m.posterTrust) else "New"
            Text(ratingDisplay, color = Floodlight, fontSize = 11.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
        }"""
content = content.replace(target_poster_row, replacement_poster_row)

target_feed_call = """fun FeedScreen(viewModel: MaidanViewModel, onMatchClick: (MatchEntity) -> Unit, onNotificationsClick: () -> Unit, userName: String) {"""
replacement_feed_call = """fun FeedScreen(viewModel: MaidanViewModel, onMatchClick: (MatchEntity) -> Unit, onNotificationsClick: () -> Unit, userName: String, onPosterClick: (String) -> Unit) {"""
content = content.replace(target_feed_call, replacement_feed_call)

target_card_call = """                MatchCard(
                    m = match, 
                    onClick = { onMatchClick(match) }, 
                    onJoinClick = { viewModel.requestToJoinMatch(match, userName) },
                    currentStatus = status
                )"""
replacement_card_call = """                MatchCard(
                    m = match, 
                    onClick = { onMatchClick(match) }, 
                    onJoinClick = { viewModel.requestToJoinMatch(match, userName) },
                    currentStatus = status,
                    onPosterClick = { if (match.posterId.isNotEmpty()) onPosterClick(match.posterId) }
                )"""
content = content.replace(target_card_call, replacement_card_call)

target_feed_usage = """                            "Home" -> FeedScreen(viewModel, onMatchClick = { 
                                selectedMatch = it
                                currentScreen = "postDetail"
                            }, onNotificationsClick = {
                                currentScreen = "notifications"
                            }, userName = name)"""
replacement_feed_usage = """                            "Home" -> FeedScreen(viewModel, onMatchClick = { 
                                selectedMatch = it
                                currentScreen = "postDetail"
                            }, onNotificationsClick = {
                                currentScreen = "notifications"
                            }, userName = name, onPosterClick = {
                                targetUserId = it
                                currentScreen = "userProfile"
                            })"""
content = content.replace(target_feed_usage, replacement_feed_usage)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

