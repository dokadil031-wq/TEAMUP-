import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# We need to change OtpScreen's isSendingOtp back.
target = """fun OtpScreen(
    contact: String,
    otp: String,
    onOtpChange: (String) -> Unit,
    onBack: () -> Unit,
    onNext: () -> Unit
)"""
# wait, the button in OtpScreen is what we need to fix
# Let's just fix the button inside OtpScreen

# Find OtpScreen definition
idx = content.find("fun OtpScreen(")
if idx != -1:
    otp_screen_content = content[idx:]
    # Replace the FIRST occurrence of `enabled = !isSendingOtp,` and `if (isSendingOtp)... else ...` in OtpScreen
    
    new_otp_screen = otp_screen_content.replace("enabled = !isSendingOtp,", "", 1)
    new_otp_screen = new_otp_screen.replace("if (isSendingOtp) androidx.compose.material3.CircularProgressIndicator(color = Pitch, modifier = Modifier.size(24.dp))\n            else Text(\"Continue\", fontSize = 16.sp, fontWeight = FontWeight.Bold)", "Text(\"Verify\", fontSize = 16.sp, fontWeight = FontWeight.Bold)", 1)
    
    # Wait, the original text in OtpScreen was "Verify". Did my replacement match "Text("Continue""? 
    # Let's check what `patch_auth.py` actually replaced.
