import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    text = f.read()

target = """    val locationPermissions = com.google.accompanist.permissions.rememberMultiplePermissionsState(
        permissions = listOf(
            android.Manifest.permission.ACCESS_COARSE_LOCATION,
            android.Manifest.permission.ACCESS_FINE_LOCATION
        )
    )

    val contextForLocation = androidx.compose.ui.platform.LocalContext.current
    androidx.compose.runtime.LaunchedEffect(locationPermissions.allPermissionsGranted, currentScreen) {
        if (currentScreen == "main") {
            if (!locationPermissions.allPermissionsGranted) {
                locationPermissions.launchMultiplePermissionRequest()
            } else if (userCity.isEmpty()) {
                val city = LocationHelper.getCurrentCity(contextForLocation)
                if (city != null) {
                    viewModel.updateUserCity(city)
                }
            }
        }
    }"""

repl = """    val contextForLocation = androidx.compose.ui.platform.LocalContext.current
    val scope = androidx.compose.runtime.rememberCoroutineScope()
    val permissionLauncher = androidx.activity.compose.rememberLauncherForActivityResult(
        androidx.activity.result.contract.ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        val granted = permissions[android.Manifest.permission.ACCESS_FINE_LOCATION] == true || permissions[android.Manifest.permission.ACCESS_COARSE_LOCATION] == true
        if (granted && userCity.isEmpty()) {
            scope.kotlinx.coroutines.launch {
                val city = LocationHelper.getCurrentCity(contextForLocation)
                if (city != null) {
                    viewModel.updateUserCity(city)
                }
            }
        }
    }

    androidx.compose.runtime.LaunchedEffect(currentScreen) {
        if (currentScreen == "main") {
            val hasPermission = androidx.core.content.ContextCompat.checkSelfPermission(contextForLocation, android.Manifest.permission.ACCESS_COARSE_LOCATION) == android.content.pm.PackageManager.PERMISSION_GRANTED
            if (!hasPermission) {
                permissionLauncher.launch(arrayOf(
                    android.Manifest.permission.ACCESS_COARSE_LOCATION,
                    android.Manifest.permission.ACCESS_FINE_LOCATION
                ))
            } else if (userCity.isEmpty()) {
                val city = LocationHelper.getCurrentCity(contextForLocation)
                if (city != null) {
                    viewModel.updateUserCity(city)
                }
            }
        }
    }"""

# Fix the scope syntax for coroutines
repl = repl.replace("scope.kotlinx.coroutines.launch", "scope.launch")
# We need to import kotlinx.coroutines.launch if not present, but scope.launch is usually enough if imported.
# Actually, just use `kotlinx.coroutines.launch` explicitly? No, `scope.launch` is an extension function on CoroutineScope.
# Better to use fully qualified or import. `kotlinx.coroutines.launch` needs `import kotlinx.coroutines.launch`.
# In Kotlin, `scope.launch` works if we have `import kotlinx.coroutines.launch`. Let's assume it's imported.

text = text.replace(target, repl)

text = text.replace("@OptIn(com.google.accompanist.permissions.ExperimentalPermissionsApi::class)\n@Composable\nfun MaidanApp(", "@Composable\nfun MaidanApp(")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(text)

