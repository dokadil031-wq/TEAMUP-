import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Fix OtpScreen button
idx_otp = content.find("fun OtpScreen(")
if idx_otp != -1:
    before = content[:idx_otp]
    after = content[idx_otp:]
    after = after.replace("enabled = !isSendingOtp,\n", "", 1)
    content = before + after

# Fix ProfileSetupScreen button
idx_profile = content.find("fun ProfileSetupScreen(")
if idx_profile != -1:
    before = content[:idx_profile]
    after = content[idx_profile:]
    after = after.replace("enabled = !isSendingOtp,\n", "", 1)
    content = before + after

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
print("Fixed OtpScreen and ProfileSetupScreen buttons")
