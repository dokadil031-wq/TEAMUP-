import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Update the MaidanApp states
# Change default to auth
content = content.replace('var currentScreen by remember { mutableStateOf("phone") }', 'var currentScreen by remember { mutableStateOf("auth") }')

# 2. Change MaidanApp when block
maidan_app_old = """    Box(
        modifier = modifier
            .fillMaxSize()
            .background(Pitch)
    ) {
        when {
            currentScreen == "phone" -> AuthScreen(
                viewModel = viewModel,
                onAuthSuccess = { isNewUser ->
                    if (isNewUser) currentScreen = "profileSetup"
                    else currentScreen = "main"
                }
            )
            currentScreen == "profileSetup" -> ProfileSetupScreen("""

maidan_app_new = """    var setupPassword by remember { mutableStateOf("") }
    Box(
        modifier = modifier
            .fillMaxSize()
            .background(Pitch)
    ) {
        when {
            currentScreen == "auth" -> AuthScreen(
                viewModel = viewModel,
                onAuthSuccess = { isNewUser ->
                    if (isNewUser) currentScreen = "profileSetup"
                    else currentScreen = "main"
                },
                onSignUpClick = { currentScreen = "phone" }
            )
            currentScreen == "phone" -> PhoneScreen(
                method = method,
                onMethodChange = { method = it },
                contact = contact,
                onContactChange = { contact = it },
                onNext = { currentScreen = "otp" },
                onSignInClick = { currentScreen = "auth" }
            )
            currentScreen == "otp" -> OtpScreen(
                contact = contact,
                otp = otp,
                onOtpChange = { otp = it },
                onBack = { currentScreen = "phone" },
                onNext = { currentScreen = "profileSetup" }
            )
            currentScreen == "profileSetup" -> ProfileSetupScreen("""

content = content.replace(maidan_app_old, maidan_app_new)

# 3. Update ProfileSetupScreen call inside MaidanApp
profile_setup_call_old = """            currentScreen == "profileSetup" -> ProfileSetupScreen(
                name = name,
                onNameChange = { name = it },
                age = age,
                onAgeChange = { age = it },
                gender = gender,
                onGenderChange = { gender = it },
                selectedSports = selectedSports,
                onToggleSport = {
                    if (selectedSports.contains(it)) selectedSports.remove(it)
                    else selectedSports.add(it)
                },
                onBack = { currentScreen = "otp" },
                onNext = { 
                    viewModel.saveUserProfile(name, age, gender, selectedSports.toList())
                    currentScreen = "main" 
                }
            )"""

profile_setup_call_new = """            currentScreen == "profileSetup" -> ProfileSetupScreen(
                name = name,
                onNameChange = { name = it },
                age = age,
                onAgeChange = { age = it },
                gender = gender,
                onGenderChange = { gender = it },
                selectedSports = selectedSports,
                onToggleSport = {
                    if (selectedSports.contains(it)) selectedSports.remove(it)
                    else selectedSports.add(it)
                },
                password = setupPassword,
                onPasswordChange = { setupPassword = it },
                onBack = { currentScreen = "otp" },
                onNext = { 
                    val actualEmail = if (contact.contains("@")) contact else "$contact@maidan.app"
                    val actualPass = if (setupPassword.isNotBlank()) setupPassword else "maidan123"
                    viewModel.signUp(
                        email = actualEmail,
                        pass = actualPass,
                        onSuccess = {
                            viewModel.saveUserProfile(name, age, gender, selectedSports.toList())
                            currentScreen = "main"
                        },
                        onError = {
                            viewModel.saveUserProfile(name, age, gender, selectedSports.toList())
                            currentScreen = "main"
                        }
                    )
                }
            )"""

content = content.replace(profile_setup_call_old, profile_setup_call_new)

# 4. Modify AuthScreen signature and behavior
auth_sig_old = "fun AuthScreen(viewModel: MaidanViewModel, onAuthSuccess: (Boolean) -> Unit) {"
auth_sig_new = "fun AuthScreen(viewModel: MaidanViewModel, onAuthSuccess: (Boolean) -> Unit, onSignUpClick: () -> Unit) {"
content = content.replace(auth_sig_old, auth_sig_new)

auth_screen_body_old = """    var isSignUp by remember { mutableStateOf(false) }
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
        )"""

auth_screen_body_new = """    var email by remember { mutableStateOf("") }
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
        )"""
content = content.replace(auth_screen_body_old, auth_screen_body_new)

