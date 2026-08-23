with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target = """fun ProfileScreen(viewModel: MaidanViewModel, onEditProfileClick: () -> Unit = {}, onLogoutClick: () -> Unit = {}) {
    val userName by viewModel.userName.collectAsStateWithLifecycle()
    val userAge by viewModel.userAge.collectAsStateWithLifecycle()
    val userGender by viewModel.userGender.collectAsStateWithLifecycle()
    val userSports by viewModel.userSports.collectAsStateWithLifecycle()

    Column(modifier = Modifier.fillMaxSize().padding(horizontal = 22.dp, vertical = 16.dp)) {
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End, verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.clip(RoundedCornerShape(20.dp)).border(1.dp, Line, RoundedCornerShape(20.dp)).clickable { onEditProfileClick() }.padding(horizontal = 12.dp, vertical = 6.dp)) {
                Text("Edit profile", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
            }
            Spacer(modifier = Modifier.width(8.dp))
            Box(modifier = Modifier.clip(RoundedCornerShape(20.dp)).border(1.dp, Color(0xFFEF4444), RoundedCornerShape(20.dp)).clickable { onLogoutClick() }.padding(horizontal = 12.dp, vertical = 6.dp)) {
                Text("Logout", color = Color(0xFFEF4444), fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
            }
        }
        
        Column(modifier = Modifier.fillMaxWidth().padding(bottom = 22.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Box(modifier = Modifier.size(72.dp).clip(CircleShape).background(Turf2), contentAlignment = Alignment.Center) {
                Text(if (userName.isNotEmpty()) userName.first().toString() else "Y", color = Floodlight, fontSize = 30.sp, fontWeight = FontWeight.ExtraBold)
            }"""

replacement = """fun ProfileScreen(viewModel: MaidanViewModel, onEditProfileClick: () -> Unit = {}, onLogoutClick: () -> Unit = {}) {
    val userName by viewModel.userName.collectAsStateWithLifecycle()
    val userAge by viewModel.userAge.collectAsStateWithLifecycle()
    val userGender by viewModel.userGender.collectAsStateWithLifecycle()
    val userSports by viewModel.userSports.collectAsStateWithLifecycle()
    val userImage by viewModel.userImage.collectAsStateWithLifecycle()
    
    val context = LocalContext.current
    val launcher = rememberLauncherForActivityResult(contract = ActivityResultContracts.PickVisualMedia()) { uri: Uri? ->
        uri?.let {
            try {
                val inputStream: InputStream? = context.contentResolver.openInputStream(it)
                val originalBitmap = BitmapFactory.decodeStream(inputStream)
                // Resize and compress
                val maxSize = 400
                val ratio = Math.min(maxSize.toFloat() / originalBitmap.width, maxSize.toFloat() / originalBitmap.height)
                val width = Math.round(ratio * originalBitmap.width)
                val height = Math.round(ratio * originalBitmap.height)
                val resizedBitmap = Bitmap.createScaledBitmap(originalBitmap, width, height, false)
                val outputStream = ByteArrayOutputStream()
                resizedBitmap.compress(Bitmap.CompressFormat.JPEG, 70, outputStream)
                val byteArray = outputStream.toByteArray()
                val base64 = Base64.encodeToString(byteArray, Base64.DEFAULT)
                viewModel.updateProfilePhoto(base64)
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    Column(modifier = Modifier.fillMaxSize().padding(horizontal = 22.dp, vertical = 16.dp)) {
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End, verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.clip(RoundedCornerShape(20.dp)).border(1.dp, Line, RoundedCornerShape(20.dp)).clickable { onEditProfileClick() }.padding(horizontal = 12.dp, vertical = 6.dp)) {
                Text("Edit profile", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
            }
            Spacer(modifier = Modifier.width(8.dp))
            Box(modifier = Modifier.clip(RoundedCornerShape(20.dp)).border(1.dp, Color(0xFFEF4444), RoundedCornerShape(20.dp)).clickable { onLogoutClick() }.padding(horizontal = 12.dp, vertical = 6.dp)) {
                Text("Logout", color = Color(0xFFEF4444), fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
            }
        }
        
        Column(modifier = Modifier.fillMaxWidth().padding(bottom = 22.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Box(
                modifier = Modifier
                    .size(80.dp)
                    .clip(CircleShape)
                    .background(Turf2)
                    .clickable { launcher.launch(androidx.activity.result.PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)) },
                contentAlignment = Alignment.Center
            ) {
                if (userImage.isNotEmpty()) {
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
                } else {
                    Text(if (userName.isNotEmpty()) userName.first().toString() else "Y", color = Floodlight, fontSize = 30.sp, fontWeight = FontWeight.ExtraBold)
                }
            }
            Text("Tap to change photo", color = Bench, fontSize = 10.sp, modifier = Modifier.padding(top = 4.dp))"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
