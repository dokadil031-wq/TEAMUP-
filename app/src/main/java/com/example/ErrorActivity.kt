package com.example

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ui.theme.MyApplicationTheme

class ErrorActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val errorDetails = intent.getStringExtra("EXTRA_ERROR_DETAILS") ?: "Unknown Error"
        val errorMessage = intent.getStringExtra("EXTRA_ERROR_MESSAGE") ?: ""

        val friendlyMessage: String
        val fixAdvice: String

        when {
            errorDetails.contains("Zego", ignoreCase = true) || errorDetails.contains("Live", ignoreCase = true) -> {
                friendlyMessage = "Live Feature Error"
                fixAdvice = "API keys are missing or invalid. Please download the APK directly from AI Studio instead of GitHub."
            }
            errorDetails.contains("Firebase", ignoreCase = true) || errorDetails.contains("auth", ignoreCase = true) -> {
                friendlyMessage = "Authentication Issue"
                fixAdvice = "There was a problem verifying your account. Please check your internet connection and try logging in again."
            }
            errorDetails.contains("ConnectException", ignoreCase = true) || errorDetails.contains("UnknownHostException", ignoreCase = true) -> {
                friendlyMessage = "Network Connection Error"
                fixAdvice = "The app couldn't reach the server. Please check your WiFi or mobile data connection."
            }
            errorDetails.contains("SecurityException", ignoreCase = true) -> {
                friendlyMessage = "Permission Denied"
                fixAdvice = "The app needs certain permissions (like Camera, Mic, or Location) to work. Please enable them in your phone settings."
            }
            errorDetails.contains("OutOfMemoryError", ignoreCase = true) -> {
                friendlyMessage = "Memory Full"
                fixAdvice = "Your phone ran out of memory. Please close other apps and try again."
            }
            else -> {
                friendlyMessage = "App Crash Prevented"
                fixAdvice = "An unexpected system error occurred. We have caught it so your phone doesn't freeze. Please restart the app."
            }
        }

        setContent {
            MyApplicationTheme {
                Surface(modifier = Modifier.fillMaxSize(), color = Pitch) {
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(24.dp)
                            .verticalScroll(rememberScrollState()),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        Icon(
                            Icons.Default.Warning,
                            contentDescription = "Error Warning",
                            tint = Whistle,
                            modifier = Modifier.size(72.dp)
                        )
                        Spacer(modifier = Modifier.height(24.dp))
                        Text(
                            text = friendlyMessage,
                            color = Chalk,
                            fontSize = 28.sp,
                            fontWeight = FontWeight.Bold,
                            textAlign = TextAlign.Center
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(
                            text = "How to fix this:",
                            color = Floodlight,
                            fontSize = 20.sp,
                            fontWeight = FontWeight.SemiBold
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        Text(
                            text = fixAdvice,
                            color = Bench,
                            fontSize = 16.sp,
                            textAlign = TextAlign.Center
                        )

                        Spacer(modifier = Modifier.height(40.dp))

                        var showDetails by remember { mutableStateOf(false) }
                        TextButton(onClick = { showDetails = !showDetails }) {
                            Text(
                                if (showDetails) "Hide Technical Code" else "View Technical Error Code",
                                color = Bench
                            )
                        }

                        if (showDetails) {
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = errorDetails,
                                color = Color(0xFFFF8A80),
                                fontSize = 12.sp,
                                modifier = Modifier
                                    .background(Color.Black.copy(alpha = 0.3f))
                                    .padding(12.dp)
                                    .fillMaxWidth()
                            )
                        }

                        Spacer(modifier = Modifier.height(40.dp))

                        Button(
                            onClick = {
                                val restartIntent = Intent(this@ErrorActivity, MainActivity::class.java)
                                restartIntent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_NEW_TASK)
                                startActivity(restartIntent)
                                finish()
                            },
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(56.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = Floodlight, contentColor = Pitch),
                            shape = RoundedCornerShape(12.dp)
                        ) {
                            Text("Restart App", fontSize = 18.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
        }
    }
}
