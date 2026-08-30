import re

with open("app/src/main/java/com/example/UserProfileScreen.kt", "r") as f:
    content = f.read()

target = """            Column {
                Text(profile!!.name, color = Chalk, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("TRUST SCORE: ", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)"""

replacement = """            Column {
                Text(profile!!.name, color = Chalk, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                if (profile!!.age.isNotEmpty() || profile!!.gender.isNotEmpty()) {
                    val ageStr = if (profile!!.age.isNotEmpty()) "${profile!!.age} yrs" else ""
                    val separator = if (profile!!.age.isNotEmpty() && profile!!.gender.isNotEmpty()) " · " else ""
                    val genderStr = profile!!.gender
                    Text("$ageStr$separator$genderStr", color = Bench, fontSize = 13.sp, modifier = Modifier.padding(bottom = 4.dp))
                }
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("TRUST SCORE: ", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/UserProfileScreen.kt", "w") as f:
    f.write(content)
