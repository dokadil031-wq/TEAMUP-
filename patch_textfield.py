import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Add import
if "import androidx.compose.ui.text.input.TextFieldValue" not in content:
    content = content.replace("import androidx.compose.ui.text.input.KeyboardType", "import androidx.compose.ui.text.input.KeyboardType\nimport androidx.compose.ui.text.input.TextFieldValue")

# Fix AuthScreen
content = content.replace('var email by remember { mutableStateOf("") }', 'var email by remember { mutableStateOf(TextFieldValue("")) }')
content = content.replace('var password by remember { mutableStateOf("") }', 'var password by remember { mutableStateOf(TextFieldValue("")) }')
content = content.replace('var forgotEmail by remember { mutableStateOf("") }', 'var forgotEmail by remember { mutableStateOf(TextFieldValue("")) }')
content = content.replace('if (email.isBlank())', 'if (email.text.isBlank())')
content = content.replace('viewModel.resetPassword(email.trim())', 'viewModel.resetPassword(email.text.trim())')
content = content.replace('if (forgotEmail.isNotBlank())', 'if (forgotEmail.text.isNotBlank())')
content = content.replace('viewModel.resetPassword(forgotEmail.trim())', 'viewModel.resetPassword(forgotEmail.text.trim())')
content = content.replace('if (email.isBlank() || password.isBlank())', 'if (email.text.isBlank() || password.text.isBlank())')
content = content.replace('viewModel.signIn(email.trim(), password.trim()', 'viewModel.signIn(email.text.trim(), password.text.trim()')

# Fix PhoneScreen
content = content.replace('var contact by remember { mutableStateOf("") }', 'var contact by remember { mutableStateOf(TextFieldValue("")) }')
content = content.replace('onContactChange: (String) -> Unit', 'onContactChange: (TextFieldValue) -> Unit')
content = content.replace('if (contact.isBlank())', 'if (contact.text.isBlank())')
content = content.replace('val contactText = contact.trim()', 'val contactText = contact.text.trim()')

# Fix OtpScreen
content = content.replace('var otp by remember { mutableStateOf("") }', 'var otp by remember { mutableStateOf(TextFieldValue("")) }')
content = content.replace('var setupPassword by remember { mutableStateOf("") }', 'var setupPassword by remember { mutableStateOf(TextFieldValue("")) }')
content = content.replace('if (otp.isBlank())', 'if (otp.text.isBlank())')
content = content.replace('val cred = PhoneAuthProvider.getCredential(verificationId, otp.trim())', 'val cred = PhoneAuthProvider.getCredential(verificationId, otp.text.trim())')
content = content.replace('if (otp.length != 6)', 'if (otp.text.length != 6)')
content = content.replace('if (setupPassword.length < 6)', 'if (setupPassword.text.length < 6)')
content = content.replace('viewModel.linkWithEmail(methodValue, setupPassword.trim()', 'viewModel.linkWithEmail(methodValue, setupPassword.text.trim()')

# Fix ProfileSetupScreen
content = content.replace('var name by remember { mutableStateOf("") }', 'var name by remember { mutableStateOf(TextFieldValue("")) }')
content = content.replace('var age by remember { mutableStateOf("") }', 'var age by remember { mutableStateOf(TextFieldValue("")) }')
content = content.replace('var gender by remember { mutableStateOf("") }', 'var gender by remember { mutableStateOf(TextFieldValue("")) }')
content = content.replace('if (name.isBlank() || age.isBlank() || gender.isBlank())', 'if (name.text.isBlank() || age.text.isBlank() || gender.text.isBlank())')
content = content.replace('viewModel.saveProfile(name.trim(), age.trim(), gender.trim(), emptyList()', 'viewModel.saveProfile(name.text.trim(), age.text.trim(), gender.text.trim(), emptyList()')

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
