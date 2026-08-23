with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target_def = """fun PostDetailScreen(match: MatchEntity, viewModel: MaidanViewModel, onBack: () -> Unit, onMessageClick: () -> Unit, userName: String) {"""
replacement_def = """fun PostDetailScreen(match: MatchEntity, viewModel: MaidanViewModel, onBack: () -> Unit, onMessageClick: () -> Unit, userName: String, onPosterClick: (String) -> Unit) {"""
content = content.replace(target_def, replacement_def)

target_poster = """        Row(modifier = Modifier.padding(bottom = 24.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.size(36.dp).clip(CircleShape).background(Turf2), contentAlignment = Alignment.Center) {
                Text(match.posterName.first().toString(), color = Floodlight, fontSize = 16.sp, fontWeight = FontWeight.Bold)
            }
            Spacer(modifier = Modifier.width(12.dp))
            Column {
                Text(match.posterName, color = Chalk, fontSize = 15.sp, fontWeight = FontWeight.Bold)
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.Star, contentDescription = null, tint = Floodlight, modifier = Modifier.size(12.dp))
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(match.posterTrust.toString(), color = Floodlight, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
                }
            }
        }"""
replacement_poster = """        Row(modifier = Modifier.padding(bottom = 24.dp).clickable { if (match.posterId.isNotEmpty()) onPosterClick(match.posterId) }, verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.size(36.dp).clip(CircleShape).background(Turf2), contentAlignment = Alignment.Center) {
                Text(match.posterName.firstOrNull()?.toString() ?: "?", color = Floodlight, fontSize = 16.sp, fontWeight = FontWeight.Bold)
            }
            Spacer(modifier = Modifier.width(12.dp))
            Column {
                Text(match.posterName, color = Chalk, fontSize = 15.sp, fontWeight = FontWeight.Bold)
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.Star, contentDescription = null, tint = Floodlight, modifier = Modifier.size(12.dp))
                    Spacer(modifier = Modifier.width(4.dp))
                    val ratingDisplay = if (match.posterTrust > 0) String.format("%.1f", match.posterTrust) else "New"
                    Text(ratingDisplay, color = Floodlight, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
                }
            }
        }"""
content = content.replace(target_poster, replacement_poster)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
