import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

components = """
@Composable
fun FeedScreen(viewModel: MaidanViewModel, onMatchClick: (MatchEntity) -> Unit, onNotificationsClick: () -> Unit, userName: String, onPosterClick: (String) -> Unit) {
    val matches by viewModel.allMatches.collectAsStateWithLifecycle()
    val myRequests by viewModel.myRequests.collectAsStateWithLifecycle()
    val uid = viewModel.auth.currentUser?.uid
    var category by remember { mutableStateOf("All") }
    var selectedSubcat by remember { mutableStateOf("All") }
    
    val categories = listOf("All", "Sports", "Online gaming", "Exercise", "Group", "Other")
    val subcats = mapOf(
        "Sports" to listOf("Cricket", "Football", "Badminton", "Basketball", "Volleyball", "Table tennis"),
        "Online gaming" to listOf("BGMI", "Valorant", "FIFA", "Free Fire"),
        "Exercise" to listOf("Running", "Gym", "Yoga", "Cycling"),
        "Group" to listOf("Community", "Study", "Entrepreneur", "IT Development", "Coding")
    )
    
    Column(modifier = Modifier.fillMaxSize()) {
        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 22.dp, vertical = 16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Maidan", color = Chalk, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp)
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(modifier = Modifier.size(36.dp).clip(CircleShape).background(Turf2).clickable { onNotificationsClick() }, contentAlignment = Alignment.Center) {
                    Icon(Icons.Default.Notifications, contentDescription = "Notifications", tint = Floodlight, modifier = Modifier.size(18.dp))
                }
            }
        }
        
        LazyRow(contentPadding = PaddingValues(horizontal = 22.dp), horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.padding(bottom = 12.dp)) {
            items(categories) { c ->
                val isSelected = category == c
                Box(
                    modifier = Modifier.clip(RoundedCornerShape(20.dp))
                        .background(if (isSelected) Floodlight else Turf)
                        .border(1.dp, if (isSelected) Color.Transparent else Line, RoundedCornerShape(20.dp))
                        .clickable { category = c; selectedSubcat = "All" }
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Text(c, color = if (isSelected) Pitch else Bench, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
                }
            }
        }
        
        if (category != "All" && category != "Other") {
            val subs = listOf("All ${category}") + (subcats[category] ?: emptyList())
            LazyRow(contentPadding = PaddingValues(horizontal = 22.dp), horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.padding(bottom = 14.dp)) {
                items(subs) { sub ->
                    val isSelected = selectedSubcat == sub
                    Box(
                        modifier = Modifier.clip(RoundedCornerShape(20.dp))
                            .background(if (isSelected) Chalk else Turf2)
                            .clickable { selectedSubcat = sub }
                            .padding(horizontal = 14.dp, vertical = 6.dp)
                    ) {
                        Text(sub, color = if (isSelected) Pitch else Chalk, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                    }
                }
            }
        }
        
        val filtered = matches.filter { match ->
            val catMatch = category == "All" || match.category == category
            val subcatMatch = selectedSubcat == "All" || selectedSubcat.startsWith("All ") || match.sport == selectedSubcat
            catMatch && subcatMatch
        }
        
        LazyColumn(contentPadding = PaddingValues(horizontal = 22.dp, vertical = 8.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            items(filtered) { match ->
                val req = myRequests.find { it.matchId == match.id }
                val status = if (match.posterId == uid) "mine" else req?.status ?: "none"
                MatchCard(
                    m = match, 
                    onClick = { onMatchClick(match) }, 
                    onJoinClick = { viewModel.requestToJoinMatch(match, userName) },
                    currentStatus = status,
                    onPosterClick = { if (match.posterId.isNotEmpty()) onPosterClick(match.posterId) }
                )
            }
        }
    }
}

@Composable
fun BottomNavItem(icon: androidx.compose.ui.graphics.vector.ImageVector, label: String, isSelected: Boolean, onClick: () -> Unit) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier.clickable(onClick = onClick).padding(8.dp)
    ) {
        Icon(icon, contentDescription = label, tint = if (isSelected) Chalk else Bench, modifier = Modifier.size(24.dp))
        Spacer(modifier = Modifier.height(4.dp))
        Text(label, color = if (isSelected) Chalk else Bench, fontSize = 10.sp, fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal)
    }
}

@Composable
fun MatchCard(m: MatchEntity, onClick: () -> Unit, onJoinClick: (() -> Unit)? = null, currentStatus: String = "none", onPosterClick: (() -> Unit)? = null) {
    Column(
        modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(16.dp)).background(Turf).border(1.dp, Line, RoundedCornerShape(16.dp)).clickable { onClick() }
    ) {
        Row(modifier = Modifier.padding(start = 18.dp, top = 14.dp, end = 18.dp, bottom = 10.dp).clickable { onPosterClick?.invoke() }, verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.size(26.dp).clip(CircleShape).background(Turf2), contentAlignment = Alignment.Center) {
                Text(m.posterName.firstOrNull()?.toString() ?: "?", color = Floodlight, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }
            Spacer(modifier = Modifier.width(8.dp))
            Text(m.posterName, color = Chalk, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.width(8.dp))
            Icon(Icons.Default.Star, contentDescription = null, tint = Floodlight, modifier = Modifier.size(11.dp))
            val ratingDisplay = if (m.posterTrust > 0) String.format("%.1f", m.posterTrust) else "New"
            Text(ratingDisplay, color = Floodlight, fontSize = 11.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
        }
        
        Column(modifier = Modifier.padding(horizontal = 18.dp).padding(bottom = 14.dp)) {
            Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                Text(m.sport.uppercase(), color = Floodlight, fontSize = 11.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.background(Turf2, RoundedCornerShape(20.dp)).padding(horizontal = 10.dp, vertical = 4.dp))
                if (m.audience != "All") {
                    Text("${m.audience} only", color = Bench, fontSize = 11.sp, fontWeight = FontWeight.SemiBold, fontFamily = FontFamily.Monospace, modifier = Modifier.border(1.dp, Line, RoundedCornerShape(20.dp)).padding(horizontal = 10.dp, vertical = 4.dp))
                }
            }
            Text(m.title, color = Chalk, fontSize = 16.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 10.dp))
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(bottom = 4.dp)) {
                Icon(Icons.Default.LocationOn, contentDescription = null, tint = Bench, modifier = Modifier.size(13.dp))
                Spacer(modifier = Modifier.width(6.dp))
                Text(m.location, color = Bench, fontSize = 13.sp)
            }
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.DateRange, contentDescription = null, tint = Bench, modifier = Modifier.size(13.dp))
                Spacer(modifier = Modifier.width(6.dp))
                Text(m.time, color = Bench, fontSize = 13.sp)
            }
        }
        
        androidx.compose.foundation.Canvas(modifier = Modifier.fillMaxWidth().height(1.dp)) {
            drawLine(
                color = Line,
                start = Offset(0f, 0f),
                end = Offset(size.width, 0f),
                pathEffect = PathEffect.dashPathEffect(floatArrayOf(12f, 12f), 0f)
            )
        }
        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 18.dp, vertical = 12.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.Person, contentDescription = null, tint = Bench, modifier = Modifier.size(14.dp))
                Spacer(modifier = Modifier.width(6.dp))
                Text("${m.joined}/${m.total} joined", color = Bench, fontSize = 13.sp, fontFamily = FontFamily.Monospace)
            }
            if (currentStatus == "mine") {
                Button(
                    onClick = { },
                    colors = ButtonDefaults.buttonColors(containerColor = Turf2, contentColor = Bench),
                    shape = RoundedCornerShape(20.dp),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    modifier = Modifier.height(32.dp)
                ) {
                    Text("My Post", fontSize = 13.sp, fontWeight = FontWeight.Bold)
                }
            } else if (currentStatus == "none") {
                Button(
                    onClick = { 
                        onJoinClick?.invoke() 
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = Floodlight, contentColor = Pitch),
                    shape = RoundedCornerShape(20.dp),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    modifier = Modifier.height(32.dp)
                ) {
                    Text("Request to join", fontSize = 13.sp, fontWeight = FontWeight.Bold)
                }
            } else if (currentStatus == "requested" || currentStatus == "pending") {
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
            }
        }
    }
}
"""

# Insert these components right before `fun AuthScreen(`
idx = content.find("@Composable\nfun AuthScreen(")
if idx != -1:
    content = content[:idx] + components + "\n" + content[idx:]
else:
    print("Could not find AuthScreen")

# Fix stray syntax errors at end of file if any
lines = content.split('\n')
while lines and lines[-1].strip() == '':
    lines.pop()
if lines and "@Composable" in lines[-1]:
    lines.pop()
if lines and lines[-1].strip() == "}":
    pass # ok
else:
    print("Warning: syntax might be off at end of file")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write('\n'.join(lines))
