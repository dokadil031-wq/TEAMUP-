with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target = """fun CreatePostScreen(viewModel: MaidanViewModel, onPostCreated: () -> Unit) {
    val userName by viewModel.userName.collectAsStateWithLifecycle()
    var category by remember { mutableStateOf("") }
    var sport by remember { mutableStateOf("") }
    var title by remember { mutableStateOf("") }
    var description by remember { mutableStateOf("") }
    var location by remember { mutableStateOf("") }
    var time by remember { mutableStateOf("") }
    var audience by remember { mutableStateOf("All") }"""

replacement = """fun CreatePostScreen(viewModel: MaidanViewModel, onPostCreated: () -> Unit) {
    val userName by viewModel.userName.collectAsStateWithLifecycle()
    var category by remember { mutableStateOf("") }
    var sport by remember { mutableStateOf("") }
    var title by remember { mutableStateOf("") }
    var description by remember { mutableStateOf("") }
    var location by remember { mutableStateOf("") }
    var dateStr by remember { mutableStateOf("") }
    var timeStr by remember { mutableStateOf("") }
    var audience by remember { mutableStateOf("All") }
    var totalPlayers by remember { mutableStateOf(4) }
    var mapSelectedPosition by remember { mutableStateOf<com.google.android.gms.maps.model.LatLng?>(null) }
    val context = androidx.compose.ui.platform.LocalContext.current"""

content = content.replace(target, replacement)

target2 = """    val valid = title.isNotEmpty() && sport.isNotEmpty() && location.isNotEmpty() && time.isNotEmpty()"""
replacement2 = """    val valid = title.isNotEmpty() && sport.isNotEmpty() && location.isNotEmpty() && dateStr.isNotEmpty() && timeStr.isNotEmpty()"""

content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