auth_button_action_old = """                if (isSignUp) {
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
                }"""
auth_button_action_new = """                viewModel.signIn(email.trim(), password.trim(), onSuccess = {
                    isLoading = false
                    onAuthSuccess(false)
                }, onError = {
                    isLoading = false
                    errorMessage = it
                })"""
content = content.replace(auth_button_action_old, auth_button_action_new)

auth_button_text_old = """Text(if (isSignUp) "Sign Up" else "Sign In", fontSize = 18.sp, fontWeight = FontWeight.Bold)"""
auth_button_text_new = """Text("Sign In", fontSize = 18.sp, fontWeight = FontWeight.Bold)"""
content = content.replace(auth_button_text_old, auth_button_text_new)

auth_toggle_old = """        if (!isSignUp) {
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
        }

        Spacer(modifier = Modifier.height(16.dp))

        TextButton(onClick = { 
            isSignUp = !isSignUp 
            errorMessage = ""
        }) {
            Text(
                if (isSignUp) "Already have an account? Sign In" else "Don't have an account? Sign Up",
                color = Bench
            )
        }"""
auth_toggle_new = """        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
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

        TextButton(onClick = onSignUpClick) {
            Text(
                "Don't have an account? Sign Up",
                color = Bench
            )
        }"""
content = content.replace(auth_toggle_old, auth_toggle_new)


# 5. Append PhoneScreen, OtpScreen, MethodButton
extra_screens = """
@Composable
fun PhoneScreen(
    method: String,
    onMethodChange: (String) -> Unit,
    contact: String,
    onContactChange: (String) -> Unit,
    onNext: () -> Unit,
    onSignInClick: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(26.dp)
    ) {
        StepDots(0)
        Text(
            text = "Someone's always\\nshort a player.",
            color = Chalk,
            fontSize = 34.sp,
            fontWeight = FontWeight.Bold,
            lineHeight = 40.sp,
            modifier = Modifier.padding(bottom = 10.dp)
        )
        Text(
            text = "Post your game. Find your squad. Play today.",
            color = Bench,
            fontSize = 15.sp,
            modifier = Modifier.padding(bottom = 28.dp)
        )
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(Turf2, RoundedCornerShape(12.dp))
                .padding(4.dp)
        ) {
            MethodButton(
                text = "Phone",
                icon = Icons.Default.Phone,
                isSelected = method == "phone",
                onClick = { onMethodChange("phone") },
                modifier = Modifier.weight(1f)
            )
            MethodButton(
                text = "Email",
                icon = Icons.Default.Email,
                isSelected = method == "email",
                onClick = { onMethodChange("email") },
                modifier = Modifier.weight(1f)
            )
        }
        Spacer(modifier = Modifier.height(16.dp))
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, Line, RoundedCornerShape(12.dp))
                .background(Turf2, RoundedCornerShape(12.dp))
                .padding(horizontal = 14.dp, vertical = 2.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            if (method == "phone") {
                Text("+91", color = Bench, modifier = Modifier.padding(end = 8.dp))
            }
            TextField(
                value = contact,
                onValueChange = onContactChange,
                placeholder = { Text(if (method == "phone") "98765 43210" else "you@email.com", color = Bench) },
                colors = TextFieldDefaults.colors(
                    focusedContainerColor = Color.Transparent,
                    unfocusedContainerColor = Color.Transparent,
                    focusedIndicatorColor = Color.Transparent,
                    unfocusedIndicatorColor = Color.Transparent,
                    focusedTextColor = Chalk,
                    unfocusedTextColor = Chalk,
                    cursorColor = Floodlight
                ),
                keyboardOptions = KeyboardOptions(keyboardType = if (method == "phone") KeyboardType.Phone else KeyboardType.Email),
                modifier = Modifier.weight(1f)
            )
        }
        Spacer(modifier = Modifier.height(24.dp))
        Button(
            onClick = onNext,
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Floodlight, contentColor = Pitch),
            shape = RoundedCornerShape(12.dp)
        ) {
            Text("Continue", fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }
        
        Spacer(modifier = Modifier.weight(1f))
        
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.Center) {
            TextButton(onClick = onSignInClick) {
                Text("Already have an account? Sign In", color = Bench)
            }
        }
    }
}

@Composable
fun MethodButton(text: String, icon: androidx.compose.ui.graphics.vector.ImageVector, isSelected: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier) {
    val bg = if (isSelected) Floodlight else Color.Transparent
    val color = if (isSelected) Pitch else Bench
    Row(
        horizontalArrangement = Arrangement.Center,
        verticalAlignment = Alignment.CenterVertically,
        modifier = modifier
            .clip(RoundedCornerShape(9.dp))
            .background(bg)
            .clickable(onClick = onClick)
            .padding(vertical = 10.dp)
    ) {
        Icon(icon, contentDescription = null, tint = color, modifier = Modifier.size(15.dp))
        Spacer(modifier = Modifier.width(6.dp))
        Text(text, color = color, fontWeight = FontWeight.SemiBold, fontSize = 14.sp)
    }
}

@Composable
fun OtpScreen(
    contact: String,
    otp: String,
    onOtpChange: (String) -> Unit,
    onBack: () -> Unit,
    onNext: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(26.dp)
    ) {
        IconButton(onClick = onBack, modifier = Modifier.padding(bottom = 18.dp)) {
            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Bench)
        }
        StepDots(1)
        Text("Enter the code", color = Chalk, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp, modifier = Modifier.padding(bottom = 8.dp))
        Text("Sent to ${if (contact.isEmpty()) "your number" else contact}", color = Bench, fontSize = 14.sp, modifier = Modifier.padding(bottom = 28.dp))
        
        TextField(
            value = otp,
            onValueChange = { if (it.length <= 4) onOtpChange(it) },
            placeholder = { Text("0000", color = Bench) },
            colors = TextFieldDefaults.colors(
                focusedContainerColor = Color.Transparent,
                unfocusedContainerColor = Color.Transparent,
                focusedIndicatorColor = Line,
                unfocusedIndicatorColor = Line,
                focusedTextColor = Chalk,
                unfocusedTextColor = Chalk,
                cursorColor = Floodlight
            ),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            modifier = Modifier.fillMaxWidth(),
            textStyle = androidx.compose.ui.text.TextStyle(fontSize = 24.sp, letterSpacing = 8.sp, textAlign = TextAlign.Center)
        )
        Spacer(modifier = Modifier.height(32.dp))
        Button(
            onClick = onNext,
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Floodlight, contentColor = Pitch),
            shape = RoundedCornerShape(12.dp)
        ) {
            Text("Verify", fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }
    }
}
"""

