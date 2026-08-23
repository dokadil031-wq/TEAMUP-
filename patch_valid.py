with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

import re

content = re.sub(
    r'val categories = listOf\("Sports", "Online gaming", "Exercise"\).*?val valid = category\.isNotEmpty\(\) && sport\.isNotEmpty\(\) && title\.isNotEmpty\(\) && location\.isNotEmpty\(\) && time\.isNotEmpty\(\)',
    r'''val categories = listOf("Sports", "Online gaming", "Exercise", "Group", "Other")
    val subcats = mapOf(
        "Sports" to listOf("Cricket", "Football", "Badminton", "Basketball", "Volleyball", "Table tennis"),
        "Online gaming" to listOf("BGMI", "Valorant", "FIFA", "Free Fire"),
        "Exercise" to listOf("Running", "Gym", "Yoga", "Cycling"),
        "Group" to listOf("Community", "Study", "Entrepreneur", "IT Development", "Coding")
    )

    val valid = category.isNotEmpty() && (sport.isNotEmpty() || category == "Other") && title.isNotEmpty() && location.isNotEmpty() && time.isNotEmpty()''',
    content,
    flags=re.DOTALL
)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
