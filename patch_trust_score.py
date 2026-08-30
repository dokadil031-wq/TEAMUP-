import re

with open("app/src/main/java/com/example/UserProfileScreen.kt", "r") as f:
    content = f.read()

target = """            Column {
                Text(profile!!.name, color = Chalk, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.Star, contentDescription = null, tint = Floodlight, modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(4.dp))
                    val avgRating = if (profile!!.reviewCount > 0) String.format("%.1f", profile!!.averageRating) else "No ratings"
                    Text("$avgRating (${profile!!.reviewCount} reviews)", color = Floodlight, fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
                }
            }"""

replacement = """            Column {
                Text(profile!!.name, color = Chalk, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("TRUST SCORE: ", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
                    Icon(Icons.Default.Star, contentDescription = null, tint = Floodlight, modifier = Modifier.size(14.dp))
                    Spacer(modifier = Modifier.width(2.dp))
                    val avgRating = if (profile!!.reviewCount > 0) String.format("%.1f", profile!!.averageRating) else "New"
                    Text("$avgRating (${profile!!.reviewCount} reviews)", color = Floodlight, fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
                }
            }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/UserProfileScreen.kt", "w") as f:
    f.write(content)
