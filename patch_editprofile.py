with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target = '''fun EditProfileScreen(
    name: String, onNameChange: (String) -> Unit,
    age: String, onAgeChange: (String) -> Unit,
    gender: String, onGenderChange: (String) -> Unit,
    viewModel: MaidanViewModel,
    onBack: () -> Unit, onSave: () -> Unit
) {
    var newPassword by remember { mutableStateOf("") }
    var statusMessage by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(26.dp)
            .verticalScroll(rememberScrollState())
    ) {'''

replacement = '''fun EditProfileScreen(
    name: String, onNameChange: (String) -> Unit,
    age: String, onAgeChange: (String) -> Unit,
    gender: String, onGenderChange: (String) -> Unit,
    selectedSports: List<String>, onToggleSport: (String) -> Unit,
    viewModel: MaidanViewModel,
    onBack: () -> Unit, onSave: () -> Unit
) {
    val sportsList = listOf("Cricket", "Football", "Badminton", "Basketball", "Volleyball", "Table tennis", "Running", "Gym", "Online gaming", "Exercise")
    var newPassword by remember { mutableStateOf("") }
    var statusMessage by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Pitch)
            .padding(26.dp)
            .verticalScroll(rememberScrollState())
    ) {'''

content = content.replace(target, replacement)

target_sports = '''        }

        Spacer(modifier = Modifier.height(16.dp))
        Text("Change Password", color = Chalk, fontSize = 20.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 12.dp))'''

replacement_sports = '''        }

        Spacer(modifier = Modifier.height(16.dp))
        Text("Categories you like", color = Chalk, fontSize = 16.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 12.dp))
        @OptIn(ExperimentalLayoutApi::class)
        FlowRow(
            modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            sportsList.forEach { sport ->
                val isSelected = selectedSports.contains(sport)
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(20.dp))
                        .background(if (isSelected) Floodlight else Turf2)
                        .clickable { onToggleSport(sport) }
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Text(
                        text = sport,
                        color = if (isSelected) Pitch else Chalk,
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Medium
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(16.dp))
        Text("Change Password", color = Chalk, fontSize = 16.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 12.dp))'''

content = content.replace(target_sports, replacement_sports)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)

