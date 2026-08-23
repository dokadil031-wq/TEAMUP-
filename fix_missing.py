import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# We need to add ProfileSetupScreen, FeedScreen, BottomNavItem, MatchCard

missing_code = """
@OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)
@Composable
fun ProfileSetupScreen(
    name: String, onNameChange: (String) -> Unit,
    age: String, onAgeChange: (String) -> Unit,
    gender: String, onGenderChange: (String) -> Unit,
    selectedSports: List<String>, onToggleSport: (String) -> Unit,
    password: String = "", onPasswordChange: (String) -> Unit = {},
    onBack: () -> Unit, onNext: () -> Unit
) {
    val sportsList = listOf("Cricket", "Football", "Badminton", "Basketball", "Volleyball", "Table tennis", "Running", "Gym")
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(26.dp)
    ) {
        IconButton(onClick = onBack, modifier = Modifier.padding(bottom = 18.dp)) {
            Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = Bench)
        }
        StepDots(2)
        Text("Build your profile", color = Chalk, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp, modifier = Modifier.padding(bottom = 24.dp))
        
        OutlinedTextField(
            value = name,
            onValueChange = onNameChange,
            label = { Text("Full Name") },
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = Floodlight,
                focusedLabelColor = Floodlight,
                unfocusedBorderColor = Line,
                unfocusedLabelColor = Bench,
                focusedTextColor = Chalk,
                unfocusedTextColor = Chalk
            ),
            modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp)
        )
        
        Row(modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            OutlinedTextField(
                value = age,
                onValueChange = onAgeChange,
                label = { Text("Age") },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = Floodlight,
                    focusedLabelColor = Floodlight,
                    unfocusedBorderColor = Line,
                    unfocusedLabelColor = Bench,
                    focusedTextColor = Chalk,
                    unfocusedTextColor = Chalk
                ),
                modifier = Modifier.weight(1f)
            )
            OutlinedTextField(
                value = gender,
                onValueChange = onGenderChange,
                label = { Text("Gender") },
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = Floodlight,
                    focusedLabelColor = Floodlight,
                    unfocusedBorderColor = Line,
                    unfocusedLabelColor = Bench,
                    focusedTextColor = Chalk,
                    unfocusedTextColor = Chalk
                ),
                modifier = Modifier.weight(1f)
            )
        }
        
        Text("Sports you play", color = Chalk, fontSize = 14.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 8.dp))
        androidx.compose.foundation.layout.FlowRow(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            sportsList.forEach { sport ->
                val isSelected = selectedSports.contains(sport)
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(20.dp))
                        .background(if (isSelected) Floodlight else Turf2)
                        .clickable { onToggleSport(sport) }
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Text(sport, color = if (isSelected) Pitch else Bench, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
                }
            }
        }
        
        Spacer(modifier = Modifier.weight(1f))
        
        Text("Create Password", color = Chalk, fontSize = 14.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 8.dp, top = 16.dp))
        TextField(
            value = password,
            onValueChange = onPasswordChange,
            placeholder = { Text("At least 6 characters", color = Bench) },
            colors = TextFieldDefaults.colors(
                focusedContainerColor = Color.Transparent,
                unfocusedContainerColor = Color.Transparent,
                focusedIndicatorColor = Floodlight,
                unfocusedIndicatorColor = Line,
                focusedTextColor = Chalk,
                unfocusedTextColor = Chalk
            ),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
            modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp)
        )
        
        Button(
            onClick = onNext,
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Floodlight, contentColor = Pitch),
            shape = RoundedCornerShape(12.dp)
        ) {
            Text("Finish", fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun FeedScreen(viewModel: MaidanViewModel, onMatchClick: (MatchEntity) -> Unit) {
    val matches by viewModel.allMatches.collectAsStateWithLifecycle()
    val categories = listOf("All", "Sports", "Online gaming", "Exercise")
    var category by remember { mutableStateOf("All") }
    
    Column(modifier = Modifier.fillMaxSize()) {
        Text("Feed", color = Chalk, fontSize = 28.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 22.dp, vertical = 16.dp))
        
        LazyRow(contentPadding = PaddingValues(horizontal = 22.dp), horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.padding(bottom = 16.dp)) {
            items(categories) { cat ->
                val isSelected = category == cat
                Box(
                    modifier = Modifier.clip(RoundedCornerShape(20.dp))
                        .background(if (isSelected) Floodlight else Turf2)
                        .clickable { category = cat }
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Text(cat, color = if (isSelected) Pitch else Bench, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                }
            }
        }
        
        val filtered = if (category == "All") matches else matches.filter { it.category == category }
        
        LazyColumn(contentPadding = PaddingValues(horizontal = 22.dp, vertical = 8.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            items(filtered) { match ->
                MatchCard(match, onClick = { onMatchClick(match) })
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
fun MatchCard(m: MatchEntity, onClick: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(16.dp)).background(Turf).border(1.dp, Line, RoundedCornerShape(16.dp)).clickable { onClick() }
    ) {
        Row(modifier = Modifier.padding(start = 18.dp, top = 14.dp, end = 18.dp, bottom = 10.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.size(26.dp).clip(CircleShape).background(Turf2), contentAlignment = Alignment.Center) {
                Text(m.posterName.first().toString(), color = Floodlight, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }
            Spacer(modifier = Modifier.width(8.dp))
            Text(m.posterName, color = Chalk, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.width(8.dp))
            Icon(Icons.Default.Star, contentDescription = null, tint = Floodlight, modifier = Modifier.size(11.dp))
            Text(m.posterTrust.toString(), color = Floodlight, fontSize = 11.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
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
            Button(
                onClick = {},
                colors = ButtonDefaults.buttonColors(containerColor = Floodlight, contentColor = Pitch),
                shape = RoundedCornerShape(20.dp),
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                modifier = Modifier.height(32.dp)
            ) {
                Text("Request to join", fontSize = 13.sp, fontWeight = FontWeight.Bold)
            }
        }
    }
}
"""

content += missing_code

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

print("Restored missing screens")
