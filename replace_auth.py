import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Replace the navigation part
nav_old = """            currentScreen == "phone" -> PhoneScreen(
                method = method,
                onMethodChange = { method = it },
                contact = contact,
                onContactChange = { contact = it },
                onNext = { currentScreen = "otp" }
            )
            currentScreen == "otp" -> OtpScreen(
                contact = contact,
                otp = otp,
                onOtpChange = { otp = it },
                onBack = { currentScreen = "phone" },
                onNext = { currentScreen = "profileSetup" }
            )"""

nav_new = """            currentScreen == "phone" -> AuthScreen(
                viewModel = viewModel,
                onAuthSuccess = { isNewUser ->
                    if (isNewUser) currentScreen = "profileSetup"
                    else currentScreen = "main"
                }
            )"""

content = content.replace(nav_old, nav_new)

# Now let's remove PhoneScreen and OtpScreen completely
# Since they are at the end or somewhere, we can just truncate the file from 'fun PhoneScreen(' and append the new AuthScreen.

idx = content.find("@Composable\nfun PhoneScreen(")
if idx != -1:
    content = content[:idx]

# Remove the MethodButton as well if it's there
# PhoneScreen and OtpScreen and MethodButton are followed by ProfileSetupScreen?
# Let's check where PhoneScreen is defined.
