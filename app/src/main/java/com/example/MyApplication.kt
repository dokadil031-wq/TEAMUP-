package com.example

import android.app.Application
import com.google.firebase.FirebaseApp
import com.google.firebase.FirebaseOptions
import android.util.Log

class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        
        val defaultHandler = Thread.getDefaultUncaughtExceptionHandler()
        Thread.setDefaultUncaughtExceptionHandler(GlobalExceptionHandler(this, defaultHandler))
        
        try {
            if (FirebaseApp.getApps(this).isEmpty()) {
                val options = FirebaseOptions.Builder()
                    .setApplicationId("1:195869990157:android:e5e3d3f99f1094db902444")
                    .setApiKey("AIzaSyAAMwYj_nAAZeIIT_MSRI079Y54np_mlg0")
                    .setDatabaseUrl("https://teamup-bb90b-default-rtdb.firebaseio.com")
                    .setProjectId("teamup-bb90b")
                    .setStorageBucket("teamup-bb90b.firebasestorage.app")
                    .build()
                FirebaseApp.initializeApp(this, options)
                Log.d("INIT", "Firebase explicit init success in Application class")
            }
        } catch(e: Exception) {
            e.printStackTrace()
            Log.e("INIT", "Firebase init failed in Application class", e)
        }
    }
}
