package com.example


import android.app.Activity
import androidx.compose.ui.platform.LocalContext
import com.google.firebase.auth.PhoneAuthOptions
import com.google.firebase.auth.PhoneAuthProvider
import com.google.firebase.auth.PhoneAuthCredential
import com.google.firebase.FirebaseException
import java.util.concurrent.TimeUnit
import android.widget.Toast
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.foundation.Image

import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.ui.theme.MyApplicationTheme

val Pitch = Color(0xFF0E1512)
val Turf = Color(0xFF16211C)
val Turf2 = Color(0xFF1D2A22)
val Chalk = Color(0xFFF3F5EC)
val Bench = Color(0xFF93A398)
val Floodlight = Color(0xFFC8FF4D)
val Whistle = Color(0xFFFF5A36)
val Line = Color(0xFF283730)
val LiveGreen = Color(0xFF22C55E)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyApplicationTheme {
                Scaffold(
                    modifier = Modifier.fillMaxSize(),
                    containerColor = Pitch
                ) { innerPadding ->
                    MaidanApp(modifier = Modifier.padding(innerPadding))
                }
            }
        }
    }
}

@Composable
fun MaidanApp(modifier: Modifier = Modifier, viewModel: MaidanViewModel = viewModel()) {
    var currentScreen by remember { mutableStateOf(if (viewModel.auth.currentUser != null) "main" else "auth") }
    var method by remember { mutableStateOf("phone") }
    var contact by remember { mutableStateOf("") }
    var otp by remember { mutableStateOf("") }
    var setupPassword by remember { mutableStateOf("") }
    var verificationId by remember { mutableStateOf("") }
    var isSendingOtp by remember { mutableStateOf(false) }
    val context = LocalContext.current
    val activity = remember(context) { 
        var ctx = context
        while (ctx is android.content.ContextWrapper) {
            if (ctx is Activity) break
            ctx = ctx.baseContext
        }
        ctx as Activity
    }
    val userName by viewModel.userName.collectAsStateWithLifecycle()
    val userAge by viewModel.userAge.collectAsStateWithLifecycle()
    val userGender by viewModel.userGender.collectAsStateWithLifecycle()
    val userSports by viewModel.userSports.collectAsStateWithLifecycle()
    
    var name by remember(userName) { mutableStateOf(userName) }
    var age by remember(userAge) { mutableStateOf(userAge) }
    var gender by remember(userGender) { mutableStateOf(userGender) }
    val selectedSports = remember(userSports) { mutableStateListOf(*userSports.toTypedArray()) }
    var profilePhotoBase64 by remember { mutableStateOf("") }

    var currentTab by remember { mutableStateOf("Home") }
    var selectedMatch by remember { mutableStateOf<MatchEntity?>(null) }
    var selectedRequest by remember { mutableStateOf<MatchRequest?>(null) }
    var targetUserId by remember { mutableStateOf<String?>(null) }

    Box(
        modifier = modifier
            .fillMaxSize()
            .background(Pitch)
    ) {
        when {
            currentScreen == "auth" -> AuthScreen(
                viewModel = viewModel,
                onAuthSuccess = { isNewUser ->
                    if (isNewUser) currentScreen = "profileSetup"
                    else currentScreen = "main"
                },
                onSignUpClick = { currentScreen = "phone" }
            )
            currentScreen == "phone" -> PhoneScreen(
                method = method,
                onMethodChange = { method = it },
                contact = contact,
                onContactChange = { contact = it },
                onNext = { 
                    if (contact.isBlank()) {
                        Toast.makeText(activity, "Please enter a valid detail", Toast.LENGTH_SHORT).show()
                        return@PhoneScreen
                    }
                    if (method == "phone") {
                        isSendingOtp = true
                        val options = PhoneAuthOptions.newBuilder(viewModel.auth)
                            .setPhoneNumber(if (contact.startsWith("+")) contact else "+91$contact")
                            .setTimeout(60L, TimeUnit.SECONDS)
                            .setActivity(activity)
                            .setCallbacks(object : PhoneAuthProvider.OnVerificationStateChangedCallbacks() {
                                override fun onVerificationCompleted(credential: PhoneAuthCredential) {
                                    isSendingOtp = false
                                    // Optionally handle auto-retrieval
                                }
                                override fun onVerificationFailed(e: FirebaseException) {
                                    isSendingOtp = false
                                    Toast.makeText(activity, "Verification failed: ${e.message}", Toast.LENGTH_LONG).show()
                                }
                                override fun onCodeSent(verId: String, token: PhoneAuthProvider.ForceResendingToken) {
                                    isSendingOtp = false
                                    verificationId = verId
                                    currentScreen = "otp"
                                    Toast.makeText(activity, "OTP Sent", Toast.LENGTH_SHORT).show()
                                }
                            })
                            .build()
                        PhoneAuthProvider.verifyPhoneNumber(options)
                    } else {
                        // Email doesn't use OTP in this flow, directly go to setup to set password
                        currentScreen = "profileSetup"
                    }
                },
                onSignInClick = { currentScreen = "auth" },
                isSendingOtp = isSendingOtp
            )
            currentScreen == "otp" -> OtpScreen(
                contact = contact,
                otp = otp,
                onOtpChange = { otp = it },
                onBack = { currentScreen = "phone" },
                onNext = {
                    if (otp.length < 6) {
                        Toast.makeText(activity, "Invalid OTP", Toast.LENGTH_SHORT).show()
                        return@OtpScreen
                    }
                    val credential = PhoneAuthProvider.getCredential(verificationId, otp)
                    viewModel.auth.signInWithCredential(credential)
                        .addOnCompleteListener(activity) { task ->
                            if (task.isSuccessful) {
                                currentScreen = "profileSetup"
                            } else {
                                Toast.makeText(activity, "Invalid OTP", Toast.LENGTH_SHORT).show()
                            }
                        }
                }
            )
            currentScreen == "editProfile" -> EditProfileScreen(
                name = name,
                onNameChange = { name = it },
                age = age,
                onAgeChange = { age = it },
                gender = gender,
                onGenderChange = { gender = it },
                selectedSports = selectedSports,
                onToggleSport = {
                    if (selectedSports.contains(it)) selectedSports.remove(it)
                    else selectedSports.add(it)
                },
                viewModel = viewModel,
                onBack = { currentScreen = "main" },
                onSave = {
                    viewModel.saveUserProfile(name, age, gender, selectedSports.toList())
                    currentScreen = "main"
                }
            )
                        currentScreen == "profileSetup" -> ProfileSetupScreen(
                name = name,
                onNameChange = { name = it },
                age = age,
                onAgeChange = { age = it },
                gender = gender,
                onGenderChange = { gender = it },
                selectedSports = selectedSports,
                onToggleSport = {
                    if (selectedSports.contains(it)) selectedSports.remove(it)
                    else selectedSports.add(it)
                },
                password = setupPassword,
                onPasswordChange = { setupPassword = it },
                onBack = { currentScreen = "otp" },
                onNext = { 
                    val actualEmail = if (contact.contains("@")) contact else "$${contact}@maidan.app"
                    val actualPass = if (setupPassword.isNotBlank()) setupPassword else "maidan123"
                    viewModel.signUp(
                        email = actualEmail,
                        pass = actualPass,
                        onSuccess = {
                            viewModel.saveUserProfile(name, age, gender, selectedSports.toList())
                            if (profilePhotoBase64.isNotEmpty()) viewModel.updateProfilePhoto(profilePhotoBase64)
                            currentScreen = "main"
                        },
                        onError = {
                            // If user exists or failed, just login and proceed
                            viewModel.signIn(
                                email = actualEmail,
                                pass = actualPass,
                                onSuccess = {
                                    viewModel.saveUserProfile(name, age, gender, selectedSports.toList())
                                    if (profilePhotoBase64.isNotEmpty()) viewModel.updateProfilePhoto(profilePhotoBase64)
                                    currentScreen = "main"
                                },
                                onError = {
                                    viewModel.signInAnonymously(
                                        onSuccess = {
                                            viewModel.saveUserProfile(name, age, gender, selectedSports.toList())
                                            if (profilePhotoBase64.isNotEmpty()) viewModel.updateProfilePhoto(profilePhotoBase64)
                                            currentScreen = "main"
                                        },
                                        onError = {
                                            viewModel.saveUserProfile(name, age, gender, selectedSports.toList())
                                            if (profilePhotoBase64.isNotEmpty()) viewModel.updateProfilePhoto(profilePhotoBase64)
                                            currentScreen = "main"
                                        }
                                    )
                                }
                            )
                        }
                    )
                },
                photoBase64 = profilePhotoBase64,
                onPhotoCaptured = { profilePhotoBase64 = it }
            )
            currentScreen == "postDetail" && selectedMatch != null -> {
                PostDetailScreen(
                    match = selectedMatch!!,
                    viewModel = viewModel,
                    onBack = { currentScreen = "main" },
                    onMessageClick = {
                        val req = viewModel.myRequests.value.find { it.matchId == selectedMatch!!.id } ?: viewModel.myNotifications.value.find { it.matchId == selectedMatch!!.id }
                        if (req != null) {
                            selectedRequest = req
                            currentScreen = "chat"
                        } else {
                            currentTab = "Messages"
                            currentScreen = "main"
                        }
                    },
                    userName = name,
                    onPosterClick = {
                        targetUserId = it
                        currentScreen = "userProfile"
                    }
                )
            }
            currentScreen == "notifications" -> {
                NotificationsScreen(viewModel = viewModel, onBack = { currentScreen = "main" })
            }
            currentScreen == "chat" && selectedRequest != null -> {
                ChatScreen(request = selectedRequest!!, viewModel = viewModel, onBack = { currentScreen = "main" })
            }
            currentScreen == "main" -> {
                Column(modifier = Modifier.fillMaxSize()) {
                    Box(modifier = Modifier.weight(1f)) {
                        when (currentTab) {
                            "Home" -> FeedScreen(viewModel, onMatchClick = { 
                                selectedMatch = it
                                currentScreen = "postDetail"
                            }, onNotificationsClick = {
                                currentScreen = "notifications"
                            }, userName = name, onPosterClick = {
                                targetUserId = it
                                currentScreen = "userProfile"
                            })
                            "Live" -> LiveScreen()
                            "CreatePost" -> CreatePostScreen(viewModel = viewModel, onPostCreated = { currentTab = "Home" })
                            "Messages" -> MessagesScreen(viewModel = viewModel, onChatClick = { req -> selectedRequest = req; currentScreen = "chat" })
                            "Profile" -> ProfileScreen(viewModel, onEditProfileClick = { currentScreen = "editProfile" }, onLogoutClick = { viewModel.auth.signOut(); currentScreen = "auth" })
                            "userProfile" -> if (targetUserId != null) UserProfileScreen(targetUserId = targetUserId!!, viewModel = viewModel, onBack = { currentScreen = "main" })
                        }
                    }
                    
                    // Bottom Navigation Bar
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(Turf)
                            .border(1.dp, Line)
                            .padding(vertical = 12.dp, horizontal = 24.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        BottomNavItem(icon = Icons.Default.Home, label = "Home", isSelected = currentTab == "Home", onClick = { currentTab = "Home" })
                        BottomNavItem(icon = Icons.Default.PlayArrow, label = "Live", isSelected = currentTab == "Live", onClick = { currentTab = "Live" })
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .clip(CircleShape)
                                .background(Floodlight)
                                .clickable { currentTab = "CreatePost" },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.Add, contentDescription = "Add", tint = Pitch)
                        }
                        BottomNavItem(icon = Icons.Default.Email, label = "Messages", isSelected = currentTab == "Messages", onClick = { currentTab = "Messages" })
                        BottomNavItem(icon = Icons.Default.Person, label = "Profile", isSelected = currentTab == "Profile", onClick = { currentTab = "Profile" })
                    }
                }
            }
        }
    }
}

