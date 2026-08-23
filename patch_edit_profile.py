with open("app/src/main/java/com/example/AppScreens.kt", "a") as f:
    f.write('''

@Composable
fun EditProfileScreen(
    name: String, onNameChange: (String) -> Unit,
    age: String, onAgeChange: (String) -> Unit,
    gender: String, onGenderChange: (String) -> Unit,
    viewModel: MaidanViewModel,
    onBack: () -> Unit, onSave: () -> Unit
) {
    var newPassword by remember { mutableStateOf("") }
    var statusMessage by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(26.dp)
            .verticalScroll(rememberScrollState())
    ) {
        IconButton(onClick = onBack, modifier = Modifier.padding(bottom = 18.dp)) {
            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Bench)
        }
        Text("Edit profile", color = Chalk, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp, modifier = Modifier.padding(bottom = 24.dp))
        
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

        Spacer(modifier = Modifier.height(16.dp))
        Text("Change Password", color = Chalk, fontSize = 20.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 12.dp))

        OutlinedTextField(
            value = newPassword,
            onValueChange = { newPassword = it },
            label = { Text("New Password (optional)") },
            visualTransformation = PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = Floodlight,
                focusedLabelColor = Floodlight,
                unfocusedBorderColor = Line,
                unfocusedLabelColor = Bench,
                focusedTextColor = Chalk,
                unfocusedTextColor = Chalk
            ),
            modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)
        )

        if (statusMessage.isNotEmpty()) {
            Text(statusMessage, color = Floodlight, fontSize = 14.sp, modifier = Modifier.padding(bottom = 8.dp))
        }
        
        Button(
            onClick = {
                if (newPassword.isNotBlank()) {
                    viewModel.updatePassword(newPassword) { result ->
                        statusMessage = result
                        if (result.contains("successfully")) {
                            onSave()
                        }
                    }
                } else {
                    onSave()
                }
            },
            colors = ButtonDefaults.buttonColors(containerColor = Whistle, contentColor = Color.White),
            modifier = Modifier.fillMaxWidth().height(50.dp)
        ) {
            Text("Save Changes", fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }
    }
}
''')
