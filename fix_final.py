import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Fix @Composable @Composable
content = content.replace("@Composable\n@Composable", "@Composable")

# Fix FeedScreen signature and header
old_feed = """fun FeedScreen(viewModel: MaidanViewModel, onMatchClick: (MatchEntity) -> Unit) {
    val matches by viewModel.allMatches.collectAsStateWithLifecycle()
    val categories = listOf("All", "Sports", "Online gaming", "Exercise")
    var category by remember { mutableStateOf("All") }
    
    Column(modifier = Modifier.fillMaxSize()) {
        Text("Feed", color = Chalk, fontSize = 28.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 22.dp, vertical = 16.dp))"""

new_feed = """fun FeedScreen(viewModel: MaidanViewModel, onMatchClick: (MatchEntity) -> Unit, onNotificationsClick: () -> Unit) {
    val matches by viewModel.allMatches.collectAsStateWithLifecycle()
    val categories = listOf("All", "Sports", "Online gaming", "Exercise")
    var category by remember { mutableStateOf("All") }
    
    Column(modifier = Modifier.fillMaxSize()) {
        Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 22.dp, vertical = 16.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
            Text("Feed", color = Chalk, fontSize = 28.sp, fontWeight = FontWeight.Bold)
            IconButton(onClick = onNotificationsClick) {
                Icon(Icons.Default.Notifications, contentDescription = "Notifications", tint = Chalk)
            }
        }"""

content = content.replace(old_feed, new_feed)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

print("Fixed final issues")