@Composable
fun StepDots(active: Int) {
    Row(
        horizontalArrangement = Arrangement.Center,
        modifier = Modifier
            .fillMaxWidth()
            .padding(bottom = 28.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        for (i in 0..2) {
            Box(
                modifier = Modifier
                    .padding(horizontal = 3.dp)
                    .width(if (i == active) 20.dp else 6.dp)
                    .height(6.dp)
                    .clip(CircleShape)
                    .background(if (i == active) Floodlight else Line)
            )
        }
    }
}


@Composable
fun FeedScreen(viewModel: MaidanViewModel, onMatchClick: (MatchEntity) -> Unit, onNotificationsClick: () -> Unit, userName: String, onPosterClick: (String) -> Unit) {
    val matches by viewModel.allMatches.collectAsStateWithLifecycle()
    val myRequests by viewModel.myRequests.collectAsStateWithLifecycle()
    val uid = viewModel.auth.currentUser?.uid
    var category by remember { mutableStateOf("All") }
    var selectedSubcat by remember { mutableStateOf("All") }
    
    val categories = listOf("All", "Sports", "Online gaming", "Exercise", "Group", "Other")
    val subcats = mapOf(
        "Sports" to listOf("Cricket", "Football", "Badminton", "Basketball", "Volleyball", "Table tennis"),
        "Online gaming" to listOf("BGMI", "Valorant", "FIFA", "Free Fire"),
        "Exercise" to listOf("Running", "Gym", "Yoga", "Cycling"),
        "Group" to listOf("Community", "Study", "Entrepreneur", "IT Development", "Coding")
    )
    
    Column(modifier = Modifier.fillMaxSize()) {
        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 22.dp, vertical = 16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Maidan", color = Chalk, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp)
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(modifier = Modifier.size(36.dp).clip(CircleShape).background(Turf2).clickable { onNotificationsClick() }, contentAlignment = Alignment.Center) {
                    Icon(Icons.Default.Notifications, contentDescription = "Notifications", tint = Floodlight, modifier = Modifier.size(18.dp))
                }
            }
        }
        
        LazyRow(contentPadding = PaddingValues(horizontal = 22.dp), horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.padding(bottom = 12.dp)) {
            items(categories) { c ->
                val isSelected = category == c
                Box(
                    modifier = Modifier.clip(RoundedCornerShape(20.dp))
                        .background(if (isSelected) Floodlight else Turf)
                        .border(1.dp, if (isSelected) Color.Transparent else Line, RoundedCornerShape(20.dp))
                        .clickable { category = c; selectedSubcat = "All" }
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Text(c, color = if (isSelected) Pitch else Bench, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
                }
            }
        }
        
        if (category != "All" && category != "Other") {
            val subs = listOf("All ${category}") + (subcats[category] ?: emptyList())
            LazyRow(contentPadding = PaddingValues(horizontal = 22.dp), horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.padding(bottom = 14.dp)) {
                items(subs) { sub ->
                    val isSelected = selectedSubcat == sub
                    Box(
                        modifier = Modifier.clip(RoundedCornerShape(20.dp))
                            .background(if (isSelected) Chalk else Turf2)
                            .clickable { selectedSubcat = sub }
                            .padding(horizontal = 14.dp, vertical = 6.dp)
                    ) {
                        Text(sub, color = if (isSelected) Pitch else Chalk, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                    }
                }
            }
        }
        
        val filtered = matches.filter { match ->
            val catMatch = category == "All" || match.category == category
            val subcatMatch = selectedSubcat == "All" || selectedSubcat.startsWith("All ") || match.sport == selectedSubcat
            catMatch && subcatMatch
        }
        
        LazyColumn(contentPadding = PaddingValues(horizontal = 22.dp, vertical = 8.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            items(filtered) { match ->
                val req = myRequests.find { it.matchId == match.id }
                val status = if (match.posterId == uid) "mine" else req?.status ?: "none"
                MatchCard(
                    m = match, 
                    onClick = { onMatchClick(match) }, 
                    onJoinClick = { viewModel.requestToJoinMatch(match, userName) },
                    currentStatus = status,
                    onPosterClick = { if (match.posterId.isNotEmpty()) onPosterClick(match.posterId) }
                )
            }
        }
    }
}

@Composable
fun BottomNavItem(icon: androidx.compose.ui.graphics.vector.ImageVector, label: String, isSelected: Boolean, onClick: () -> Unit) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier.clickable(onClick = onClick).padding(8.dp)
    ) {
        Icon(icon, contentDescription = label, tint = if (isSelected) Chalk else Bench, modifier = Modifier.size(24.dp))
        Spacer(modifier = Modifier.height(4.dp))
        Text(label, color = if (isSelected) Chalk else Bench, fontSize = 10.sp, fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal)
    }
}

