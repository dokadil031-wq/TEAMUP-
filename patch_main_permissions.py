import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    text = f.read()

target = '    var currentScreen by remember { mutableStateOf(if (viewModel.auth.currentUser != null) "main" else "auth") }'

repl = '''    var currentScreen by remember { mutableStateOf(if (viewModel.auth.currentUser != null) "main" else "auth") }
    val userCity by viewModel.userCity.collectAsStateWithLifecycle()
    
    val locationPermissions = com.google.accompanist.permissions.rememberMultiplePermissionsState(
        permissions = listOf(
            android.Manifest.permission.ACCESS_COARSE_LOCATION,
            android.Manifest.permission.ACCESS_FINE_LOCATION
        )
    )

    androidx.compose.runtime.LaunchedEffect(locationPermissions.allPermissionsGranted, currentScreen) {
        if (currentScreen == "main") {
            if (!locationPermissions.allPermissionsGranted) {
                locationPermissions.launchMultiplePermissionRequest()
            } else if (userCity.isEmpty()) {
                kotlinx.coroutines.Dispatchers.IO.invoke {
                    val city = LocationHelper.getCurrentCity(context)
                    if (city != null) {
                        viewModel.updateUserCity(city)
                    }
                }
            }
        }
    }'''

text = text.replace(target, repl)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(text)
