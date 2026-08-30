package com.example

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "user_prefs")

class UserPreferencesRepository(private val dataStore: DataStore<Preferences>) {
    private val NAME_KEY = stringPreferencesKey("user_name")
    private val AGE_KEY = stringPreferencesKey("user_age")
    private val GENDER_KEY = stringPreferencesKey("user_gender")
    private val SPORTS_KEY = stringPreferencesKey("user_sports")
    private val IMAGE_KEY = stringPreferencesKey("user_image")
    private val CITY_KEY = stringPreferencesKey("user_city")

    val userName: Flow<String> = dataStore.data.map { preferences ->
        preferences[NAME_KEY] ?: ""
    }
    
    val userAge: Flow<String> = dataStore.data.map { preferences ->
        preferences[AGE_KEY] ?: ""
    }
    
    val userGender: Flow<String> = dataStore.data.map { preferences ->
        preferences[GENDER_KEY] ?: "Male"
    }
    
    val userSports: Flow<List<String>> = dataStore.data.map { preferences ->
        val sportsString = preferences[SPORTS_KEY] ?: ""
        if (sportsString.isEmpty()) emptyList() else sportsString.split(",")
    }
    
    val userImage: Flow<String> = dataStore.data.map { preferences ->
        preferences[IMAGE_KEY] ?: ""
    }

    val userCity: Flow<String> = dataStore.data.map { preferences ->
        preferences[CITY_KEY] ?: ""
    }

    suspend fun saveUserProfile(name: String, age: String, gender: String, sports: List<String>) {
        dataStore.edit { preferences ->
            preferences[NAME_KEY] = name
            preferences[AGE_KEY] = age
            preferences[GENDER_KEY] = gender
            preferences[SPORTS_KEY] = sports.joinToString(",")
        }
    }
    
    suspend fun saveUserImage(base64: String) {
        dataStore.edit { preferences ->
            preferences[IMAGE_KEY] = base64
        }
    }

    suspend fun saveUserCity(city: String) {
        dataStore.edit { preferences ->
            preferences[CITY_KEY] = city
        }
    }
    
    suspend fun clearProfile() {
        dataStore.edit { preferences ->
            preferences.clear()
        }
    }
}
