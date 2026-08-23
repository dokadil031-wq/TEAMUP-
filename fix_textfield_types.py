import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Fix contact checks
content = content.replace('if (contact.startsWith', 'if (contact.text.startsWith')
content = content.replace('if (contact.contains', 'if (contact.text.contains')
content = content.replace('contact@maidan.app', '${contact.text}@maidan.app')
content = content.replace('val actualEmail = if (contact.text.contains("@")) contact else "$contact.text@maidan.app"', 'val actualEmail = if (contact.text.contains("@")) contact.text else "${contact.text}@maidan.app"')

# Fix password checks in setup
content = content.replace('if (setupPassword.isNotBlank()) setupPassword else "maidan123"', 'if (setupPassword.text.isNotBlank()) setupPassword.text else "maidan123"')

# Fix saveUserProfile
content = content.replace('viewModel.saveUserProfile(name, age, gender, selectedSports.toList())', 'viewModel.saveUserProfile(name.text, age.text, gender.text, selectedSports.toList())')

# Fix otp checks
content = content.replace('val credential = PhoneAuthProvider.getCredential(verificationId, otp)', 'val credential = PhoneAuthProvider.getCredential(verificationId, otp.text)')
content = content.replace('if (otp.length < 6)', 'if (otp.text.length < 6)')
content = content.replace('if (setupPassword.length < 6)', 'if (setupPassword.text.length < 6)')
content = content.replace('if (otp.length', 'if (otp.text.length')

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
