import re

with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target = """            Text("No one's live right now.", color = Bench, fontSize = 14.sp, modifier = Modifier.fillMaxWidth().padding(vertical = 20.dp), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
            Text("More live streams show up here as players you've matched with go live.", color = Bench, fontSize = 13.sp, modifier = Modifier.fillMaxWidth().padding(10.dp), textAlign = androidx.compose.ui.text.style.TextAlign.Center)"""

repl = """            androidx.compose.foundation.layout.Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 20.dp)
                    .clip(RoundedCornerShape(12.dp))
                    .background(Turf2)
                    .clickable {
                        val intent = android.content.Intent(context, LiveActivity::class.java).apply {
                            putExtra("isHost", false)
                        }
                        context.startActivity(intent)
                    }
                    .padding(16.dp),
                contentAlignment = Alignment.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Default.PlayArrow, contentDescription = null, tint = Whistle, modifier = Modifier.size(48.dp))
                    Spacer(modifier = Modifier.height(8.dp))
                    Text("Join Test Stream", color = Chalk, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    Text("Tap to join a live session", color = Bench, fontSize = 12.sp)
                }
            }"""

content = content.replace(target, repl)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
