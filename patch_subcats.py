with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target1 = """fun FeedScreen(viewModel: MaidanViewModel, onMatchClick: (MatchEntity) -> Unit, onNotificationsClick: () -> Unit) {
    val matches by viewModel.allMatches.collectAsStateWithLifecycle()
    val categories = listOf("All", "Sports", "Online gaming", "Exercise")
    var category by remember { mutableStateOf("All") }"""

replacement1 = """fun FeedScreen(viewModel: MaidanViewModel, onMatchClick: (MatchEntity) -> Unit, onNotificationsClick: () -> Unit) {
    val matches by viewModel.allMatches.collectAsStateWithLifecycle()
    val categories = listOf("All", "Sports", "Online gaming", "Exercise")
    
    val subcats = mapOf(
        "Sports" to listOf("All Sports", "Cricket", "Football", "Badminton", "Basketball", "Volleyball", "Table tennis"),
        "Online gaming" to listOf("All Games", "BGMI", "Valorant", "FIFA", "Free Fire"),
        "Exercise" to listOf("All Exercises", "Running", "Gym", "Yoga", "Cycling")
    )

    var category by remember { mutableStateOf("All") }
    var selectedSubcat by remember { mutableStateOf("All") }"""

content = content.replace(target1, replacement1)

target2 = """.clickable { category = cat }"""
replacement2 = """.clickable { 
                            category = cat
                            selectedSubcat = if (cat == "All") "All" else subcats[cat]?.firstOrNull() ?: "All" 
                        }"""
content = content.replace(target2, replacement2)

target3 = """        }
        
        val filtered = if (category == "All") matches else matches.filter { it.category == category }
        
        LazyColumn(contentPadding = PaddingValues(horizontal = 22.dp, vertical = 8.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {"""

replacement3 = """        }
        
        if (category != "All") {
            val subList = subcats[category] ?: emptyList()
            if (subList.isNotEmpty()) {
                LazyRow(contentPadding = PaddingValues(horizontal = 22.dp), horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.padding(bottom = 16.dp)) {
                    items(subList) { sub ->
                        val isSelected = selectedSubcat == sub
                        Box(
                            modifier = Modifier.clip(RoundedCornerShape(20.dp))
                                .background(if (isSelected) Bench else Turf)
                                .border(1.dp, if (isSelected) Bench else Line, RoundedCornerShape(20.dp))
                                .clickable { selectedSubcat = sub }
                                .padding(horizontal = 14.dp, vertical = 6.dp)
                        ) {
                            Text(sub, color = if (isSelected) Pitch else Chalk, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                        }
                    }
                }
            }
        }
        
        val filtered = matches.filter { match ->
            val catMatch = category == "All" || match.category == category
            val subcatMatch = selectedSubcat == "All" || selectedSubcat.startsWith("All ") || match.sport == selectedSubcat
            catMatch && subcatMatch
        }
        
        LazyColumn(contentPadding = PaddingValues(horizontal = 22.dp, vertical = 8.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {"""

content = content.replace(target3, replacement3)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
