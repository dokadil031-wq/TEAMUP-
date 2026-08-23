with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    content = f.read()

target = """            MatchEntity("", "Sports", "Cricket", "Sunday morning cricket, need 3 more", "DLF Ground, Sector 14", "Tomorrow, 7:00 AM", 5, 8, "All", "Rahul Verma", 4.8),
            MatchEntity("", "Sports", "Badminton", "Evening doubles, casual level", "Indoor Court, Sector 21", "Today, 6:30 PM", 2, 4, "Female", "Priya Sharma", 4.9),
            MatchEntity("", "Sports", "Football", "5-a-side, need a keeper", "Turf Arena, Sector 29", "Sat, 5:00 PM", 8, 10, "All", "Arjun Mehta", 3.9),
            MatchEntity("", "Online gaming", "BGMI", "Squad push, ranked grind tonight", "Online", "Today, 9:00 PM", 2, 4, "All", "Arjun Mehta", 3.9),
            MatchEntity("", "Exercise", "Running", "5K morning run, easy pace", "City Park, Gate 2", "Tomorrow, 6:00 AM", 4, 12, "All", "Sneha Kulkarni", 4.6)"""

replacement = """            MatchEntity("", "Sports", "Cricket", "Sunday morning cricket, need 3 more", "DLF Ground, Sector 14", "Tomorrow, 7:00 AM", 5, 8, "All", "Rahul Verma", "", 4.8),
            MatchEntity("", "Sports", "Badminton", "Evening doubles, casual level", "Indoor Court, Sector 21", "Today, 6:30 PM", 2, 4, "Female", "Priya Sharma", "", 4.9),
            MatchEntity("", "Sports", "Football", "5-a-side, need a keeper", "Turf Arena, Sector 29", "Sat, 5:00 PM", 8, 10, "All", "Arjun Mehta", "", 3.9),
            MatchEntity("", "Online gaming", "BGMI", "Squad push, ranked grind tonight", "Online", "Today, 9:00 PM", 2, 4, "All", "Arjun Mehta", "", 3.9),
            MatchEntity("", "Exercise", "Running", "5K morning run, easy pace", "City Park, Gate 2", "Tomorrow, 6:00 AM", 4, 12, "All", "Sneha Kulkarni", "", 4.6)"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MaidanViewModel.kt", "w") as f:
    f.write(content)
