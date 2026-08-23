with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target_cats = """    val categories = listOf("All", "Sports", "Online gaming", "Exercise")
    
    val subcats = mapOf(
        "Sports" to listOf("All Sports", "Cricket", "Football", "Badminton", "Basketball", "Volleyball", "Table tennis"),
        "Online gaming" to listOf("All Games", "BGMI", "Valorant", "FIFA", "Free Fire"),
        "Exercise" to listOf("All Exercises", "Running", "Gym", "Yoga", "Cycling")
    )"""

replacement_cats = """    val categories = listOf("All", "Sports", "Online gaming", "Exercise", "Group", "Other")
    
    val subcats = mapOf(
        "Sports" to listOf("All Sports", "Cricket", "Football", "Badminton", "Basketball", "Volleyball", "Table tennis"),
        "Online gaming" to listOf("All Games", "BGMI", "Valorant", "FIFA", "Free Fire"),
        "Exercise" to listOf("All Exercises", "Running", "Gym", "Yoga", "Cycling"),
        "Group" to listOf("All Groups", "Community", "Study", "Entrepreneur", "IT Development", "Coding")
    )"""

content = content.replace(target_cats, replacement_cats)

target_subcat_filter = """        if (category != "All") {
            val subList = subcats[category] ?: emptyList()
            if (subList.isNotEmpty()) {"""
replacement_subcat_filter = """        if (category != "All" && category != "Other") {
            val subList = subcats[category] ?: emptyList()
            if (subList.isNotEmpty()) {"""
content = content.replace(target_subcat_filter, replacement_subcat_filter)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
