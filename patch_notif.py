with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target_notif = """fun NotificationsScreen(onBack: () -> Unit) {
    Column(modifier = Modifier.fillMaxSize().padding(horizontal = 22.dp, vertical = 16.dp)) {
        IconButton(onClick = onBack, modifier = Modifier.padding(bottom = 18.dp)) {
            Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = Bench)
        }
        Text("Notifications", color = Chalk, fontSize = 26.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp, modifier = Modifier.padding(bottom = 20.dp))
        Text("Nothing yet. Requests and updates show up here.", color = Bench, fontSize = 14.sp)
    }
}"""
replacement_notif = """fun NotificationsScreen(viewModel: MaidanViewModel, onBack: () -> Unit) {
    val myNotifications by viewModel.myNotifications.collectAsStateWithLifecycle()
    val pending = myNotifications.filter { it.status == "pending" }
    
    Column(modifier = Modifier.fillMaxSize().padding(horizontal = 22.dp, vertical = 16.dp)) {
        IconButton(onClick = onBack, modifier = Modifier.padding(bottom = 18.dp)) {
            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Bench)
        }
        Text("Notifications", color = Chalk, fontSize = 26.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp, modifier = Modifier.padding(bottom = 20.dp))
        
        if (pending.isEmpty()) {
            Text("Nothing yet. Requests and updates show up here.", color = Bench, fontSize = 14.sp)
        } else {
            LazyColumn(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                items(pending) { req ->
                    Column(modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(Turf).padding(16.dp)) {
                        Text("${req.requesterName} wants to join", color = Chalk, fontSize = 16.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 4.dp))
                        Text(req.matchTitle, color = Floodlight, fontSize = 14.sp, modifier = Modifier.padding(bottom = 12.dp))
                        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            Button(
                                onClick = { viewModel.acceptRequest(req) },
                                colors = ButtonDefaults.buttonColors(containerColor = Whistle, contentColor = Color.White),
                                shape = RoundedCornerShape(8.dp),
                                modifier = Modifier.weight(1f)
                            ) {
                                Text("Accept")
                            }
                            Button(
                                onClick = { viewModel.rejectRequest(req) },
                                colors = ButtonDefaults.buttonColors(containerColor = Turf2, contentColor = Bench),
                                shape = RoundedCornerShape(8.dp),
                                modifier = Modifier.weight(1f)
                            ) {
                                Text("Reject")
                            }
                        }
                    }
                }
            }
        }
    }
}"""
content = content.replace(target_notif, replacement_notif)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
