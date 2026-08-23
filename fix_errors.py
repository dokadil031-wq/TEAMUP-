import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Fix isSignUp unresolved reference. In AuthScreen, there might be remnants of isSignUp.
# Wait, I removed `isSignUp` from `var isSignUp by remember { mutableStateOf(false) }`, but some `Text(if (isSignUp) ... else ...)` might still exist!
# Let's check lines 296, 348, 352.
# Let's just remove `isSignUp` completely from the file.
# If I can't find them, I'll just replace the whole AuthScreen with a clean version.

idx1 = content.find("fun AuthScreen")
idx2 = content.find("fun PhoneScreen")

if idx1 != -1 and idx2 != -1:
    auth_screen_code = """@Composable
fun AuthScreen(viewModel: MaidanViewModel, onAuthSuccess: (Boolean) -> Unit, onSignUpClick: () -> Unit) {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var errorMessage by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(26.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Welcome Back",
            color = Chalk,
            fontSize = 32.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(bottom = 8.dp)
        )
        Text(
            text = "Sign in to continue.",
            color = Bench,
            fontSize = 15.sp,
            modifier = Modifier.padding(bottom = 32.dp)
        )

        OutlinedTextField(
            value = email,
            onValueChange = { email = it },
            label = { Text("Email") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
            modifier = Modifier.fillMaxWidth(),
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = Floodlight,
                focusedLabelColor = Floodlight,
                unfocusedBorderColor = Line,
                unfocusedLabelColor = Bench,
                focusedTextColor = Chalk,
                unfocusedTextColor = Chalk
            )
        )
        
        Spacer(modifier = Modifier.height(16.dp))

        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Password") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
            modifier = Modifier.fillMaxWidth(),
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = Floodlight,
                focusedLabelColor = Floodlight,
                unfocusedBorderColor = Line,
                unfocusedLabelColor = Bench,
                focusedTextColor = Chalk,
                unfocusedTextColor = Chalk
            )
        )

        if (errorMessage.isNotEmpty()) {
            Spacer(modifier = Modifier.height(16.dp))
            Text(errorMessage, color = Whistle, fontSize = 14.sp)
        }

        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
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
        }

        Spacer(modifier = Modifier.height(16.dp))

        Button(
            onClick = {
                if (email.isBlank() || password.isBlank()) {
                    errorMessage = "Please enter email and password"
                    return@Button
                }
                isLoading = true
                errorMessage = ""
                viewModel.signIn(email.trim(), password.trim(), onSuccess = {
                    isLoading = false
                    onAuthSuccess(false)
                }, onError = {
                    isLoading = false
                    errorMessage = it
                })
            },
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Floodlight, contentColor = Pitch),
            shape = RoundedCornerShape(12.dp)
        ) {
            if (isLoading) {
                CircularProgressIndicator(color = Pitch, modifier = Modifier.size(24.dp))
            } else {
                Text("Sign In", fontSize = 18.sp, fontWeight = FontWeight.Bold)
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        TextButton(onClick = onSignUpClick) {
            Text(
                "Don't have an account? Sign Up",
                color = Bench
            )
        }
    }
}
"""
    content = content[:idx1] + auth_screen_code + content[idx2:]

# Also fix Icons.AutoMirrored.Filled.ArrowBack -> Icons.Default.ArrowBack (since the import might not be there)
content = content.replace("Icons.AutoMirrored.Filled.ArrowBack", "Icons.Default.ArrowBack")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
print("Fixed")
