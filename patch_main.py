import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """        if (errorMessage.isNotEmpty()) {
            Spacer(modifier = Modifier.height(16.dp))
            Text(errorMessage, color = Whistle, fontSize = 14.sp)
        }

        Spacer(modifier = Modifier.height(32.dp))"""

replacement = """        if (errorMessage.isNotEmpty()) {
            Spacer(modifier = Modifier.height(16.dp))
            Text(errorMessage, color = Whistle, fontSize = 14.sp)
        }

        if (!isSignUp) {
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

        Spacer(modifier = Modifier.height(16.dp))"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
        f.write(content)
    print("Success")
else:
    print("Target not found")