@Composable
fun MatchCard(m: MatchEntity, onClick: () -> Unit, onJoinClick: (() -> Unit)? = null, currentStatus: String = "none", onPosterClick: (() -> Unit)? = null) {
    Column(
        modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(16.dp)).background(Turf).border(1.dp, Line, RoundedCornerShape(16.dp)).clickable { onClick() }
    ) {
        Row(modifier = Modifier.padding(start = 18.dp, top = 14.dp, end = 18.dp, bottom = 10.dp).clickable { onPosterClick?.invoke() }, verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.size(26.dp).clip(CircleShape).background(Turf2), contentAlignment = Alignment.Center) {
                Text(m.posterName.firstOrNull()?.toString() ?: "?", color = Floodlight, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }
            Spacer(modifier = Modifier.width(8.dp))
            Text(m.posterName, color = Chalk, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.width(8.dp))
            Icon(Icons.Default.Star, contentDescription = null, tint = Floodlight, modifier = Modifier.size(11.dp))
            val ratingDisplay = if (m.posterTrust > 0) String.format("%.1f", m.posterTrust) else "New"
            Text(ratingDisplay, color = Floodlight, fontSize = 11.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
        }
        
        Column(modifier = Modifier.padding(horizontal = 18.dp).padding(bottom = 14.dp)) {
            Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                Text(m.sport.uppercase(), color = Floodlight, fontSize = 11.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.background(Turf2, RoundedCornerShape(20.dp)).padding(horizontal = 10.dp, vertical = 4.dp))
                if (m.audience != "All") {
                    Text("${m.audience} only", color = Bench, fontSize = 11.sp, fontWeight = FontWeight.SemiBold, fontFamily = FontFamily.Monospace, modifier = Modifier.border(1.dp, Line, RoundedCornerShape(20.dp)).padding(horizontal = 10.dp, vertical = 4.dp))
                }
            }
            Text(m.title, color = Chalk, fontSize = 16.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 10.dp))
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(bottom = 4.dp)) {
                Icon(Icons.Default.LocationOn, contentDescription = null, tint = Bench, modifier = Modifier.size(13.dp))
                Spacer(modifier = Modifier.width(6.dp))
                Text(m.location, color = Bench, fontSize = 13.sp)
            }
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.DateRange, contentDescription = null, tint = Bench, modifier = Modifier.size(13.dp))
                Spacer(modifier = Modifier.width(6.dp))
                Text(m.time, color = Bench, fontSize = 13.sp)
            }
        }
        
        androidx.compose.foundation.Canvas(modifier = Modifier.fillMaxWidth().height(1.dp)) {
            drawLine(
                color = Line,
                start = Offset(0f, 0f),
                end = Offset(size.width, 0f),
                pathEffect = PathEffect.dashPathEffect(floatArrayOf(12f, 12f), 0f)
            )
        }
        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 18.dp, vertical = 12.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.Person, contentDescription = null, tint = Bench, modifier = Modifier.size(14.dp))
                Spacer(modifier = Modifier.width(6.dp))
                Text("${m.joined}/${m.total} joined", color = Bench, fontSize = 13.sp, fontFamily = FontFamily.Monospace)
            }
            if (currentStatus == "mine") {
                Button(
                    onClick = { },
                    colors = ButtonDefaults.buttonColors(containerColor = Turf2, contentColor = Bench),
                    shape = RoundedCornerShape(20.dp),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    modifier = Modifier.height(32.dp)
                ) {
                    Text("My Post", fontSize = 13.sp, fontWeight = FontWeight.Bold)
                }
            } else if (currentStatus == "none") {
                Button(
                    onClick = { 
                        onJoinClick?.invoke() 
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = Floodlight, contentColor = Pitch),
                    shape = RoundedCornerShape(20.dp),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    modifier = Modifier.height(32.dp)
                ) {
                    Text("Request to join", fontSize = 13.sp, fontWeight = FontWeight.Bold)
                }
            } else if (currentStatus == "requested" || currentStatus == "pending") {
                Button(
                    onClick = { },
                    colors = ButtonDefaults.buttonColors(containerColor = Turf2, contentColor = Bench),
                    shape = RoundedCornerShape(20.dp),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    modifier = Modifier.height(32.dp)
                ) {
                    Text("Requested", fontSize = 13.sp, fontWeight = FontWeight.Bold)
                }
            } else if (currentStatus == "accepted") {
                Button(
                    onClick = { },
                    colors = ButtonDefaults.buttonColors(containerColor = Turf2, contentColor = Floodlight),
                    shape = RoundedCornerShape(20.dp),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    modifier = Modifier.height(32.dp)
                ) {
                    Text("Joined", fontSize = 13.sp, fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}

@Composable
fun AuthScreen(viewModel: MaidanViewModel, onAuthSuccess: (Boolean) -> Unit, onSignUpClick: () -> Unit) {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var errorMessage by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    var showForgotDialog by remember { mutableStateOf(false) }
    var forgotEmail by remember { mutableStateOf("") }
    val context = androidx.compose.ui.platform.LocalContext.current

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(26.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Welcome Back",
            color = Chalk,
            fontSize = 32.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(bottom = 8.dp)
        )
        Text(
            text = "Sign in to continue.",
            color = Bench,
            fontSize = 15.sp,
            modifier = Modifier.padding(bottom = 32.dp)
        )

        OutlinedTextField(
            value = email,
            onValueChange = { email = it },
            label = { Text("Email") },
            singleLine = true, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
            modifier = Modifier.fillMaxWidth(),
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = Floodlight,
                focusedLabelColor = Floodlight,
                unfocusedBorderColor = Line,
                unfocusedLabelColor = Bench,
                focusedTextColor = Chalk,
                unfocusedTextColor = Chalk
            )
        )
        
        Spacer(modifier = Modifier.height(16.dp))

        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Password") },
            singleLine = true, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
            modifier = Modifier.fillMaxWidth(),
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = Floodlight,
                focusedLabelColor = Floodlight,
                unfocusedBorderColor = Line,
                unfocusedLabelColor = Bench,
                focusedTextColor = Chalk,
                unfocusedTextColor = Chalk
            )
        )

        if (errorMessage.isNotEmpty()) {
            Spacer(modifier = Modifier.height(16.dp))
            Text(errorMessage, color = Whistle, fontSize = 14.sp)
        }

        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
            TextButton(onClick = { showForgotDialog = true }) {
                Text("Forgot Password?", color = Bench, fontSize = 14.sp)
            }
        }
        
        if (showForgotDialog) {
            androidx.compose.material3.AlertDialog(
                onDismissRequest = { showForgotDialog = false },
                title = { Text("Reset Password", color = Chalk) },
                text = {
                    Column {
                        Text("Enter your email address to receive a password reset link.\n\nNote: If you don't see it in your Inbox, please check your Spam/Junk folder.", color = Bench, fontSize = 14.sp, modifier = Modifier.padding(bottom = 16.dp))
                        OutlinedTextField(
                            value = forgotEmail,
                            onValueChange = { forgotEmail = it },
                            label = { Text("Email") },
                            singleLine = true, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedBorderColor = Floodlight,
                                focusedLabelColor = Floodlight,
                                unfocusedBorderColor = Line,
                                unfocusedLabelColor = Bench,
                                focusedTextColor = Chalk,
                                unfocusedTextColor = Chalk
                            ),
                            modifier = Modifier.fillMaxWidth()
                        )
                    }
                },
                confirmButton = {
                    TextButton(onClick = {
                        if (forgotEmail.isNotBlank()) {
                            viewModel.resetPassword(forgotEmail.trim()) { msg ->
                                android.widget.Toast.makeText(context, "Link sent! Please check your Inbox and Spam folder.", android.widget.Toast.LENGTH_LONG).show()
                            }
                            showForgotDialog = false
                        } else {
                            android.widget.Toast.makeText(context, "Please enter an email", android.widget.Toast.LENGTH_SHORT).show()
                        }
                    }) {
                        Text("Send Link", color = Floodlight, fontWeight = FontWeight.Bold)
                    }
                },
                dismissButton = {
                    TextButton(onClick = { showForgotDialog = false }) {
                        Text("Cancel", color = Bench)
                    }
                },
                containerColor = Turf,
                titleContentColor = Chalk,
                textContentColor = Bench
            )
        }

        Spacer(modifier = Modifier.height(16.dp))

        Button(
            onClick = {
                if (email.isBlank() || password.isBlank()) {
                    errorMessage = "Please enter email and password"
                    return@Button
                }
                isLoading = true
                errorMessage = ""
                viewModel.signIn(email.trim(), password.trim(), onSuccess = {
                    isLoading = false
                    onAuthSuccess(false)
                }, onError = {
                    isLoading = false
                    errorMessage = it
                })
            },
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Floodlight, contentColor = Pitch),
            shape = RoundedCornerShape(12.dp)
        ) {
            if (isLoading) {
                CircularProgressIndicator(color = Pitch, modifier = Modifier.size(24.dp))
            } else {
                Text("Sign In", fontSize = 18.sp, fontWeight = FontWeight.Bold)
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        TextButton(onClick = onSignUpClick) {
            Text(
                "Don't have an account? Sign Up",
                color = Bench
            )
        }
    }
}
@Composable
fun PhoneScreen(
    method: String,
    onMethodChange: (String) -> Unit,
    contact: String,
    onContactChange: (String) -> Unit,
    onNext: () -> Unit,
    onSignInClick: () -> Unit,
    isSendingOtp: Boolean = false
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(26.dp)
    ) {
        StepDots(0)
        Text(
            text = "Someone's always\nshort a player.",
            color = Chalk,
            fontSize = 34.sp,
            fontWeight = FontWeight.Bold,
            lineHeight = 40.sp,
            modifier = Modifier.padding(bottom = 10.dp)
        )
        Text(
            text = "Post your game. Find your squad. Play today.",
            color = Bench,
            fontSize = 15.sp,
            modifier = Modifier.padding(bottom = 28.dp)
        )
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(Turf2, RoundedCornerShape(12.dp))
                .padding(4.dp)
        ) {
            MethodButton(
                text = "Phone",
                icon = Icons.Default.Phone,
                isSelected = method == "phone",
                onClick = { onMethodChange("phone") },
                modifier = Modifier.weight(1f)
            )
            MethodButton(
                text = "Email",
                icon = Icons.Default.Email,
                isSelected = method == "email",
                onClick = { onMethodChange("email") },
                modifier = Modifier.weight(1f)
            )
        }
        Spacer(modifier = Modifier.height(16.dp))
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, Line, RoundedCornerShape(12.dp))
                .background(Turf2, RoundedCornerShape(12.dp))
                .padding(horizontal = 14.dp, vertical = 2.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            if (method == "phone") {
                Text("+91", color = Bench, modifier = Modifier.padding(end = 8.dp))
            }
            TextField(
                value = contact,
                onValueChange = onContactChange,
                placeholder = { Text(if (method == "phone") "98765 43210" else "you@email.com", color = Bench) },
                colors = TextFieldDefaults.colors(
                    focusedContainerColor = Color.Transparent,
                    unfocusedContainerColor = Color.Transparent,
                    focusedIndicatorColor = Color.Transparent,
                    unfocusedIndicatorColor = Color.Transparent,
                    focusedTextColor = Chalk,
                    unfocusedTextColor = Chalk,
                    cursorColor = Floodlight
                ),
                singleLine = true, keyboardOptions = KeyboardOptions(keyboardType = if (method == "phone") KeyboardType.Phone else KeyboardType.Email),
                modifier = Modifier.weight(1f)
            )
        }
        Spacer(modifier = Modifier.height(24.dp))
        Button(
            onClick = onNext,
            enabled = !isSendingOtp,
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Floodlight, contentColor = Pitch),
            shape = RoundedCornerShape(12.dp)
        ) {
            if (isSendingOtp) androidx.compose.material3.CircularProgressIndicator(color = Pitch, modifier = Modifier.size(24.dp))
            else Text("Continue", fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }
        
        Spacer(modifier = Modifier.weight(1f))
        
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.Center) {
            TextButton(onClick = onSignInClick) {
                Text("Already have an account? Sign In", color = Bench)
            }
        }
    }
}

