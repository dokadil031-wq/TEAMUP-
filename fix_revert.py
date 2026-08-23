import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace('import androidx.compose.ui.text.input.TextFieldValue\n', '')
content = content.replace('var email by remember { mutableStateOf(TextFieldValue("")) }', 'var email by remember { mutableStateOf("") }')
content = content.replace('var password by remember { mutableStateOf(TextFieldValue("")) }', 'var password by remember { mutableStateOf("") }')
content = content.replace('var forgotEmail by remember { mutableStateOf(TextFieldValue("")) }', 'var forgotEmail by remember { mutableStateOf("") }')
content = content.replace('var contact by remember { mutableStateOf(TextFieldValue("")) }', 'var contact by remember { mutableStateOf("") }')
content = content.replace('var otp by remember { mutableStateOf(TextFieldValue("")) }', 'var otp by remember { mutableStateOf("") }')
content = content.replace('var setupPassword by remember { mutableStateOf(TextFieldValue("")) }', 'var setupPassword by remember { mutableStateOf("") }')
content = content.replace('var name by remember { mutableStateOf(TextFieldValue("")) }', 'var name by remember { mutableStateOf("") }')
content = content.replace('var age by remember { mutableStateOf(TextFieldValue("")) }', 'var age by remember { mutableStateOf("") }')
content = content.replace('var gender by remember { mutableStateOf(TextFieldValue("")) }', 'var gender by remember { mutableStateOf("") }')

content = content.replace('.text', '')

content = content.replace('contact: TextFieldValue', 'contact: String')
content = content.replace('otp: TextFieldValue', 'otp: String')
content = content.replace('name: TextFieldValue', 'name: String')
content = content.replace('age: TextFieldValue', 'age: String')
content = content.replace('gender: TextFieldValue', 'gender: String')
content = content.replace('password: TextFieldValue', 'password: String')

content = content.replace('(TextFieldValue) -> Unit', '(String) -> Unit')

# There were some properties that had .text removed that shouldn't be? No, I only added .text
# Wait, Text("Sign in to continue") -> Text("Sign in to continue") (no .text)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
