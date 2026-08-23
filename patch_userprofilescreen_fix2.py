with open("app/src/main/java/com/example/UserProfileScreen.kt", "r") as f:
    content = f.read()

target = """androidx.compose.foundation.Image(bitmap = androidx.compose.ui.graphics.asImageBitmap(bitmap), contentDescription = "Profile Photo", modifier = Modifier.fillMaxSize(), contentScale = androidx.compose.ui.layout.ContentScale.Crop)"""
replacement = """androidx.compose.foundation.Image(bitmap = bitmap.asImageBitmap(), contentDescription = "Profile Photo", modifier = Modifier.fillMaxSize(), contentScale = androidx.compose.ui.layout.ContentScale.Crop)"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/UserProfileScreen.kt", "w") as f:
    f.write(content)
