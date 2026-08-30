import re

with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target = """        Row(modifier = Modifier.fillMaxWidth().clickable { if (match.posterId.isNotEmpty()) onPosterClick(match.posterId) }.padding(bottom = 18.dp, top = 8.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.size(44.dp).clip(CircleShape).background(Turf2), contentAlignment = Alignment.Center) {
                Text(match.posterName.first().toString(), color = Floodlight, fontSize = 18.sp, fontWeight = FontWeight.Bold)
            }
            Spacer(modifier = Modifier.width(10.dp))"""

repl = """        Row(modifier = Modifier.fillMaxWidth().clickable { if (match.posterId.isNotEmpty()) onPosterClick(match.posterId) }.padding(bottom = 18.dp, top = 8.dp), verticalAlignment = Alignment.CenterVertically) {
            if (match.posterImageBase64.isNotEmpty()) {
                val imageBytes = android.util.Base64.decode(match.posterImageBase64, android.util.Base64.DEFAULT)
                val bitmap = android.graphics.BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
                androidx.compose.foundation.Image(
                    bitmap = androidx.compose.ui.graphics.asImageBitmap(bitmap),
                    contentDescription = null,
                    modifier = Modifier.size(44.dp).clip(CircleShape),
                    contentScale = androidx.compose.ui.layout.ContentScale.Crop
                )
            } else {
                Box(modifier = Modifier.size(44.dp).clip(CircleShape).background(Turf2), contentAlignment = Alignment.Center) {
                    Text(match.posterName.first().toString(), color = Floodlight, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                }
            }
            Spacer(modifier = Modifier.width(10.dp))"""

content = content.replace(target, repl)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
