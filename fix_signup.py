import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Add setupPassword state
if "var setupPassword by remember" not in content:
    content = content.replace('var otp by remember { mutableStateOf("") }', 'var otp by remember { mutableStateOf("") }\n    var setupPassword by remember { mutableStateOf("") }')

# 2. Update ProfileSetupScreen call
target = """            currentScreen == "profileSetup" -> ProfileSetupScreen(
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

replacement = """            currentScreen == "profileSetup" -> ProfileSetupScreen(
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
                            // If user exists or failed, just login and proceed
                            viewModel.signIn(
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
                    )
                }
            )"""

content = content.replace(target, replacement)

# 3. Update ProfileSetupScreen signature
target_sig = """fun ProfileSetupScreen(
    name: String, onNameChange: (String) -> Unit,
    age: String, onAgeChange: (String) -> Unit,
    gender: String, onGenderChange: (String) -> Unit,
    selectedSports: List<String>, onToggleSport: (String) -> Unit,
    onBack: () -> Unit, onNext: () -> Unit
)"""

replacement_sig = """fun ProfileSetupScreen(
    name: String, onNameChange: (String) -> Unit,
    age: String, onAgeChange: (String) -> Unit,
    gender: String, onGenderChange: (String) -> Unit,
    selectedSports: List<String>, onToggleSport: (String) -> Unit,
    password: String = "", onPasswordChange: (String) -> Unit = {},
    onBack: () -> Unit, onNext: () -> Unit
)"""
content = content.replace(target_sig, replacement_sig)

# 4. Add password field
target_btn = """        Spacer(modifier = Modifier.weight(1f))
        
        Button(
            onClick = onNext,"""

replacement_btn = """        Spacer(modifier = Modifier.weight(1f))
        
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
content = content.replace(target_btn, replacement_btn)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

print("Updated ProfileSetupScreen and signup flow")
