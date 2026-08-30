import re

def patch_app_screens():
    with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
        content = f.read()

    target = """            if (match.posterImageBase64.isNotEmpty()) {
                val imageBytes = android.util.Base64.decode(match.posterImageBase64, android.util.Base64.DEFAULT)
                val bitmap = android.graphics.BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
                androidx.compose.foundation.Image(
                    bitmap = bitmap.asImageBitmap(),
                    contentDescription = null,
                    modifier = Modifier.size(44.dp).clip(CircleShape),
                    contentScale = androidx.compose.ui.layout.ContentScale.Crop
                )
            } else {"""
            
    repl = """            val bitmap = androidx.compose.runtime.remember(match.posterImageBase64) {
                if (match.posterImageBase64.isNotEmpty()) {
                    try {
                        val imageBytes = android.util.Base64.decode(match.posterImageBase64, android.util.Base64.DEFAULT)
                        android.graphics.BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
                    } catch (e: Exception) {
                        null
                    }
                } else null
            }
            if (bitmap != null) {
                androidx.compose.foundation.Image(
                    bitmap = bitmap.asImageBitmap(),
                    contentDescription = null,
                    modifier = Modifier.size(44.dp).clip(CircleShape),
                    contentScale = androidx.compose.ui.layout.ContentScale.Crop
                )
            } else {"""
            
    content = content.replace(target, repl)
    with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
        f.write(content)

def patch_main_activity():
    with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
        content = f.read()

    target = """            if (m.posterImageBase64.isNotEmpty()) {
                val imageBytes = android.util.Base64.decode(m.posterImageBase64, android.util.Base64.DEFAULT)
                val bitmap = android.graphics.BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
                androidx.compose.foundation.Image(
                    bitmap = bitmap.asImageBitmap(),
                    contentDescription = null,
                    modifier = Modifier.size(26.dp).clip(CircleShape),
                    contentScale = androidx.compose.ui.layout.ContentScale.Crop
                )
            } else {"""
            
    repl = """            val bitmap = androidx.compose.runtime.remember(m.posterImageBase64) {
                if (m.posterImageBase64.isNotEmpty()) {
                    try {
                        val imageBytes = android.util.Base64.decode(m.posterImageBase64, android.util.Base64.DEFAULT)
                        android.graphics.BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
                    } catch (e: Exception) {
                        null
                    }
                } else null
            }
            if (bitmap != null) {
                androidx.compose.foundation.Image(
                    bitmap = bitmap.asImageBitmap(),
                    contentDescription = null,
                    modifier = Modifier.size(26.dp).clip(CircleShape),
                    contentScale = androidx.compose.ui.layout.ContentScale.Crop
                )
            } else {"""
            
    content = content.replace(target, repl)
    with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
        f.write(content)

patch_app_screens()
patch_main_activity()
