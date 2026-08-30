import re

with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    text = f.read()

target = """    private fun insertInitialDataIfNeeded() {
        val initial = listOf(
            MatchEntity("", "Sports", "", "Cricket", "Sunday morning cricket, need 3 more", "DLF Ground, Sector 14", "Tomorrow, 7:00 AM", 5, 8, "All", "Rahul Verma", "", 4.8),
            MatchEntity("", "Sports", "", "Badminton", "Evening doubles, casual level", "Indoor Court, Sector 21", "Today, 6:30 PM", 2, 4, "Female", "Priya Sharma", "", 4.9),
            MatchEntity("", "Sports", "", "Football", "5-a-side, need a keeper", "Turf Arena, Sector 29", "Sat, 5:00 PM", 8, 10, "All", "Arjun Mehta", "", 3.9),
            MatchEntity("", "Online gaming", "", "BGMI", "Squad push, ranked grind tonight", "Online", "Today, 9:00 PM", 2, 4, "All", "Arjun Mehta", "", 3.9),
            MatchEntity("", "Exercise", "", "Running", "5K morning run, easy pace", "City Park, Gate 2", "Tomorrow, 6:00 AM", 4, 12, "All", "Sneha Kulkarni", "", 4.6)
        )"""

repl = """    private fun insertInitialDataIfNeeded() {
        val initial = listOf(
            MatchEntity(category = "Sports", sport = "Cricket", title = "Sunday morning cricket, need 3 more", location = "DLF Ground, Sector 14", time = "Tomorrow, 7:00 AM", joined = 5, total = 8, audience = "All", posterName = "Rahul Verma", posterTrust = 4.8),
            MatchEntity(category = "Sports", sport = "Badminton", title = "Evening doubles, casual level", location = "Indoor Court, Sector 21", time = "Today, 6:30 PM", joined = 2, total = 4, audience = "Female", posterName = "Priya Sharma", posterTrust = 4.9),
            MatchEntity(category = "Sports", sport = "Football", title = "5-a-side, need a keeper", location = "Turf Arena, Sector 29", time = "Sat, 5:00 PM", joined = 8, total = 10, audience = "All", posterName = "Arjun Mehta", posterTrust = 3.9),
            MatchEntity(category = "Online gaming", sport = "BGMI", title = "Squad push, ranked grind tonight", location = "Online", time = "Today, 9:00 PM", joined = 2, total = 4, audience = "All", posterName = "Arjun Mehta", posterTrust = 3.9),
            MatchEntity(category = "Exercise", sport = "Running", title = "5K morning run, easy pace", location = "City Park, Gate 2", time = "Tomorrow, 6:00 AM", joined = 4, total = 12, audience = "All", posterName = "Sneha Kulkarni", posterTrust = 4.6)
        )"""

text = text.replace(target, repl)

with open("app/src/main/java/com/example/MaidanViewModel.kt", "w") as f:
    f.write(text)
