import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """        Row(modifier = Modifier.fillMaxWidth().clickable { onPosterClick?.invoke() }.padding(start = 18.dp, top = 14.dp, end = 18.dp, bottom = 10.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.size(26.dp).clip(CircleShape).background(Turf2), contentAlignment = Alignment.Center) {
                Text(m.posterName.firstOrNull()?.toString() ?: "?", color = Floodlight, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }
            Spacer(modifier = Modifier.width(8.dp))"""

repl = """        Row(modifier = Modifier.fillMaxWidth().clickable { onPosterClick?.invoke() }.padding(start = 18.dp, top = 14.dp, end = 18.dp, bottom = 10.dp), verticalAlignment = Alignment.CenterVertically) {
            if (m.posterImageBase64.isNotEmpty()) {
                val imageBytes = android.util.Base64.decode(m.posterImageBase64, android.util.Base64.DEFAULT)
                val bitmap = android.graphics.BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
                androidx.compose.foundation.Image(
                    bitmap = androidx.compose.ui.graphics.asImageBitmap(bitmap),
                    contentDescription = null,
                    modifier = Modifier.size(26.dp).clip(CircleShape),
                    contentScale = androidx.compose.ui.layout.ContentScale.Crop
                )
            } else {
                Box(modifier = Modifier.size(26.dp).clip(CircleShape).background(Turf2), contentAlignment = Alignment.Center) {
                    Text(m.posterName.firstOrNull()?.toString() ?: "?", color = Floodlight, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }
            }
            Spacer(modifier = Modifier.width(8.dp))"""

content = content.replace(target, repl)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
