import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target_auth_state = """    var errorMessage by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }"""

replacement_auth_state = """    var errorMessage by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    var showForgotDialog by remember { mutableStateOf(false) }
    var forgotEmail by remember { mutableStateOf("") }
    val context = androidx.compose.ui.platform.LocalContext.current"""

content = content.replace(target_auth_state, replacement_auth_state)

target_auth_button = """        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
            TextButton(onClick = {
                if (email.isBlank()) {
                    errorMessage = "Please enter your email to reset password"
                } else {
                    isLoading = true
                    viewModel.resetPassword(email.trim()) { msg ->
                        isLoading = false
                        errorMessage = msg
                    }
                }
            }) {
                Text("Forgot Password?", color = Bench, fontSize = 14.sp)
            }
        }"""

replacement_auth_button = """        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
            TextButton(onClick = { showForgotDialog = true }) {
                Text("Forgot Password?", color = Bench, fontSize = 14.sp)
            }
        }
        
        if (showForgotDialog) {
            androidx.compose.material3.AlertDialog(
                onDismissRequest = { showForgotDialog = false },
                title = { Text("Reset Password", color = Chalk) },
                text = {
                    Column {
                        Text("Enter your email address to receive a password reset link.", color = Bench, fontSize = 14.sp, modifier = Modifier.padding(bottom = 16.dp))
                        OutlinedTextField(
                            value = forgotEmail,
                            onValueChange = { forgotEmail = it },
                            label = { Text("Email") },
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedBorderColor = Floodlight,
                                focusedLabelColor = Floodlight,
                                unfocusedBorderColor = Line,
                                unfocusedLabelColor = Bench,
                                focusedTextColor = Chalk,
                                unfocusedTextColor = Chalk
                            ),
                            modifier = Modifier.fillMaxWidth()
                        )
                    }
                },
                confirmButton = {
                    TextButton(onClick = {
                        if (forgotEmail.isNotBlank()) {
                            viewModel.resetPassword(forgotEmail.trim()) { msg ->
                                android.widget.Toast.makeText(context, msg, android.widget.Toast.LENGTH_LONG).show()
                            }
                            showForgotDialog = false
                        } else {
                            android.widget.Toast.makeText(context, "Please enter an email", android.widget.Toast.LENGTH_SHORT).show()
                        }
                    }) {
                        Text("Send Link", color = Floodlight, fontWeight = FontWeight.Bold)
                    }
                },
                dismissButton = {
                    TextButton(onClick = { showForgotDialog = false }) {
                        Text("Cancel", color = Bench)
                    }
                },
                containerColor = Turf,
                titleContentColor = Chalk,
                textContentColor = Bench
            )
        }"""

content = content.replace(target_auth_button, replacement_auth_button)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