@Composable
fun MethodButton(text: String, icon: androidx.compose.ui.graphics.vector.ImageVector, isSelected: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier) {
    val bg = if (isSelected) Floodlight else Color.Transparent
    val color = if (isSelected) Pitch else Bench
    Row(
        horizontalArrangement = Arrangement.Center,
        verticalAlignment = Alignment.CenterVertically,
        modifier = modifier
            .clip(RoundedCornerShape(9.dp))
            .background(bg)
            .clickable(onClick = onClick)
            .padding(vertical = 10.dp)
    ) {
        Icon(icon, contentDescription = null, tint = color, modifier = Modifier.size(15.dp))
        Spacer(modifier = Modifier.width(6.dp))
        Text(text, color = color, fontWeight = FontWeight.SemiBold, fontSize = 14.sp)
    }
}

@Composable
fun OtpScreen(
    contact: String,
    otp: String,
    onOtpChange: (String) -> Unit,
    onBack: () -> Unit,
    onNext: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(26.dp)
    ) {
        IconButton(onClick = onBack, modifier = Modifier.padding(bottom = 18.dp)) {
            Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = Bench)
        }
        StepDots(1)
        Text("Enter the code", color = Chalk, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp, modifier = Modifier.padding(bottom = 8.dp))
        Text("Sent to ${if (contact.isEmpty()) "your number" else contact}", color = Bench, fontSize = 14.sp, modifier = Modifier.padding(bottom = 28.dp))
        
        TextField(
            value = otp,
            onValueChange = { if (it.length <= 6) onOtpChange(it) },
            placeholder = { Text("000000", color = Bench) },
            colors = TextFieldDefaults.colors(
                focusedContainerColor = Color.Transparent,
                unfocusedContainerColor = Color.Transparent,
                focusedIndicatorColor = Line,
                unfocusedIndicatorColor = Line,
                focusedTextColor = Chalk,
                unfocusedTextColor = Chalk,
                cursorColor = Floodlight
            ),
            singleLine = true, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            modifier = Modifier.fillMaxWidth(),
            textStyle = androidx.compose.ui.text.TextStyle(fontSize = 24.sp, letterSpacing = 8.sp, textAlign = TextAlign.Center)
        )
        Spacer(modifier = Modifier.height(32.dp))
        Button(
            onClick = onNext,
                        modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Floodlight, contentColor = Pitch),
            shape = RoundedCornerShape(12.dp)
        ) {
            Text("Verify", fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }
    }
}

@OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)
@Composable
fun ProfileSetupScreen(
    name: String, onNameChange: (String) -> Unit,
    age: String, onAgeChange: (String) -> Unit,
    gender: String, onGenderChange: (String) -> Unit,
    selectedSports: List<String>, onToggleSport: (String) -> Unit,
    password: String = "", onPasswordChange: (String) -> Unit = {},
    onBack: () -> Unit, onNext: () -> Unit,
    photoBase64: String = "", onPhotoCaptured: (String) -> Unit = {}
) {
    val sportsList = listOf("Cricket", "Football", "Badminton", "Basketball", "Volleyball", "Table tennis", "Running", "Gym", "Online gaming", "Exercise")
    
    val context = androidx.compose.ui.platform.LocalContext.current
    
    val launcher = androidx.activity.compose.rememberLauncherForActivityResult(
        contract = androidx.activity.result.contract.ActivityResultContracts.TakePicturePreview()
    ) { bitmap: android.graphics.Bitmap? ->
        if (bitmap != null) {
            val outputStream = java.io.ByteArrayOutputStream()
            bitmap.compress(android.graphics.Bitmap.CompressFormat.JPEG, 80, outputStream)
            val byteArray = outputStream.toByteArray()
            val base64 = android.util.Base64.encodeToString(byteArray, android.util.Base64.DEFAULT)
            onPhotoCaptured(base64)
        }
    }

    val cameraPermissionLauncher = androidx.activity.compose.rememberLauncherForActivityResult(
        contract = androidx.activity.result.contract.ActivityResultContracts.RequestPermission()
    ) { isGranted: Boolean ->
        if (isGranted) {
            launcher.launch(null)
        }
    }
    
    val canProceed = name.isNotBlank() && age.isNotBlank() && photoBase64.isNotBlank()
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(26.dp)
            .verticalScroll(rememberScrollState())
    ) {
        IconButton(onClick = onBack, modifier = Modifier.padding(bottom = 18.dp)) {
            Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = Bench)
        }
        StepDots(2)
        Text("Build your profile", color = Chalk, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = (-1).sp, modifier = Modifier.padding(bottom = 16.dp))
        
        Text("Take a live photo for your profile (Required)", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 8.dp))
        Box(
            modifier = Modifier
                .size(100.dp)
                .clip(CircleShape)
                .background(Turf2)
                .border(2.dp, if (photoBase64.isEmpty()) Line else Floodlight, CircleShape)
                .clickable {
                    if (androidx.core.content.ContextCompat.checkSelfPermission(context, android.Manifest.permission.CAMERA) == android.content.pm.PackageManager.PERMISSION_GRANTED) {
                        launcher.launch(null)
                    } else {
                        cameraPermissionLauncher.launch(android.Manifest.permission.CAMERA)
                    }
                }
                .align(Alignment.CenterHorizontally)
                .padding(bottom = 16.dp),
            contentAlignment = Alignment.Center
        ) {
            if (photoBase64.isNotEmpty()) {
                val imageBytes = android.util.Base64.decode(photoBase64, android.util.Base64.DEFAULT)
                val bitmap = android.graphics.BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
                if (bitmap != null) {
                    androidx.compose.foundation.Image(
                        bitmap = bitmap.asImageBitmap(),
                        contentDescription = "Profile Photo",
                        modifier = Modifier.fillMaxSize().clip(CircleShape),
                        contentScale = ContentScale.Crop
                    )
                }
            } else {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Default.Add, contentDescription = "Take Photo", tint = Bench)
                    Text("Camera", color = Bench, fontSize = 10.sp)
                }
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
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
        
        Text("FAVORITE SPORTS", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 8.dp))
        @OptIn(ExperimentalLayoutApi::class)
        FlowRow(modifier = Modifier.fillMaxWidth().padding(bottom = 24.dp), horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            sportsList.forEach { s ->
                val isSelected = selectedSports.contains(s)
                Box(
                    modifier = Modifier.clip(RoundedCornerShape(10.dp))
                        .background(if (isSelected) Floodlight else Turf2)
                        .border(if (isSelected) 0.dp else 1.dp, if (isSelected) Color.Transparent else Line, RoundedCornerShape(10.dp))
                        .clickable { onToggleSport(s) }
                        .padding(horizontal = 14.dp, vertical = 8.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(s, color = if (isSelected) Pitch else Chalk, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                }
            }
        }
        
        OutlinedTextField(
            value = password,
            onValueChange = onPasswordChange,
            label = { Text("Password (for next login)") },
            visualTransformation = androidx.compose.ui.text.input.PasswordVisualTransformation(),
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = Floodlight,
                focusedLabelColor = Floodlight,
                unfocusedBorderColor = Line,
                unfocusedLabelColor = Bench,
                focusedTextColor = Chalk,
                unfocusedTextColor = Chalk
            ),
            modifier = Modifier.fillMaxWidth().padding(bottom = 26.dp)
        )
        
        Button(
            onClick = onNext,
            enabled = canProceed,
            colors = ButtonDefaults.buttonColors(containerColor = Floodlight, contentColor = Pitch, disabledContainerColor = Turf2, disabledContentColor = Bench),
            modifier = Modifier.fillMaxWidth().height(50.dp),
            shape = RoundedCornerShape(12.dp)
        ) {
            Text(if (photoBase64.isEmpty()) "Take Photo to Continue" else "Complete Profile", fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }
    }
}
