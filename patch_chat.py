import re

with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target = """        Row(
            modifier = Modifier.fillMaxWidth().background(Turf).padding(horizontal = 16.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = onBack) {
                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Chalk)
            }
            Text("Chat", color = Chalk, fontSize = 18.sp, fontWeight = FontWeight.Bold)
        }"""

repl = """        val isMeRequester = viewModel.auth.currentUser?.uid == request.requesterId
        val targetUserId = if (isMeRequester) request.posterId else request.requesterId
        val targetUserName = if (isMeRequester) request.posterId else request.requesterName
        
        Row(
            modifier = Modifier.fillMaxWidth().background(Turf).padding(horizontal = 16.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = onBack) {
                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Chalk)
            }
            Text("Chat", color = Chalk, fontSize = 18.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.weight(1f))
            androidx.compose.ui.viewinterop.AndroidView(
                factory = { context ->
                    com.zegocloud.uikit.prebuilt.call.invite.widget.ZegoSendCallInvitationButton(context).apply {
                        setIsVideoCall(false)
                        setResourceID("zego_uikit_call")
                        setInvitees(listOf(com.zegocloud.uikit.service.defines.ZegoUIKitUser(targetUserId, targetUserName)))
                    }
                },
                modifier = Modifier.size(40.dp)
            )
            Spacer(modifier = Modifier.width(8.dp))
            androidx.compose.ui.viewinterop.AndroidView(
                factory = { context ->
                    com.zegocloud.uikit.prebuilt.call.invite.widget.ZegoSendCallInvitationButton(context).apply {
                        setIsVideoCall(true)
                        setResourceID("zego_uikit_call")
                        setInvitees(listOf(com.zegocloud.uikit.service.defines.ZegoUIKitUser(targetUserId, targetUserName)))
                    }
                },
                modifier = Modifier.size(40.dp)
            )
        }"""

content = content.replace(target, repl)

target_live = """    var isStreaming by remember { mutableStateOf(false) }
    if (isStreaming) {
        Box(modifier = Modifier.fillMaxSize().background(Color.Black)) {
            // Fake Camera Preview
            Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally) {
                Icon(Icons.Default.Videocam, contentDescription = null, tint = Bench.copy(alpha = 0.5f), modifier = Modifier.size(64.dp))
                Spacer(modifier = Modifier.height(8.dp))
                Text("Camera Preview Active", color = Bench.copy(alpha = 0.5f))
            }
            
            // Overlay
            Column(modifier = Modifier.fillMaxSize().padding(22.dp)) {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Row(
                        modifier = Modifier.clip(RoundedCornerShape(8.dp)).background(Whistle).padding(horizontal = 8.dp, vertical = 4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(modifier = Modifier.size(8.dp).clip(CircleShape).background(Color.White))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("LIVE", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    }
                    Box(modifier = Modifier.clip(RoundedCornerShape(8.dp)).background(Pitch.copy(alpha = 0.5f)).padding(horizontal = 8.dp, vertical = 4.dp)) {
                        Text("12 viewers", color = Chalk, fontSize = 12.sp)
                    }
                }
                Spacer(modifier = Modifier.weight(1f))
                
                // Chat and End Stream
                Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                    TextField(
                        value = "", onValueChange = {},
                        placeholder = { Text("Say something...", color = Bench) },
                        modifier = Modifier.weight(1f).height(50.dp).clip(RoundedCornerShape(25.dp)),
                        colors = TextFieldDefaults.colors(
                            focusedContainerColor = Turf2.copy(alpha=0.7f),
                            unfocusedContainerColor = Turf2.copy(alpha=0.7f),
                            focusedIndicatorColor = Color.Transparent,
                            unfocusedIndicatorColor = Color.Transparent
                        )
                    )
                    Spacer(modifier = Modifier.width(12.dp))
                    IconButton(
                        onClick = { isStreaming = false },
                        modifier = Modifier.size(50.dp).clip(CircleShape).background(Color(0xFFE53935))
                    ) {
                        Icon(Icons.Default.Close, contentDescription = "End Stream", tint = Color.White)
                    }
                }
            }
        }
    } else {"""

repl_live = """    val context = androidx.compose.ui.platform.LocalContext.current
    var isStreaming by remember { mutableStateOf(false) }
    if (isStreaming) {
        // We will never hit this in the real app because we launch an intent.
    } else {"""

content = content.replace(target_live, repl_live)

target_go_live = """                Button(
                    onClick = { isStreaming = true },
                    colors = ButtonDefaults.buttonColors(containerColor = Whistle, contentColor = Color.White),
                    shape = RoundedCornerShape(20.dp),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Icon(Icons.Default.Add, contentDescription = null, modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(4.dp))
                    Text("Go live", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }"""

repl_go_live = """                Button(
                    onClick = { 
                        val intent = android.content.Intent(context, LiveActivity::class.java).apply {
                            putExtra("isHost", true)
                        }
                        context.startActivity(intent)
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = Whistle, contentColor = Color.White),
                    shape = RoundedCornerShape(20.dp),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Icon(Icons.Default.Add, contentDescription = null, modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(4.dp))
                    Text("Go live", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }"""
content = content.replace(target_go_live, repl_go_live)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
