with open("app/src/main/java/com/example/UserProfileScreen.kt", "r") as f:
    content = f.read()

target = """            Box(modifier = Modifier.size(60.dp).clip(CircleShape).background(Turf2), contentAlignment = Alignment.Center) {
                if (profile!!.profileImageBase64.isNotEmpty()) {
                    try {
                        val imageBytes = android.util.Base64.decode(profile!!.profileImageBase64, android.util.Base64.DEFAULT)
                        val bitmap = android.graphics.BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
                        if (bitmap != null) {
                            androidx.compose.foundation.Image(bitmap = androidx.compose.ui.graphics.asImageBitmap(bitmap), contentDescription = "Profile Photo", modifier = Modifier.fillMaxSize(), contentScale = androidx.compose.ui.layout.ContentScale.Crop)
                        } else {
                            Text(profile!!.name.firstOrNull()?.toString() ?: "?", color = Floodlight, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                        }
                    } catch (e: Exception) {
                        Text(profile!!.name.firstOrNull()?.toString() ?: "?", color = Floodlight, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                    }
                } else {
                    Text(profile!!.name.firstOrNull()?.toString() ?: "?", color = Floodlight, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                }
            }"""

replacement = """            Box(modifier = Modifier.size(60.dp).clip(CircleShape).background(Turf2), contentAlignment = Alignment.Center) {
                if (profile!!.profileImageBase64.isNotEmpty()) {
                    val bitmap = remember(profile!!.profileImageBase64) {
                        try {
                            val imageBytes = android.util.Base64.decode(profile!!.profileImageBase64, android.util.Base64.DEFAULT)
                            android.graphics.BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
                        } catch (e: Exception) {
                            null
                        }
                    }
                    if (bitmap != null) {
                        androidx.compose.foundation.Image(bitmap = androidx.compose.ui.graphics.asImageBitmap(bitmap), contentDescription = "Profile Photo", modifier = Modifier.fillMaxSize(), contentScale = androidx.compose.ui.layout.ContentScale.Crop)
                    } else {
                        Text(profile!!.name.firstOrNull()?.toString() ?: "?", color = Floodlight, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                    }
                } else {
                    Text(profile!!.name.firstOrNull()?.toString() ?: "?", color = Floodlight, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                }
            }"""

import_target = """import androidx.compose.ui.graphics.Color"""
import_replacement = """import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap"""

content = content.replace(target, replacement).replace(import_target, import_replacement)

with open("app/src/main/java/com/example/UserProfileScreen.kt", "w") as f:
    f.write(content)
