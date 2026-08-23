import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """            value = otp,
            onValueChange = { if (it.length <= 4) onOtpChange(it) },
            placeholder = { Text("0000", color = Bench) },"""

replacement = """            value = otp,
            onValueChange = { if (it.length <= 6) onOtpChange(it) },
            placeholder = { Text("000000", color = Bench) },"""

content = content.replace(target, replacement)

target_verify = """                    if (otp.length < 4) {"""

replacement_verify = """                    if (otp.length < 6) {"""

content = content.replace(target_verify, replacement_verify)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
print("Updated OTP length to 6")
