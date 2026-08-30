package com.example

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.zegocloud.uikit.prebuilt.livestreaming.ZegoUIKitPrebuiltLiveStreamingConfig
import com.zegocloud.uikit.prebuilt.livestreaming.ZegoUIKitPrebuiltLiveStreamingFragment

class LiveActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val isHost = intent.getBooleanExtra("isHost", false)
        val liveID = intent.getStringExtra("liveID") ?: "test_live_id"
        val userID = intent.getStringExtra("userID") ?: "user_${System.currentTimeMillis()}"
        val userName = intent.getStringExtra("userName") ?: "User"
        val appID: Long = 259383851L
        val appSign = "ead2e75a111bd2bfaddc3d0687cdd98175b3398"
        
        val config = if (isHost) {
            ZegoUIKitPrebuiltLiveStreamingConfig.host(true)
        } else {
            ZegoUIKitPrebuiltLiveStreamingConfig.audience(true)
        }
        
        try {
            val fragment = ZegoUIKitPrebuiltLiveStreamingFragment.newInstance(
                appID, appSign, userID, userName, liveID, config
            )
            
            supportFragmentManager.beginTransaction()
                .replace(android.R.id.content, fragment)
                .commitNow()
        } catch (e: Exception) {
            e.printStackTrace()
            android.widget.Toast.makeText(this, "Failed to start Zego SDK. Check AppSign.", android.widget.Toast.LENGTH_LONG).show()
            finish()
        }
    }
}
