package com.example

import android.app.Application
import com.google.firebase.FirebaseApp
import android.util.Log

class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        try {
            FirebaseApp.initializeApp(this)
            Log.d("INIT", "Firebase init success in Application class")
        } catch(e: Exception) {
            e.printStackTrace()
            Log.e("INIT", "Firebase init failed in Application class", e)
        }
    }
}
