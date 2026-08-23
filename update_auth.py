import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Replace the navigation in MaidanApp
nav_old = """            currentScreen == "phone" -> PhoneScreen(
                method = method,
                onMethodChange = { method = it },
                contact = contact,
                onContactChange = { contact = it },
                onNext = { currentScreen = "otp" }
            )
            currentScreen == "otp" -> OtpScreen(
                contact = contact,
                otp = otp,
                onOtpChange = { otp = it },
                onBack = { currentScreen = "phone" },
                onNext = { currentScreen = "profileSetup" }
            )"""

nav_new = """            currentScreen == "phone" -> AuthScreen(
                viewModel = viewModel,
                onAuthSuccess = { isNewUser ->
                    if (isNewUser) currentScreen = "profileSetup"
                    else currentScreen = "main"
                }
            )"""

content = content.replace(nav_old, nav_new)

# Now remove PhoneScreen, MethodButton, OtpScreen
start_idx = content.find("@Composable\nfun PhoneScreen(")
end_idx = content.find("@OptIn(ExperimentalLayoutApi::class)\n@Composable\nfun ProfileSetupScreen")

if start_idx != -1 and end_idx != -1:
    auth_screen_code = """@Composable
fun AuthScreen(viewModel: MaidanViewModel, onAuthSuccess: (Boolean) -> Unit) {
    var isSignUp by remember { mutableStateOf(false) }
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
            text = if (isSignUp) "Create Account" else "Welcome Back",
            color = Chalk,
            fontSize = 32.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(bottom = 8.dp)
        )
        Text(
            text = if (isSignUp) "Sign up to join the game." else "Sign in to continue.",
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

        Spacer(modifier = Modifier.height(32.dp))

        Button(
            onClick = {
                if (email.isBlank() || password.isBlank()) {
                    errorMessage = "Please enter email and password"
                    return@Button
                }
                isLoading = true
                errorMessage = ""
                if (isSignUp) {
                    viewModel.signUp(email.trim(), password.trim(), onSuccess = {
                        isLoading = false
                        onAuthSuccess(true)
                    }, onError = {
                        isLoading = false
                        errorMessage = it
                    })
                } else {
                    viewModel.signIn(email.trim(), password.trim(), onSuccess = {
                        isLoading = false
                        onAuthSuccess(false)
                    }, onError = {
                        isLoading = false
                        errorMessage = it
                    })
                }
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
                Text(if (isSignUp) "Sign Up" else "Sign In", fontSize = 18.sp, fontWeight = FontWeight.Bold)
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        TextButton(onClick = { 
            isSignUp = !isSignUp 
            errorMessage = ""
        }) {
            Text(
                if (isSignUp) "Already have an account? Sign In" else "Don't have an account? Sign Up",
                color = Bench
            )
        }
    }
}

"""
    content = content[:start_idx] + auth_screen_code + content[end_idx:]

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

print("Done")
