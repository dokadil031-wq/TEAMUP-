package com.example

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Star
import androidx.compose.material.icons.outlined.StarBorder
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle

@Composable
fun UserProfileScreen(
    targetUserId: String,
    viewModel: MaidanViewModel,
    onBack: () -> Unit
) {
    var profile by remember { mutableStateOf<UserProfile?>(null) }
    var reviews by remember { mutableStateOf<List<UserReview>>(emptyList()) }
    var ratingInput by remember { mutableStateOf(0f) }
    var reviewTextInput by remember { mutableStateOf("") }
    val currentUserName by viewModel.userName.collectAsStateWithLifecycle()
    val currentUserId = viewModel.auth.currentUser?.uid
    val myRequests by viewModel.myRequests.collectAsStateWithLifecycle()
    val myNotifications by viewModel.myNotifications.collectAsStateWithLifecycle()
    
    LaunchedEffect(targetUserId) {
        viewModel.getUserProfile(targetUserId) { profile = it }
        viewModel.getUserReviews(targetUserId) { reviews = it }
    }
    
    Column(modifier = Modifier.fillMaxSize().padding(horizontal = 22.dp, vertical = 16.dp)) {
        IconButton(onClick = onBack, modifier = Modifier.padding(bottom = 18.dp)) {
            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Bench)
        }
        
        if (profile == null) {
            Text("Loading...", color = Chalk)
            return
        }
        
        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(bottom = 24.dp)) {
            Box(modifier = Modifier.size(60.dp).clip(CircleShape).background(Turf2), contentAlignment = Alignment.Center) {
                if (profile!!.profileImageBase64.isNotEmpty()) {
                    val bitmap = remember(profile!!.profileImageBase64) {
                        try {
                            val imageBytes = android.util.Base64.decode(profile!!.profileImageBase64, android.util.Base64.DEFAULT)
                            android.graphics.BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
                        } catch (e: Exception) {
                            null
                        }
                    }
                    if (bitmap != null) {
                        androidx.compose.foundation.Image(bitmap = bitmap.asImageBitmap(), contentDescription = "Profile Photo", modifier = Modifier.fillMaxSize(), contentScale = androidx.compose.ui.layout.ContentScale.Crop)
                    } else {
                        Text(profile!!.name.firstOrNull()?.toString() ?: "?", color = Floodlight, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                    }
                } else {
                    Text(profile!!.name.firstOrNull()?.toString() ?: "?", color = Floodlight, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                }
            }
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(profile!!.name, color = Chalk, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                if (profile!!.age.isNotEmpty() || profile!!.gender.isNotEmpty()) {
                    val ageStr = if (profile!!.age.isNotEmpty()) "${profile!!.age} yrs" else ""
                    val separator = if (profile!!.age.isNotEmpty() && profile!!.gender.isNotEmpty()) " · " else ""
                    val genderStr = profile!!.gender
                    Text("$ageStr$separator$genderStr", color = Bench, fontSize = 13.sp, modifier = Modifier.padding(bottom = 4.dp))
                }
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("TRUST SCORE: ", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
                    Icon(Icons.Default.Star, contentDescription = null, tint = Floodlight, modifier = Modifier.size(14.dp))
                    Spacer(modifier = Modifier.width(2.dp))
                    val avgRating = if (profile!!.reviewCount > 0) String.format("%.1f", profile!!.averageRating) else "New"
                    Text("$avgRating (${profile!!.reviewCount} reviews)", color = Floodlight, fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
                }
            }
        }
        

        
        // Add review section
        if (currentUserId != null && currentUserId != targetUserId) {
            val hasReviewed = reviews.any { it.reviewerId == currentUserId }
            val hasPlayedTogether = myRequests.any { it.posterId == targetUserId && it.status == "accepted" } || 
                                    myNotifications.any { it.requesterId == targetUserId && it.status == "accepted" }
            if (!hasReviewed && hasPlayedTogether) {
                Column(modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(Turf).padding(16.dp).padding(bottom = 24.dp)) {
                    Text("Leave a Review", color = Chalk, fontSize = 16.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 12.dp))
                    Row(modifier = Modifier.padding(bottom = 12.dp)) {
                        (1..5).forEach { i ->
                            Icon(
                                imageVector = if (i <= ratingInput) Icons.Default.Star else Icons.Outlined.StarBorder,
                                contentDescription = "Star $i",
                                tint = Floodlight,
                                modifier = Modifier.size(32.dp).clickable { ratingInput = i.toFloat() }
                            )
                        }
                    }
                    OutlinedTextField(
                        value = reviewTextInput,
                        onValueChange = { reviewTextInput = it },
                        modifier = Modifier.fillMaxWidth().height(100.dp),
                        placeholder = { Text("Write your experience...", color = Bench) },
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Line,
                            unfocusedBorderColor = Line,
                            focusedTextColor = Chalk,
                            unfocusedTextColor = Chalk
                        )
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    Button(
                        onClick = {
                            if (ratingInput > 0) {
                                viewModel.submitReview(targetUserId, ratingInput, reviewTextInput, currentUserName)
                                ratingInput = 0f
                                reviewTextInput = ""
                                // The profile should automatically refresh because it's a SnapshotListener inside the VM? Wait, profile is a one-time get in LaunchedEffect. Let's re-fetch profile manually or rely on users to go back and forth.
                                viewModel.getUserProfile(targetUserId) { profile = it }
                            }
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Floodlight, contentColor = Pitch),
                        shape = RoundedCornerShape(8.dp),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text("Submit Review", fontWeight = FontWeight.Bold)
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
            }
        }
        
        Text("REVIEWS", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, modifier = Modifier.padding(bottom = 8.dp))
        if (reviews.isEmpty()) {
            Text("No reviews yet.", color = Bench, fontSize = 14.sp)
        } else {
            LazyColumn(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                items(reviews) { review ->
                    Column(modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).border(1.dp, Line, RoundedCornerShape(12.dp)).padding(16.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)) {
                            Text(review.reviewerName, color = Chalk, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                            Row {
                                (1..5).forEach { i ->
                                    Icon(
                                        imageVector = if (i <= review.rating) Icons.Default.Star else Icons.Outlined.StarBorder,
                                        contentDescription = null,
                                        tint = Floodlight,
                                        modifier = Modifier.size(14.dp)
                                    )
                                }
                            }
                        }
                        if (review.reviewText.isNotBlank()) {
                            Text(review.reviewText, color = Chalk, fontSize = 14.sp)
                        }
                    }
                }
            }
        }
    }
}
