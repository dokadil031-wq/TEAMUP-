import re

with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target = """fun CreatePostScreen(viewModel: MaidanViewModel, onPostCreated: () -> Unit) {
    var category by remember { mutableStateOf("Sports") }
    var sport by remember { mutableStateOf("") }
    var title by remember { mutableStateOf("") }
    var description by remember { mutableStateOf("") }
    var location by remember { mutableStateOf("") }
    var time by remember { mutableStateOf("") }
    var audience by remember { mutableStateOf("All") }
    val userName by viewModel.userName.collectAsStateWithLifecycle()
    
    val valid = title.isNotEmpty() && sport.isNotEmpty() && location.isNotEmpty() && time.isNotEmpty()
"""
replacement = """fun CreatePostScreen(viewModel: MaidanViewModel, onPostCreated: () -> Unit) {
    var category by remember { mutableStateOf("Sports") }
    var sport by remember { mutableStateOf("") }
    var title by remember { mutableStateOf("") }
    var description by remember { mutableStateOf("") }
    var location by remember { mutableStateOf("") }
    var dateStr by remember { mutableStateOf("") }
    var timeStr by remember { mutableStateOf("") }
    var audience by remember { mutableStateOf("All") }
    var totalPlayers by remember { mutableStateOf(4) }
    var mapSelectedPosition by remember { mutableStateOf<com.google.android.gms.maps.model.LatLng?>(null) }
    val userName by viewModel.userName.collectAsStateWithLifecycle()
    
    val context = androidx.compose.ui.platform.LocalContext.current
    
    val valid = title.isNotEmpty() && sport.isNotEmpty() && location.isNotEmpty() && dateStr.isNotEmpty() && timeStr.isNotEmpty()
"""
content = content.replace(target, replacement)

target2 = """                TextField(
                    value = time, onValueChange = { time = it }, placeholder = { Text("Today, 6 PM", color = Bench) },
                    colors = TextFieldDefaults.colors(focusedContainerColor = Turf2, unfocusedContainerColor = Turf2, focusedIndicatorColor = Color.Transparent, unfocusedIndicatorColor = Color.Transparent, focusedTextColor = Chalk, unfocusedTextColor = Chalk, cursorColor = Floodlight),
                    shape = RoundedCornerShape(10.dp), modifier = Modifier.fillMaxWidth().border(1.dp, Line, RoundedCornerShape(10.dp))
                )"""

replacement2 = """                Box(modifier = Modifier.fillMaxWidth().height(56.dp).border(1.dp, Line, RoundedCornerShape(10.dp)).background(Turf2, RoundedCornerShape(10.dp)).clickable {
                    val cal = java.util.Calendar.getInstance()
                    android.app.DatePickerDialog(
                        context,
                        { _, y, m, d ->
                            dateStr = "$d/${m+1}/$y"
                            android.app.TimePickerDialog(
                                context,
                                { _, h, min ->
                                    val ampm = if (h >= 12) "PM" else "AM"
                                    val hr = if (h % 12 == 0) 12 else h % 12
                                    timeStr = String.format("%02d:%02d %s", hr, min, ampm)
                                },
                                cal.get(java.util.Calendar.HOUR_OF_DAY),
                                cal.get(java.util.Calendar.MINUTE),
                                false
                            ).show()
                        },
                        cal.get(java.util.Calendar.YEAR),
                        cal.get(java.util.Calendar.MONTH),
                        cal.get(java.util.Calendar.DAY_OF_MONTH)
                    ).show()
                }, contentAlignment = Alignment.CenterStart) {
                    Text(
                        text = if (dateStr.isEmpty()) "Select Time" else "$dateStr, $timeStr",
                        color = if (dateStr.isEmpty()) Bench else Chalk,
                        fontSize = 14.sp,
                        modifier = Modifier.padding(start = 16.dp)
                    )
                }"""
content = content.replace(target2, replacement2)

target3 = """        Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth().padding(bottom = 26.dp)) {"""
replacement3 = """        Text("TOTAL PLAYERS NEEDED", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 6.dp))
        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(bottom = 14.dp)) {
            Slider(
                value = totalPlayers.toFloat(),
                onValueChange = { totalPlayers = it.toInt() },
                valueRange = 2f..22f,
                steps = 20,
                modifier = Modifier.weight(1f)
            )
            Spacer(modifier = Modifier.width(16.dp))
            Text(totalPlayers.toString(), color = Chalk, fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }
        
        Text("PIN ON MAP", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 6.dp))
        val initialMapPos = com.google.android.gms.maps.model.LatLng(28.6139, 77.2090) // Default to New Delhi
        val cameraPositionState = com.google.maps.android.compose.rememberCameraPositionState {
            position = com.google.android.gms.maps.model.CameraPosition.fromLatLngZoom(initialMapPos, 10f)
        }
        Box(modifier = Modifier.fillMaxWidth().height(200.dp).clip(RoundedCornerShape(10.dp)).border(1.dp, Line, RoundedCornerShape(10.dp)).padding(bottom = 14.dp)) {
            com.google.maps.android.compose.GoogleMap(
                modifier = Modifier.fillMaxSize(),
                cameraPositionState = cameraPositionState,
                onMapClick = { latLng -> mapSelectedPosition = latLng }
            ) {
                mapSelectedPosition?.let { pos ->
                    com.google.maps.android.compose.Marker(
                        state = com.google.maps.android.compose.MarkerState(position = pos),
                        title = "Selected Location"
                    )
                }
            }
        }
        
        Text("WHO CAN SEE THIS POST", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 8.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth().padding(bottom = 26.dp)) {"""
content = content.replace(target3, replacement3)

target4 = """                    location = location,
                    time = time,
                    joined = 1,
                    total = 8,
                    audience = audience,
                    posterName = if (userName.isNotEmpty()) userName else "You",
                    posterTrust = 0.0
                )"""
replacement4 = """                    location = location,
                    time = "$dateStr, $timeStr",
                    joined = 1,
                    total = totalPlayers,
                    audience = audience,
                    posterName = if (userName.isNotEmpty()) userName else "You",
                    posterTrust = 0.0,
                    lat = mapSelectedPosition?.latitude ?: 0.0,
                    lng = mapSelectedPosition?.longitude ?: 0.0
                )"""
content = content.replace(target4, replacement4)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
