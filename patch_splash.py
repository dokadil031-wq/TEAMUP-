import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target_app = """@Composable
fun MaidanApp(modifier: Modifier = Modifier, viewModel: MaidanViewModel = viewModel()) {
    var currentScreen by remember { mutableStateOf(if (viewModel.auth.currentUser != null) "main" else "auth") }"""

repl_app = """@Composable
fun SplashScreen() {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black),
        contentAlignment = Alignment.Center
    ) {
        androidx.compose.foundation.Image(
            painter = androidx.compose.ui.res.painterResource(id = R.drawable.teamup_logo),
            contentDescription = "App Logo",
            modifier = Modifier.size(300.dp),
            contentScale = ContentScale.Fit
        )
        Text(
            text = "from NOROX",
            color = Color.White,
            fontSize = 16.sp,
            fontWeight = FontWeight.SemiBold,
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(bottom = 50.dp)
        )
    }
}

@Composable
fun MaidanApp(modifier: Modifier = Modifier, viewModel: MaidanViewModel = viewModel()) {
    var showSplash by remember { mutableStateOf(true) }
    androidx.compose.runtime.LaunchedEffect(Unit) {
        kotlinx.coroutines.delay(2000)
        showSplash = false
    }
    
    if (showSplash) {
        SplashScreen()
        return
    }

    var currentScreen by remember { mutableStateOf(if (viewModel.auth.currentUser != null) "main" else "auth") }"""

content = content.replace(target_app, repl_app)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
