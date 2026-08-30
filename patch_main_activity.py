import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                    val credential = PhoneAuthProvider.getCredential(verificationId, otp)
                    viewModel.auth.signInWithCredential(credential)
                        .addOnCompleteListener(activity) { task ->
                            if (task.isSuccessful) {
                                currentScreen = "profileSetup"
                            } else {
                                Toast.makeText(activity, "Invalid OTP", Toast.LENGTH_SHORT).show()
                            }
                        }"""

repl = """                    val credential = PhoneAuthProvider.getCredential(verificationId, otp)
                    viewModel.auth.signInWithCredential(credential)
                        .addOnCompleteListener(activity) { task ->
                            if (task.isSuccessful) {
                                val isNew = task.result?.additionalUserInfo?.isNewUser ?: false
                                if (isNew) {
                                    currentScreen = "profileSetup"
                                } else {
                                    currentScreen = "main"
                                }
                            } else {
                                Toast.makeText(activity, "Invalid OTP", Toast.LENGTH_SHORT).show()
                            }
                        }"""

content = content.replace(target, repl)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
