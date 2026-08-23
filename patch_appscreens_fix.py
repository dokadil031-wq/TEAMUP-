with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target = """                if (userImage.isNotEmpty()) {
                    try {
                        val imageBytes = Base64.decode(userImage, Base64.DEFAULT)
                        val bitmap = BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
                        if (bitmap != null) {
                            Image(bitmap = bitmap.asImageBitmap(), contentDescription = "Profile Photo", modifier = Modifier.fillMaxSize(), contentScale = ContentScale.Crop)
                        } else {
                            Text(if (userName.isNotEmpty()) userName.first().toString() else "Y", color = Floodlight, fontSize = 30.sp, fontWeight = FontWeight.ExtraBold)
                        }
                    } catch (e: Exception) {
                        Text(if (userName.isNotEmpty()) userName.first().toString() else "Y", color = Floodlight, fontSize = 30.sp, fontWeight = FontWeight.ExtraBold)
                    }
                } else {"""

replacement = """                if (userImage.isNotEmpty()) {
                    val bitmap = remember(userImage) {
                        try {
                            val imageBytes = Base64.decode(userImage, Base64.DEFAULT)
                            BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
                        } catch (e: Exception) {
                            null
                        }
                    }
                    if (bitmap != null) {
                        Image(bitmap = bitmap.asImageBitmap(), contentDescription = "Profile Photo", modifier = Modifier.fillMaxSize(), contentScale = ContentScale.Crop)
                    } else {
                        Text(if (userName.isNotEmpty()) userName.first().toString() else "Y", color = Floodlight, fontSize = 30.sp, fontWeight = FontWeight.ExtraBold)
                    }
                } else {"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
