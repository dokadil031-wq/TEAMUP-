import re

with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target = """fun LiveScreen() {
    Column(modifier = Modifier.fillMaxSize().padding(horizontal = 22.dp, vertical = 16.dp)) {
        Row(
            modifier = Modifier.fillMaxWidth().padding(bottom = 20.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Live now", color = Chalk, fontSize = 26.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp)
            Button(
                onClick = { },
                colors = ButtonDefaults.buttonColors(containerColor = Whistle, contentColor = Color.White),
                shape = RoundedCornerShape(20.dp),
                contentPadding = PaddingValues(horizontal = 14.dp, vertical = 8.dp),
                modifier = Modifier.height(32.dp)
            ) {
                Icon(Icons.Default.PlayArrow, contentDescription = null, modifier = Modifier.size(13.dp))
                Spacer(modifier = Modifier.width(5.dp))
                Text("Go live", fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }
        }
        
        Text("No one's live right now.", color = Bench, fontSize = 14.sp, modifier = Modifier.fillMaxWidth().padding(vertical = 20.dp), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
        
        Spacer(modifier = Modifier.weight(1f))
        Text("More live streams show up here as players you've matched with go live.", color = Bench, fontSize = 13.sp, modifier = Modifier.fillMaxWidth().padding(10.dp), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
    }
}"""

replacement = """fun LiveScreen() {
    var isStreaming by remember { mutableStateOf(false) }
    if (isStreaming) {
        Box(modifier = Modifier.fillMaxSize().background(Color.Black)) {
            // Fake Camera Preview
            Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally) {
                Icon(Icons.Default.Videocam, contentDescription = null, tint = Bench.copy(alpha = 0.5f), modifier = Modifier.size(64.dp))
                Spacer(modifier = Modifier.height(8.dp))
                Text("Camera Preview Active", color = Bench.copy(alpha = 0.5f))
            }
            
            // Overlay
            Column(modifier = Modifier.fillMaxSize().padding(22.dp)) {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Row(
                        modifier = Modifier.clip(RoundedCornerShape(8.dp)).background(Whistle).padding(horizontal = 8.dp, vertical = 4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(modifier = Modifier.size(8.dp).clip(CircleShape).background(Color.White))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("LIVE", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    }
                    Box(modifier = Modifier.clip(RoundedCornerShape(8.dp)).background(Pitch.copy(alpha = 0.5f)).padding(horizontal = 8.dp, vertical = 4.dp)) {
                        Text("12 viewers", color = Chalk, fontSize = 12.sp)
                    }
                }
                Spacer(modifier = Modifier.weight(1f))
                
                // Chat and End Stream
                Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                    TextField(
                        value = "", onValueChange = {},
                        placeholder = { Text("Say something...", color = Bench) },
                        modifier = Modifier.weight(1f).height(50.dp).clip(RoundedCornerShape(25.dp)),
                        colors = TextFieldDefaults.colors(
                            focusedContainerColor = Turf2.copy(alpha=0.7f),
                            unfocusedContainerColor = Turf2.copy(alpha=0.7f),
                            focusedIndicatorColor = Color.Transparent,
                            unfocusedIndicatorColor = Color.Transparent
                        )
                    )
                    Spacer(modifier = Modifier.width(12.dp))
                    IconButton(
                        onClick = { isStreaming = false },
                        modifier = Modifier.size(50.dp).clip(CircleShape).background(Color(0xFFE53935))
                    ) {
                        Icon(Icons.Default.Close, contentDescription = "End Stream", tint = Color.White)
                    }
                }
            }
        }
    } else {
        Column(modifier = Modifier.fillMaxSize().padding(horizontal = 22.dp, vertical = 16.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth().padding(bottom = 20.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Live now", color = Chalk, fontSize = 26.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp)
                Button(
                    onClick = { isStreaming = true },
                    colors = ButtonDefaults.buttonColors(containerColor = Whistle, contentColor = Color.White),
                    shape = RoundedCornerShape(20.dp),
                    contentPadding = PaddingValues(horizontal = 14.dp, vertical = 8.dp),
                    modifier = Modifier.height(32.dp)
                ) {
                    Icon(Icons.Default.PlayArrow, contentDescription = null, modifier = Modifier.size(13.dp))
                    Spacer(modifier = Modifier.width(5.dp))
                    Text("Go live", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }
            }
            
            Text("No one's live right now.", color = Bench, fontSize = 14.sp, modifier = Modifier.fillMaxWidth().padding(vertical = 20.dp), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
            
            Spacer(modifier = Modifier.weight(1f))
            Text("More live streams show up here as players you've matched with go live.", color = Bench, fontSize = 13.sp, modifier = Modifier.fillMaxWidth().padding(10.dp), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
        }
    }
}"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
print("LiveScreen updated")
