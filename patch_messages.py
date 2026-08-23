with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target = """fun MessagesScreen() {
    Column(modifier = Modifier.fillMaxSize().padding(horizontal = 22.dp, vertical = 16.dp)) {
        Text("Messages", color = Chalk, fontSize = 26.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp, modifier = Modifier.padding(bottom = 20.dp))
        Text("No conversations yet. Get a request accepted to start chatting.", color = Bench, fontSize = 14.sp)
    }
}"""

replacement = """fun MessagesScreen(viewModel: MaidanViewModel, onChatClick: (MatchRequest) -> Unit) {
    val myRequests by viewModel.myRequests.collectAsStateWithLifecycle()
    val myNotifications by viewModel.myNotifications.collectAsStateWithLifecycle()
    val accepted = (myRequests.filter { it.status == "accepted" } + myNotifications.filter { it.status == "accepted" }).distinctBy { it.id }

    Column(modifier = Modifier.fillMaxSize().padding(horizontal = 22.dp, vertical = 16.dp)) {
        Text("Messages", color = Chalk, fontSize = 26.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp, modifier = Modifier.padding(bottom = 20.dp))
        
        if (accepted.isEmpty()) {
            Text("No conversations yet. Get a request accepted to start chatting.", color = Bench, fontSize = 14.sp)
        } else {
            LazyColumn(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                items(accepted) { req ->
                    val otherPerson = if (req.requesterId == viewModel.auth.currentUser?.uid) "Match Poster" else req.requesterName
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .background(Turf)
                            .clickable { onChatClick(req) }
                            .padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(modifier = Modifier.size(40.dp).clip(CircleShape).background(Turf2), contentAlignment = Alignment.Center) {
                            Text(otherPerson.first().toString(), color = Floodlight, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Column {
                            Text(otherPerson, color = Chalk, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                            Text(req.matchTitle, color = Bench, fontSize = 12.sp, maxLines = 1)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun ChatScreen(request: MatchRequest, viewModel: MaidanViewModel, onBack: () -> Unit) {
    var messages by remember { mutableStateOf<List<ChatMessage>>(emptyList()) }
    var inputText by remember { mutableStateOf("") }
    
    LaunchedEffect(request.id) {
        viewModel.getMessages(request.id) { msgs ->
            messages = msgs
        }
    }
    
    Column(modifier = Modifier.fillMaxSize()) {
        // Header
        Row(
            modifier = Modifier.fillMaxWidth().background(Turf).padding(horizontal = 16.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = onBack) {
                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Chalk)
            }
            Text("Chat", color = Chalk, fontSize = 18.sp, fontWeight = FontWeight.Bold)
        }
        
        // Messages list
        LazyColumn(
            modifier = Modifier.weight(1f).padding(horizontal = 16.dp),
            contentPadding = PaddingValues(vertical = 16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(messages) { msg ->
                val isMe = msg.senderId == viewModel.auth.currentUser?.uid
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = if (isMe) Arrangement.End else Arrangement.Start) {
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp, bottomStart = if (isMe) 16.dp else 0.dp, bottomEnd = if (isMe) 0.dp else 16.dp))
                            .background(if (isMe) Floodlight else Turf2)
                            .padding(12.dp)
                    ) {
                        Text(msg.text, color = if (isMe) Pitch else Chalk, fontSize = 14.sp)
                    }
                }
            }
        }
        
        // Input area
        Row(
            modifier = Modifier.fillMaxWidth().background(Turf).padding(8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            OutlinedTextField(
                value = inputText,
                onValueChange = { inputText = it },
                modifier = Modifier.weight(1f),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = Color.Transparent,
                    unfocusedBorderColor = Color.Transparent,
                    focusedTextColor = Chalk,
                    unfocusedTextColor = Chalk
                ),
                placeholder = { Text("Message...", color = Bench) },
                shape = RoundedCornerShape(24.dp)
            )
            IconButton(
                onClick = {
                    if (inputText.isNotBlank()) {
                        viewModel.sendMessage(request.id, inputText)
                        inputText = ""
                    }
                }
            ) {
                Icon(Icons.Default.Send, contentDescription = "Send", tint = Floodlight)
            }
        }
    }
}
"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
