package com.example

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.material.icons.automirrored.filled.ArrowBack

import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import android.util.Base64
import java.io.ByteArrayOutputStream
import java.io.InputStream
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.foundation.Image
import androidx.compose.ui.layout.ContentScale

@Composable
fun PostDetailScreen(match: MatchEntity, viewModel: MaidanViewModel, onBack: () -> Unit, onMessageClick: () -> Unit, userName: String, onPosterClick: (String) -> Unit) {
    val myRequests by viewModel.myRequests.collectAsStateWithLifecycle()
    val uid = viewModel.auth.currentUser?.uid
    val req = myRequests.find { it.matchId == match.id }
    val requestStatus = if (match.posterId == uid) "mine" else req?.status ?: "none"

    Column(modifier = Modifier.fillMaxSize().padding(horizontal = 22.dp, vertical = 16.dp)) {
        IconButton(onClick = onBack, modifier = Modifier.padding(bottom = 18.dp)) {
            Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = Bench)
        }
        
        Row(modifier = Modifier.padding(bottom = 18.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.size(44.dp).clip(CircleShape).background(Turf2), contentAlignment = Alignment.Center) {
                Text(match.posterName.first().toString(), color = Floodlight, fontSize = 18.sp, fontWeight = FontWeight.Bold)
            }
            Spacer(modifier = Modifier.width(10.dp))
            Column {
                Text(match.posterName, color = Chalk, fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.Star, contentDescription = null, tint = Floodlight, modifier = Modifier.size(12.dp))
                    Text("${match.posterTrust}", color = Floodlight, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
                    Text(" · ${match.joined} matches · 8 months", color = Bench, fontSize = 12.sp)
                }
            }
        }
        
        Row(modifier = Modifier.padding(bottom = 12.dp)) {
            Text(match.sport.uppercase(), color = Floodlight, fontSize = 11.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.background(Turf2, RoundedCornerShape(20.dp)).padding(horizontal = 10.dp, vertical = 4.dp))
            if (match.audience != "All") {
                Spacer(modifier = Modifier.width(8.dp))
                Text("${match.audience} only", color = Bench, fontSize = 11.sp, fontWeight = FontWeight.SemiBold, fontFamily = FontFamily.Monospace, modifier = Modifier.border(1.dp, Line, RoundedCornerShape(20.dp)).padding(horizontal = 10.dp, vertical = 4.dp))
            }
        }
        
        Text(match.title, color = Chalk, fontSize = 24.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp, modifier = Modifier.padding(bottom = 12.dp), lineHeight = 28.sp)
        Text("Players: ${match.joined} / ${match.total}", color = Floodlight, fontSize = 14.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 12.dp))
        
        Column(modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(Turf2).padding(14.dp).padding(bottom = 4.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(bottom = 12.dp)) {
                Icon(Icons.Default.LocationOn, contentDescription = null, tint = Floodlight, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text(match.location, color = Chalk, fontSize = 14.sp)
            }
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(bottom = 12.dp)) {
                Icon(Icons.Default.DateRange, contentDescription = null, tint = Floodlight, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text(match.time, color = Chalk, fontSize = 14.sp)
            }
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(bottom = 8.dp)) {
                Icon(Icons.Default.Person, contentDescription = null, tint = Floodlight, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("${match.joined}/${match.total} joined", color = Chalk, fontSize = 14.sp, fontFamily = FontFamily.Monospace)
            }
        }
        
        Spacer(modifier = Modifier.height(18.dp))
        

        
        if (requestStatus == "mine") {
            Button(
                onClick = onMessageClick,
                colors = ButtonDefaults.buttonColors(containerColor = Turf2, contentColor = Floodlight),
                shape = RoundedCornerShape(12.dp),
                contentPadding = PaddingValues(vertical = 15.dp),
                border = androidx.compose.foundation.BorderStroke(1.dp, Line),
                modifier = Modifier.fillMaxWidth()
            ) {
                Icon(Icons.Default.Chat, contentDescription = null, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("View messages", fontSize = 15.sp, fontWeight = FontWeight.Bold)
            }
        } else if (requestStatus == "none") {
            Button(
                onClick = {
                    viewModel.requestToJoinMatch(match, userName)
                },
                colors = ButtonDefaults.buttonColors(containerColor = Floodlight, contentColor = Pitch),
                shape = RoundedCornerShape(12.dp),
                contentPadding = PaddingValues(vertical = 15.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Request to join", fontSize = 15.sp, fontWeight = FontWeight.Bold)
            }
        } else if (requestStatus == "requested" || requestStatus == "pending") {
            Button(
                onClick = { },
                colors = ButtonDefaults.buttonColors(containerColor = Turf2, contentColor = Bench),
                shape = RoundedCornerShape(12.dp),
                contentPadding = PaddingValues(vertical = 15.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Icon(Icons.Default.Schedule, contentDescription = null, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("Requested", fontSize = 15.sp, fontWeight = FontWeight.Bold)
            }
            Text("${match.posterName.split(" ").first()} will get a notification to accept.", color = Bench, fontSize = 12.sp, modifier = Modifier.padding(top = 10.dp).fillMaxWidth(), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
        } else if (requestStatus == "accepted") {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                Button(
                    onClick = { },
                    colors = ButtonDefaults.buttonColors(containerColor = Turf2, contentColor = Floodlight),
                    shape = RoundedCornerShape(12.dp),
                    contentPadding = PaddingValues(vertical = 15.dp),
                    border = androidx.compose.foundation.BorderStroke(1.dp, Line),
                    modifier = Modifier.weight(1f)
                ) {
                    Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("You're in", fontSize = 15.sp, fontWeight = FontWeight.Bold)
                }
                Button(
                    onClick = onMessageClick,
                    colors = ButtonDefaults.buttonColors(containerColor = Whistle, contentColor = Color.White),
                    shape = RoundedCornerShape(12.dp),
                    contentPadding = PaddingValues(vertical = 15.dp),
                    modifier = Modifier.weight(1f)
                ) {
                    Icon(Icons.Default.Chat, contentDescription = null, modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Message", fontSize = 15.sp, fontWeight = FontWeight.Bold)
                }
            }
            Spacer(modifier = Modifier.height(10.dp))
            Button(
                onClick = onMessageClick,
                colors = ButtonDefaults.buttonColors(containerColor = Color.Transparent, contentColor = Chalk),
                shape = RoundedCornerShape(12.dp),
                contentPadding = PaddingValues(vertical = 15.dp),
                border = androidx.compose.foundation.BorderStroke(1.dp, Line),
                modifier = Modifier.fillMaxWidth()
            ) {
                Icon(Icons.Default.Email, contentDescription = null, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("Message ${match.posterName.split(" ").first()}", fontSize = 15.sp, fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun LiveScreen() {
    var isStreaming by remember { mutableStateOf(false) }
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
    } else {
        Column(modifier = Modifier.fillMaxSize().padding(horizontal = 22.dp, vertical = 16.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth().padding(bottom = 20.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Live now", color = Chalk, fontSize = 26.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp)
                Button(
                    onClick = { isStreaming = true },
                    colors = ButtonDefaults.buttonColors(containerColor = Whistle, contentColor = Color.White),
                    shape = RoundedCornerShape(20.dp),
                    contentPadding = PaddingValues(horizontal = 14.dp, vertical = 8.dp),
                    modifier = Modifier.height(32.dp)
                ) {
                    Icon(Icons.Default.PlayArrow, contentDescription = null, modifier = Modifier.size(13.dp))
                    Spacer(modifier = Modifier.width(5.dp))
                    Text("Go live", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }
            }
            
            Text("No one's live right now.", color = Bench, fontSize = 14.sp, modifier = Modifier.fillMaxWidth().padding(vertical = 20.dp), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
            
            Spacer(modifier = Modifier.weight(1f))
            Text("More live streams show up here as players you've matched with go live.", color = Bench, fontSize = 13.sp, modifier = Modifier.fillMaxWidth().padding(10.dp), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
        }
    }
}

@Composable
fun MessagesScreen(viewModel: MaidanViewModel, onChatClick: (MatchRequest) -> Unit) {
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


@Composable
fun NotificationsScreen(viewModel: MaidanViewModel, onBack: () -> Unit) {
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
}

@Composable
fun CreatePostScreen(viewModel: MaidanViewModel, onPostCreated: () -> Unit) {
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
    val context = androidx.compose.ui.platform.LocalContext.current
    
    val categories = listOf("Sports", "Online gaming", "Exercise", "Group", "Other")
    val subcats = mapOf(
        "Sports" to listOf("Cricket", "Football", "Badminton", "Basketball", "Volleyball", "Table tennis"),
        "Online gaming" to listOf("BGMI", "Valorant", "FIFA", "Free Fire"),
        "Exercise" to listOf("Running", "Gym", "Yoga", "Cycling"),
        "Group" to listOf("Community", "Study", "Entrepreneur", "IT Development", "Coding")
    )

    val valid = category.isNotEmpty() && (sport.isNotEmpty() || category == "Other") && title.isNotEmpty() && location.isNotEmpty() && dateStr.isNotEmpty() && timeStr.isNotEmpty()

    Column(modifier = Modifier.fillMaxSize().padding(horizontal = 22.dp, vertical = 16.dp)) {
        Text("New post", color = Chalk, fontSize = 26.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp, modifier = Modifier.padding(bottom = 20.dp))
        
        Text("CATEGORY", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 8.dp))
        @OptIn(ExperimentalLayoutApi::class)
        FlowRow(modifier = Modifier.fillMaxWidth().padding(bottom = 18.dp), horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            categories.forEach { c ->
                val isSelected = category == c
                Box(
                    modifier = Modifier.clip(RoundedCornerShape(10.dp))
                        .background(if (isSelected) Floodlight else Turf2)
                        .border(if (isSelected) 0.dp else 1.dp, if (isSelected) Color.Transparent else Line, RoundedCornerShape(10.dp))
                        .clickable { category = c; sport = if (c == "Other") "Other" else "" }
                        .padding(horizontal = 16.dp, vertical = 10.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(c, color = if (isSelected) Pitch else Bench, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                }
            }
        }
        
        if (category.isNotEmpty() && category != "Other") {
            Text(if (category == "Sports") "SPORT" else if (category == "Online gaming") "GAME" else "ACTIVITY", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 8.dp))
            @OptIn(ExperimentalLayoutApi::class)
            FlowRow(modifier = Modifier.padding(bottom = 18.dp), horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                subcats[category]?.forEach { s ->
                    val isSelected = sport == s
                    Box(
                        modifier = Modifier.clip(RoundedCornerShape(20.dp))
                            .background(if (isSelected) Floodlight else Turf2)
                            .border(if (isSelected) 0.dp else 1.dp, if (isSelected) Color.Transparent else Line, RoundedCornerShape(20.dp))
                            .clickable { sport = s }
                            .padding(horizontal = 14.dp, vertical = 8.dp)
                    ) {
                        Text(s, color = if (isSelected) Pitch else Bench, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
                    }
                }
            }
        }
        
        Text("TITLE", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 6.dp))
        TextField(
            value = title, onValueChange = { title = it }, placeholder = { Text("e.g. Need 2 more for badminton", color = Bench) },
            colors = TextFieldDefaults.colors(focusedContainerColor = Turf2, unfocusedContainerColor = Turf2, focusedIndicatorColor = Color.Transparent, unfocusedIndicatorColor = Color.Transparent, focusedTextColor = Chalk, unfocusedTextColor = Chalk, cursorColor = Floodlight),
            shape = RoundedCornerShape(10.dp), modifier = Modifier.fillMaxWidth().border(1.dp, Line, RoundedCornerShape(10.dp)).padding(bottom = 14.dp)
        )
        
        Text("DESCRIPTION", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 6.dp))
        TextField(
            value = description, onValueChange = { description = it }, placeholder = { Text("Any details players should know", color = Bench) },
            colors = TextFieldDefaults.colors(focusedContainerColor = Turf2, unfocusedContainerColor = Turf2, focusedIndicatorColor = Color.Transparent, unfocusedIndicatorColor = Color.Transparent, focusedTextColor = Chalk, unfocusedTextColor = Chalk, cursorColor = Floodlight),
            shape = RoundedCornerShape(10.dp), modifier = Modifier.fillMaxWidth().height(90.dp).border(1.dp, Line, RoundedCornerShape(10.dp)).padding(bottom = 14.dp)
        )
        
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth().padding(bottom = 14.dp)) {
            Column(modifier = Modifier.weight(1f)) {
                Text("LOCATION", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 6.dp))
                TextField(
                    value = location, onValueChange = { location = it }, placeholder = { Text("Ground / area", color = Bench) },
                    colors = TextFieldDefaults.colors(focusedContainerColor = Turf2, unfocusedContainerColor = Turf2, focusedIndicatorColor = Color.Transparent, unfocusedIndicatorColor = Color.Transparent, focusedTextColor = Chalk, unfocusedTextColor = Chalk, cursorColor = Floodlight),
                    shape = RoundedCornerShape(10.dp), modifier = Modifier.fillMaxWidth().border(1.dp, Line, RoundedCornerShape(10.dp))
                )
            }
            Column(modifier = Modifier.weight(1f)) {
                Text("TIME", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 6.dp))
                Box(modifier = Modifier.fillMaxWidth().height(56.dp).border(1.dp, Line, RoundedCornerShape(10.dp)).background(Turf2, RoundedCornerShape(10.dp)).clickable {
                    val cal = java.util.Calendar.getInstance(); android.app.DatePickerDialog(
                        context,
                        { _, y, m, d ->
                            dateStr = "$d/${m+1}/$y"; android.app.TimePickerDialog(
                                context,
                                { _, h, min ->
                                    val ampm = if (h >= 12) "PM" else "AM"
                                    val hr = if (h % 12 == 0) 12 else h % 12
                                    timeStr = String.format("%02d:%02d %s", hr, min, ampm)
                                },
                                cal.get(java.util.Calendar.HOUR_OF_DAY),
                                cal.get(java.util.Calendar.MINUTE),
                                false
                            ).show()
                        },
                        cal.get(java.util.Calendar.YEAR),
                        cal.get(java.util.Calendar.MONTH),
                        cal.get(java.util.Calendar.DAY_OF_MONTH)
                    ).show()
                }, contentAlignment = Alignment.CenterStart) {
                    Text(
                        text = if (dateStr.isEmpty()) "Select Time" else "$dateStr, $timeStr",
                        color = if (dateStr.isEmpty()) Bench else Chalk,
                        fontSize = 14.sp,
                        modifier = Modifier.padding(start = 16.dp)
                    )
                }
            }
        }
        
        Text("WHO CAN SEE THIS POST", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 8.dp))
        Text("TOTAL PLAYERS NEEDED", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 6.dp))
        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(bottom = 14.dp)) {
            Slider(
                value = totalPlayers.toFloat(),
                onValueChange = { totalPlayers = it.toInt() },
                valueRange = 2f..22f,
                steps = 20,
                modifier = Modifier.weight(1f)
            )
            Spacer(modifier = Modifier.width(16.dp))
            Text(totalPlayers.toString(), color = Chalk, fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }
        
        Text("WHO CAN SEE THIS POST", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 8.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth().padding(bottom = 26.dp)) {
            listOf("All", "Male", "Female").forEach { a ->
                val isSelected = audience == a
                Box(
                    modifier = Modifier.weight(1f).clip(RoundedCornerShape(10.dp))
                        .background(if (isSelected) Floodlight else Turf2)
                        .border(if (isSelected) 0.dp else 1.dp, if (isSelected) Color.Transparent else Line, RoundedCornerShape(10.dp))
                        .clickable { audience = a }
                        .padding(vertical = 10.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(if (a == "All") "Everyone" else "$a only", color = if (isSelected) Pitch else Bench, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                }
            }
        }
        
        Button(
            onClick = {
                val newMatch = MatchEntity(
                    category = category,
                    sport = sport,
                    title = title,
                    location = location,
                    time = "$dateStr, $timeStr",
                    joined = 1,
                    total = totalPlayers,
                    audience = audience,
                    posterName = if (userName.isNotEmpty()) userName else "You",
                    posterTrust = 0.0
                )
                viewModel.addMatch(newMatch)
                onPostCreated()
            },
            enabled = valid,
            colors = ButtonDefaults.buttonColors(containerColor = Floodlight, contentColor = Pitch, disabledContainerColor = Turf2, disabledContentColor = Bench),
            modifier = Modifier.fillMaxWidth().height(50.dp),
            shape = RoundedCornerShape(12.dp)
        ) {
            Text("Post", fontWeight = FontWeight.Bold, fontSize = 15.sp)
        }
    }
}

@Composable
fun ProfileScreen(viewModel: MaidanViewModel, onEditProfileClick: () -> Unit = {}, onLogoutClick: () -> Unit = {}) {
    val userName by viewModel.userName.collectAsStateWithLifecycle()
    val userAge by viewModel.userAge.collectAsStateWithLifecycle()
    val userGender by viewModel.userGender.collectAsStateWithLifecycle()
    val userSports by viewModel.userSports.collectAsStateWithLifecycle()
    val userImage by viewModel.userImage.collectAsStateWithLifecycle()
    
    val context = LocalContext.current
    val launcher = rememberLauncherForActivityResult(contract = ActivityResultContracts.PickVisualMedia()) { uri: Uri? ->
        uri?.let {
            try {
                val inputStream: InputStream? = context.contentResolver.openInputStream(it)
                val originalBitmap = BitmapFactory.decodeStream(inputStream)
                // Resize and compress
                val maxSize = 400
                val ratio = Math.min(maxSize.toFloat() / originalBitmap.width, maxSize.toFloat() / originalBitmap.height)
                val width = Math.round(ratio * originalBitmap.width)
                val height = Math.round(ratio * originalBitmap.height)
                val resizedBitmap = Bitmap.createScaledBitmap(originalBitmap, width, height, false)
                val outputStream = ByteArrayOutputStream()
                resizedBitmap.compress(Bitmap.CompressFormat.JPEG, 70, outputStream)
                val byteArray = outputStream.toByteArray()
                val base64 = Base64.encodeToString(byteArray, Base64.DEFAULT)
                viewModel.updateProfilePhoto(base64)
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    Column(modifier = Modifier.fillMaxSize().padding(horizontal = 22.dp, vertical = 16.dp)) {
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End, verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.clip(RoundedCornerShape(20.dp)).border(1.dp, Line, RoundedCornerShape(20.dp)).clickable { onEditProfileClick() }.padding(horizontal = 12.dp, vertical = 6.dp)) {
                Text("Edit profile", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
            }
            Spacer(modifier = Modifier.width(8.dp))
            Box(modifier = Modifier.clip(RoundedCornerShape(20.dp)).border(1.dp, Color(0xFFEF4444), RoundedCornerShape(20.dp)).clickable { onLogoutClick() }.padding(horizontal = 12.dp, vertical = 6.dp)) {
                Text("Logout", color = Color(0xFFEF4444), fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
            }
        }
        
        Column(modifier = Modifier.fillMaxWidth().padding(bottom = 22.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Box(
                modifier = Modifier
                    .size(80.dp)
                    .clip(CircleShape)
                    .background(Turf2)
                    .clickable { launcher.launch(androidx.activity.result.PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)) },
                contentAlignment = Alignment.Center
            ) {
                if (userImage.isNotEmpty()) {
                    val bitmap = remember(userImage) {
                        try {
                            val imageBytes = Base64.decode(userImage, Base64.DEFAULT)
                            BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
                        } catch (e: Exception) {
                            null
                        }
                    }
                    if (bitmap != null) {
                        Image(bitmap = bitmap.asImageBitmap(), contentDescription = "Profile Photo", modifier = Modifier.fillMaxSize(), contentScale = ContentScale.Crop)
                    } else {
                        Text(if (userName.isNotEmpty()) userName.first().toString() else "Y", color = Floodlight, fontSize = 30.sp, fontWeight = FontWeight.ExtraBold)
                    }
                } else {
                    Text(if (userName.isNotEmpty()) userName.first().toString() else "Y", color = Floodlight, fontSize = 30.sp, fontWeight = FontWeight.ExtraBold)
                }
            }
            Text("Tap to change photo", color = Bench, fontSize = 10.sp, modifier = Modifier.padding(top = 4.dp))
            Text(if (userName.isNotEmpty()) userName else "Your name", color = Chalk, fontSize = 22.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp, modifier = Modifier.padding(top = 12.dp, bottom = 2.dp))
            Text(if (userAge.isNotEmpty()) "$userAge yrs · $userGender" else "New player", color = Bench, fontSize = 13.sp)
        }
        
        Column(modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(14.dp)).background(Turf2).padding(16.dp).padding(bottom = 20.dp)) {
            Row(modifier = Modifier.fillMaxWidth().padding(bottom = 10.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("TRUST SCORE", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, letterSpacing = 0.5.sp)
                Text("New player", color = Bench, fontSize = 12.sp)
            }
            
            @OptIn(ExperimentalLayoutApi::class)
            FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                listOf("✓ Phone verified", "0 matches played", "Member since today").forEach { item ->
                    Box(modifier = Modifier.clip(RoundedCornerShape(20.dp)).background(Turf).padding(horizontal = 10.dp, vertical = 5.dp)) {
                        Text(item, color = Bench, fontSize = 11.sp)
                    }
                }
            }
            
            Text("Play your first match to start building your score.", color = Bench, fontSize = 12.sp, modifier = Modifier.padding(top = 10.dp))
        }
        
        Text("YOUR GAMES", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 8.dp))
        
        @OptIn(ExperimentalLayoutApi::class)
        if (userSports.isNotEmpty()) {
            FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                userSports.forEach { s ->
                    Box(modifier = Modifier.clip(RoundedCornerShape(20.dp)).border(1.dp, Line, RoundedCornerShape(20.dp)).padding(horizontal = 14.dp, vertical = 8.dp)) {
                        Text(s, color = Chalk, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
                    }
                }
            }
        } else {
            Text("No games picked yet.", color = Bench, fontSize = 13.sp)
        }
    }
}


@Composable
fun EditProfileScreen(
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
    ) {
        IconButton(onClick = onBack, modifier = Modifier.padding(bottom = 18.dp)) {
            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Bench)
        }
        Text("Edit profile", color = Chalk, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp, modifier = Modifier.padding(bottom = 24.dp))
        
        OutlinedTextField(
            value = name,
            onValueChange = onNameChange,
            label = { Text("Full Name") },
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = Floodlight,
                focusedLabelColor = Floodlight,
                unfocusedBorderColor = Line,
                unfocusedLabelColor = Bench,
                focusedTextColor = Chalk,
                unfocusedTextColor = Chalk
            ),
            modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp)
        )
        
        Row(modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            OutlinedTextField(
                value = age,
                onValueChange = onAgeChange,
                label = { Text("Age") },
                singleLine = true, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = Floodlight,
                    focusedLabelColor = Floodlight,
                    unfocusedBorderColor = Line,
                    unfocusedLabelColor = Bench,
                    focusedTextColor = Chalk,
                    unfocusedTextColor = Chalk
                ),
                modifier = Modifier.weight(1f)
            )
            OutlinedTextField(
                value = gender,
                onValueChange = onGenderChange,
                label = { Text("Gender") },
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = Floodlight,
                    focusedLabelColor = Floodlight,
                    unfocusedBorderColor = Line,
                    unfocusedLabelColor = Bench,
                    focusedTextColor = Chalk,
                    unfocusedTextColor = Chalk
                ),
                modifier = Modifier.weight(1f)
            )
        }

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
        Text("Change Password", color = Chalk, fontSize = 16.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 12.dp))

        OutlinedTextField(
            value = newPassword,
            onValueChange = { newPassword = it },
            label = { Text("New Password (optional)") },
            visualTransformation = PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = Floodlight,
                focusedLabelColor = Floodlight,
                unfocusedBorderColor = Line,
                unfocusedLabelColor = Bench,
                focusedTextColor = Chalk,
                unfocusedTextColor = Chalk
            ),
            modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)
        )

        if (statusMessage.isNotEmpty()) {
            Text(statusMessage, color = Floodlight, fontSize = 14.sp, modifier = Modifier.padding(bottom = 8.dp))
        }
        
        Button(
            onClick = {
                if (newPassword.isNotBlank()) {
                    viewModel.updatePassword(newPassword) { result ->
                        statusMessage = result
                        if (result.contains("successfully")) {
                            onSave()
                        }
                    }
                } else {
                    onSave()
                }
            },
            colors = ButtonDefaults.buttonColors(containerColor = Whistle, contentColor = Color.White),
            modifier = Modifier.fillMaxWidth().height(50.dp)
        ) {
            Text("Save Changes", fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }
    }
}
