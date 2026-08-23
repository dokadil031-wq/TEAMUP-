import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = 'Text("Sports you play", color = Chalk, fontSize = 14.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 8.dp))'
replacement = 'Text("Categories you like", color = Chalk, fontSize = 14.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 8.dp))'
content = content.replace(target, replacement)

target_list = 'val sportsList = listOf("Cricket", "Football", "Badminton", "Basketball", "Volleyball", "Table tennis", "Running", "Gym", "Online gaming")'
replacement_list = 'val sportsList = listOf("Cricket", "Football", "Badminton", "Basketball", "Volleyball", "Table tennis", "Running", "Gym", "Online gaming", "Exercise")'
content = content.replace(target_list, replacement_list)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

print("Updated ProfileSetupScreen labels")