content += extra_screens

# 6. Finally, update ProfileSetupScreen signature to take password
profile_setup_sig_old = """@OptIn(ExperimentalLayoutApi::class)
@Composable
fun ProfileSetupScreen(
    name: String, onNameChange: (String) -> Unit,
    age: String, onAgeChange: (String) -> Unit,
    gender: String, onGenderChange: (String) -> Unit,
    selectedSports: List<String>, onToggleSport: (String) -> Unit,
    onBack: () -> Unit, onNext: () -> Unit
) {"""

profile_setup_sig_new = """@OptIn(ExperimentalLayoutApi::class)
@Composable
fun ProfileSetupScreen(
    name: String, onNameChange: (String) -> Unit,
    age: String, onAgeChange: (String) -> Unit,
    gender: String, onGenderChange: (String) -> Unit,
    selectedSports: List<String>, onToggleSport: (String) -> Unit,
    password: String = "", onPasswordChange: (String) -> Unit = {},
    onBack: () -> Unit, onNext: () -> Unit
) {"""
content = content.replace(profile_setup_sig_old, profile_setup_sig_new)

# Add password field at the end of ProfileSetupScreen
profile_setup_btn_old = """        Spacer(modifier = Modifier.weight(1f))
        
        Button(
            onClick = onNext,"""

profile_setup_btn_new = """        Spacer(modifier = Modifier.weight(1f))
        
        Text("Create Password", color = Chalk, fontSize = 14.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 8.dp, top = 16.dp))
        TextField(
            value = password,
            onValueChange = onPasswordChange,
            placeholder = { Text("At least 6 characters", color = Bench) },
            colors = TextFieldDefaults.colors(
                focusedContainerColor = Color.Transparent,
                unfocusedContainerColor = Color.Transparent,
                focusedIndicatorColor = Floodlight,
                unfocusedIndicatorColor = Line,
                focusedTextColor = Chalk,
                unfocusedTextColor = Chalk
            ),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
            modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp)
        )
        
        Button(
            onClick = onNext,"""
content = content.replace(profile_setup_btn_old, profile_setup_btn_new)


with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
print("Updated successfully")
