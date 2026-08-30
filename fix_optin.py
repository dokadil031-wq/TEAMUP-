with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    text = f.read()

text = text.replace('@Composable\nfun MaidanApp(', '@OptIn(com.google.accompanist.permissions.ExperimentalPermissionsApi::class)\n@Composable\nfun MaidanApp(')
text = text.replace('@OptIn(com.google.accompanist.permissions.ExperimentalPermissionsApi::class)\n    val locationPermissions', 'val locationPermissions')

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(text)
