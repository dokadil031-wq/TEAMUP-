import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

profile_setup_start = content.find("fun ProfileSetupScreen(")
profile_setup_end = content.find("fun AuthScreen(", profile_setup_start)
if profile_setup_end == -1:
    profile_setup_end = len(content)

original_fun = content[profile_setup_start:profile_setup_end]

# We will completely replace ProfileSetupScreen
replacement = """fun ProfileSetupScreen(
    name: String, onNameChange: (String) -> Unit,
    age: String, onAgeChange: (String) -> Unit,
    gender: String, onGenderChange: (String) -> Unit,
    selectedSports: List<String>, onToggleSport: (String) -> Unit,
    password: String = "", onPasswordChange: (String) -> Unit = {},
    onBack: () -> Unit, onNext: () -> Unit,
    photoBase64: String = "", onPhotoCaptured: (String) -> Unit = {}
) {
    val sportsList = listOf("Cricket", "Football", "Badminton", "Basketball", "Volleyball", "Table tennis", "Running", "Gym", "Online gaming", "Exercise")
    
    val context = androidx.compose.ui.platform.LocalContext.current
    
    val launcher = androidx.activity.compose.rememberLauncherForActivityResult(
        contract = androidx.activity.result.contract.ActivityResultContracts.TakePicturePreview()
    ) { bitmap: android.graphics.Bitmap? ->
        if (bitmap != null) {
            val outputStream = java.io.ByteArrayOutputStream()
            bitmap.compress(android.graphics.Bitmap.CompressFormat.JPEG, 80, outputStream)
            val byteArray = outputStream.toByteArray()
            val base64 = android.util.Base64.encodeToString(byteArray, android.util.Base64.DEFAULT)
            onPhotoCaptured(base64)
        }
    }

    val cameraPermissionLauncher = androidx.activity.compose.rememberLauncherForActivityResult(
        contract = androidx.activity.result.contract.ActivityResultContracts.RequestPermission()
    ) { isGranted: Boolean ->
        if (isGranted) {
            launcher.launch(null)
        }
    }
    
    val canProceed = name.isNotBlank() && age.isNotBlank() && photoBase64.isNotBlank()
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(26.dp)
            .verticalScroll(rememberScrollState())
    ) {
        IconButton(onClick = onBack, modifier = Modifier.padding(bottom = 18.dp)) {
            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Bench)
        }
        StepDots(2)
        Text("Build your profile", color = Chalk, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp, modifier = Modifier.padding(bottom = 16.dp))
        
        Text("Take a live photo for your profile (Required)", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 8.dp))
        Box(
            modifier = Modifier
                .size(100.dp)
                .clip(CircleShape)
                .background(Turf2)
                .border(2.dp, if (photoBase64.isEmpty()) Line else Floodlight, CircleShape)
                .clickable {
                    if (androidx.core.content.ContextCompat.checkSelfPermission(context, android.Manifest.permission.CAMERA) == android.content.pm.PackageManager.PERMISSION_GRANTED) {
                        launcher.launch(null)
                    } else {
                        cameraPermissionLauncher.launch(android.Manifest.permission.CAMERA)
                    }
                }
                .align(Alignment.CenterHorizontally)
                .padding(bottom = 16.dp),
            contentAlignment = Alignment.Center
        ) {
            if (photoBase64.isNotEmpty()) {
                val imageBytes = android.util.Base64.decode(photoBase64, android.util.Base64.DEFAULT)
                val bitmap = android.graphics.BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
                if (bitmap != null) {
                    androidx.compose.foundation.Image(
                        bitmap = bitmap.asImageBitmap(),
                        contentDescription = "Profile Photo",
                        modifier = Modifier.fillMaxSize().clip(CircleShape),
                        contentScale = ContentScale.Crop
                    )
                }
            } else {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Default.Add, contentDescription = "Take Photo", tint = Bench)
                    Text("Camera", color = Bench, fontSize = 10.sp)
                }
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        OutlinedTextField(
            value = name,
            onValueChange = onNameChange,
            label = { Text("Full Name") },
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = Floodlight,
                focusedLabelColor = Floodlight,
                unfocusedBorderColor = Line,
                unfocusedLabelColor = Bench,
                focusedTextColor = Chalk,
                unfocusedTextColor = Chalk
            ),
            modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp)
        )
        
        Row(modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            OutlinedTextField(
                value = age,
                onValueChange = onAgeChange,
                label = { Text("Age") },
                singleLine = true, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = Floodlight,
                    focusedLabelColor = Floodlight,
                    unfocusedBorderColor = Line,
                    unfocusedLabelColor = Bench,
                    focusedTextColor = Chalk,
                    unfocusedTextColor = Chalk
                ),
                modifier = Modifier.weight(1f)
            )
            OutlinedTextField(
                value = gender,
                onValueChange = onGenderChange,
                label = { Text("Gender") },
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = Floodlight,
                    focusedLabelColor = Floodlight,
                    unfocusedBorderColor = Line,
                    unfocusedLabelColor = Bench,
                    focusedTextColor = Chalk,
                    unfocusedTextColor = Chalk
                ),
                modifier = Modifier.weight(1f)
            )
        }
        
        Text("FAVORITE SPORTS", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 8.dp))
        @OptIn(ExperimentalLayoutApi::class)
        FlowRow(modifier = Modifier.fillMaxWidth().padding(bottom = 24.dp), horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            sportsList.forEach { s ->
                val isSelected = selectedSports.contains(s)
                Box(
                    modifier = Modifier.clip(RoundedCornerShape(10.dp))
                        .background(if (isSelected) Floodlight else Turf2)
                        .border(if (isSelected) 0.dp else 1.dp, if (isSelected) Color.Transparent else Line, RoundedCornerShape(10.dp))
                        .clickable { onToggleSport(s) }
                        .padding(horizontal = 14.dp, vertical = 8.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(s, color = if (isSelected) Pitch else Chalk, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                }
            }
        }
        
        OutlinedTextField(
            value = password,
            onValueChange = onPasswordChange,
            label = { Text("Password (for next login)") },
            visualTransformation = androidx.compose.ui.text.input.PasswordVisualTransformation(),
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = Floodlight,
                focusedLabelColor = Floodlight,
                unfocusedBorderColor = Line,
                unfocusedLabelColor = Bench,
                focusedTextColor = Chalk,
                unfocusedTextColor = Chalk
            ),
            modifier = Modifier.fillMaxWidth().padding(bottom = 26.dp)
        )
        
        Button(
            onClick = onNext,
            enabled = canProceed,
            colors = ButtonDefaults.buttonColors(containerColor = Floodlight, contentColor = Pitch, disabledContainerColor = Turf2, disabledContentColor = Bench),
            modifier = Modifier.fillMaxWidth().height(50.dp),
            shape = RoundedCornerShape(12.dp)
        ) {
            Text(if (photoBase64.isEmpty()) "Take Photo to Continue" else "Complete Profile", fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }
    }
}
@Composable
"""

# replace up to AuthScreen
final_content = content[:profile_setup_start] + replacement + content[profile_setup_end-11:]

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(final_content)
