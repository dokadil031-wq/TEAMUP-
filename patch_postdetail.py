with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target = """        Text("Casual weekend match, all skill levels welcome. Extra bats and pads available.", color = Bench, fontSize = 14.sp, lineHeight = 20.sp, modifier = Modifier.padding(bottom = 20.dp))
        
        Column(modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(Turf2).padding(14.dp).padding(bottom = 4.dp)) {"""
replacement = """        Text("Players: ${match.joined} / ${match.total}", color = Floodlight, fontSize = 14.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 12.dp))
        
        Column(modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(Turf2).padding(14.dp).padding(bottom = 4.dp)) {"""
content = content.replace(target, replacement)

target2 = """            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(bottom = 12.dp)) {
                Icon(Icons.Default.LocationOn, contentDescription = null, tint = Floodlight, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text(match.location, color = Chalk, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
            }"""
replacement2 = """            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(bottom = 12.dp)) {
                Icon(Icons.Default.LocationOn, contentDescription = null, tint = Floodlight, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text(match.location, color = Chalk, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
            }
            if (match.lat != 0.0 && match.lng != 0.0) {
                val matchPos = com.google.android.gms.maps.model.LatLng(match.lat, match.lng)
                val cameraPositionState = com.google.maps.android.compose.rememberCameraPositionState {
                    position = com.google.android.gms.maps.model.CameraPosition.fromLatLngZoom(matchPos, 14f)
                }
                Box(modifier = Modifier.fillMaxWidth().height(150.dp).clip(RoundedCornerShape(8.dp)).padding(bottom = 12.dp)) {
                    com.google.maps.android.compose.GoogleMap(
                        modifier = Modifier.fillMaxSize(),
                        cameraPositionState = cameraPositionState,
                        uiSettings = com.google.maps.android.compose.MapUiSettings(zoomControlsEnabled = false, scrollGesturesEnabled = false, zoomGesturesEnabled = false)
                    ) {
                        com.google.maps.android.compose.Marker(
                            state = com.google.maps.android.compose.MarkerState(position = matchPos)
                        )
                    }
                }
            }"""
content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
