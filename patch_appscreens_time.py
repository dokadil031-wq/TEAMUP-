import re

with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

# 1. Add state for timestamp
state_target = """    var timeStr by remember { mutableStateOf("") }"""
state_repl = """    var timeStr by remember { mutableStateOf("") }
    var matchTimestamp by remember { mutableStateOf(0L) }"""
content = content.replace(state_target, state_repl)

# 2. Update TimePickerDialog to set matchTimestamp
time_target = """                                { _, h, min ->
                                    val ampm = if (h >= 12) "PM" else "AM"
                                    val hr = if (h % 12 == 0) 12 else h % 12
                                    timeStr = String.format("%02d:%02d %s", hr, min, ampm)
                                }"""
time_repl = """                                { _, h, min ->
                                    val ampm = if (h >= 12) "PM" else "AM"
                                    val hr = if (h % 12 == 0) 12 else h % 12
                                    timeStr = String.format("%02d:%02d %s", hr, min, ampm)
                                    val selectedCal = java.util.Calendar.getInstance()
                                    selectedCal.set(y, m, d, h, min, 0)
                                    matchTimestamp = selectedCal.timeInMillis
                                }"""
content = content.replace(time_target, time_repl)

# 3. Add timestamp to newMatch
match_target = """                val newMatch = MatchEntity(
                    category = category,
                    sport = sport,
                    title = title,
                    location = location,
                    time = "$dateStr, $timeStr",
                    joined = 1,
                    total = totalPlayers,
                    audience = audience,
                    posterName = if (userName.isNotEmpty()) userName else "You",
                    posterTrust = 0.0
                )"""
match_repl = """                val newMatch = MatchEntity(
                    category = category,
                    sport = sport,
                    title = title,
                    location = location,
                    time = "$dateStr, $timeStr",
                    joined = 1,
                    total = totalPlayers,
                    audience = audience,
                    posterName = if (userName.isNotEmpty()) userName else "You",
                    posterTrust = 0.0,
                    timestamp = matchTimestamp
                )"""
content = content.replace(match_target, match_repl)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
