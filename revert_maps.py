import re

with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

# 1. Remove mapSelectedPosition
content = re.sub(
    r"    var mapSelectedPosition by remember { mutableStateOf<com\.google\.android\.gms\.maps\.model\.LatLng\?>\(null\) }\n",
    "",
    content
)

# 2. Remove PIN ON MAP box
map_ui_target = """        Text("PIN ON MAP", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 6.dp))
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
        
"""
content = content.replace(map_ui_target, "")

# 3. Remove lat and lng from MatchEntity constructor
match_entity_target = """                    posterTrust = 0.0,
                    lat = mapSelectedPosition?.latitude ?: 0.0,
                    lng = mapSelectedPosition?.longitude ?: 0.0
                )"""
match_entity_replace = """                    posterTrust = 0.0
                )"""
content = content.replace(match_entity_target, match_entity_replace)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
