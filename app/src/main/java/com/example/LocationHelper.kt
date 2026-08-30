package com.example

import android.annotation.SuppressLint
import android.content.Context
import android.location.Geocoder
import android.location.Location
import com.google.android.gms.location.LocationServices
import kotlinx.coroutines.tasks.await
import java.util.Locale

object LocationHelper {
    @SuppressLint("MissingPermission")
    suspend fun getCurrentCity(context: Context): String? {
        return try {
            val fusedLocationClient = LocationServices.getFusedLocationProviderClient(context)
            val location: Location? = fusedLocationClient.lastLocation.await()
            if (location != null) {
                val geocoder = Geocoder(context, Locale.getDefault())
                val addresses = geocoder.getFromLocation(location.latitude, location.longitude, 1)
                if (!addresses.isNullOrEmpty()) {
                    addresses[0].locality ?: addresses[0].subAdminArea ?: addresses[0].adminArea
                } else null
            } else null
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }
}
