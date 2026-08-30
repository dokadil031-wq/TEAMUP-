import re

with open("app/src/main/java/com/example/UserProfileScreen.kt", "r") as f:
    content = f.read()

target = """        if (profile!!.sports.isNotEmpty()) {
            Text("INTERESTS", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 8.dp))
            @OptIn(ExperimentalLayoutApi::class)
            FlowRow(modifier = Modifier.fillMaxWidth().padding(bottom = 24.dp), horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                profile!!.sports.forEach { s ->
                    Box(modifier = Modifier.clip(RoundedCornerShape(20.dp)).background(Turf2).padding(horizontal = 14.dp, vertical = 6.dp)) {
                        Text(s, color = Chalk, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                    }
                }
            }
        }"""

content = content.replace(target, "")

with open("app/src/main/java/com/example/UserProfileScreen.kt", "w") as f:
    f.write(content)
