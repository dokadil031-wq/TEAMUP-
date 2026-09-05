package com.example

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.auth.FirebaseAuth
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import com.google.firebase.firestore.Query

class MaidanViewModel(application: Application) : AndroidViewModel(application) {
    val db by lazy { FirebaseFirestore.getInstance() }
    val auth by lazy { FirebaseAuth.getInstance() }
    private val userPrefsRepo = UserPreferencesRepository(application.dataStore)

    private val _allMatches = MutableStateFlow<List<MatchEntity>>(emptyList())
    val allMatches: StateFlow<List<MatchEntity>> = _allMatches.asStateFlow()

    private val _myRequests = MutableStateFlow<List<MatchRequest>>(emptyList())
    val myRequests: StateFlow<List<MatchRequest>> = _myRequests.asStateFlow()

    private val _myNotifications = MutableStateFlow<List<MatchRequest>>(emptyList())
    val myNotifications: StateFlow<List<MatchRequest>> = _myNotifications.asStateFlow()

    val userName: StateFlow<String> = userPrefsRepo.userName.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "")
    val userAge: StateFlow<String> = userPrefsRepo.userAge.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "")
    val userGender: StateFlow<String> = userPrefsRepo.userGender.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "Male")
    val userSports: StateFlow<List<String>> = userPrefsRepo.userSports.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
    val userImage: StateFlow<String> = userPrefsRepo.userImage.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "")
    val userCity: StateFlow<String> = userPrefsRepo.userCity.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "")

    init {
        auth.firebaseAuthSettings.setAppVerificationDisabledForTesting(true)
        listenToMatches()
        viewModelScope.launch {
            while (true) {
                kotlinx.coroutines.delay(30000) // check every 30 seconds
                checkAndDeleteExpiredMatches()
            }
        }
        
        auth.addAuthStateListener {
            if (it.currentUser != null) {
                listenToMyRequests()
                listenToMyNotifications()
                db.collection("users").document(it.currentUser!!.uid).get().addOnSuccessListener { doc ->
                    if (doc.exists()) {
                        val p = doc.toObject(UserProfile::class.java)
                        if (p != null) {
                            viewModelScope.launch {
                                userPrefsRepo.saveUserProfile(p.name, p.age, p.gender, p.sports)
                                if (p.profileImageBase64.isNotEmpty()) {
                                    userPrefsRepo.saveUserImage(p.profileImageBase64)
                                }
                                if (p.city.isNotEmpty()) {
                                    userPrefsRepo.saveUserCity(p.city)
                                }
                            }
                        }
                    }
                }
            } else {
                _myRequests.value = emptyList()
                _myNotifications.value = emptyList()
                viewModelScope.launch {
                    userPrefsRepo.clearProfile()
                }
            }
        }
    }
    
    private fun listenToMyRequests() {
        val uid = auth.currentUser?.uid ?: return
        db.collection("requests").whereEqualTo("requesterId", uid).addSnapshotListener { snap, err ->
            if (snap != null) {
                _myRequests.value = snap.documents.mapNotNull { it.toObject(MatchRequest::class.java)?.apply { id = it.id } }
            }
        }
    }
    
    private fun listenToMyNotifications() {
        val uid = auth.currentUser?.uid ?: return
        db.collection("requests").whereEqualTo("posterId", uid).addSnapshotListener { snap, err ->
            if (snap != null) {
                _myNotifications.value = snap.documents.mapNotNull { it.toObject(MatchRequest::class.java)?.apply { id = it.id } }
            }
        }
    }

    private fun listenToMatches() {
        db.collection("matches").addSnapshotListener { snapshot, error ->
            if (error != null) {
                android.util.Log.e("FirestoreError", "Listen failed.", error)
                return@addSnapshotListener
            }
            if (snapshot != null) {
                val matches = snapshot.documents.mapNotNull { doc ->
                    doc.toObject(MatchEntity::class.java)?.apply { id = doc.id }
                }
                
                val currentTime = System.currentTimeMillis()
                val validMatches = mutableListOf<MatchEntity>()
                
                for (match in matches) {
                    var shouldDelete = false
                    if (match.fullAtTimestamp != null && match.fullAtTimestamp > 0) {
                        // 30 minutes = 30 * 60 * 1000 = 1800000 ms
                        if (currentTime >= match.fullAtTimestamp + 1800000L) {
                            shouldDelete = true
                        }
                    } else if (match.joined >= match.total && match.timestamp > 0) {
                        // Fallback for legacy matches
                        if (currentTime >= match.timestamp + 1800000L) {
                            shouldDelete = true
                        }
                    } else if (match.joined < match.total && match.timestamp > 0) {
                        // Delete right at match time if not full
                        if (currentTime >= match.timestamp) {
                            shouldDelete = true
                        }
                    }
                    
                    if (shouldDelete) {
                        db.collection("matches").document(match.id).delete()
                    } else {
                        validMatches.add(match)
                    }
                }
                _allMatches.value = validMatches
            }
        }
    }

    private fun checkAndDeleteExpiredMatches() {
        val currentTime = System.currentTimeMillis()
        val currentMatches = _allMatches.value
        for (match in currentMatches) {
            var shouldDelete = false
            if (match.fullAtTimestamp != null && match.fullAtTimestamp > 0) {
                if (currentTime >= match.fullAtTimestamp + 1800000L) {
                    shouldDelete = true
                }
            } else if (match.joined >= match.total && match.timestamp > 0) {
                if (currentTime >= match.timestamp + 1800000L) {
                    shouldDelete = true
                }
            } else if (match.joined < match.total && match.timestamp > 0) {
                if (currentTime >= match.timestamp) {
                    shouldDelete = true
                }
            }
            if (shouldDelete) {
                db.collection("matches").document(match.id).delete()
            }
        }
    }

    private fun insertInitialDataIfNeeded() {
        val initial = listOf(
            MatchEntity(category = "Sports", sport = "Cricket", title = "Sunday morning cricket, need 3 more", location = "DLF Ground, Sector 14", time = "Tomorrow, 7:00 AM", joined = 5, total = 8, audience = "All", posterName = "Rahul Verma", posterTrust = 4.8),
            MatchEntity(category = "Sports", sport = "Badminton", title = "Evening doubles, casual level", location = "Indoor Court, Sector 21", time = "Today, 6:30 PM", joined = 2, total = 4, audience = "Female", posterName = "Priya Sharma", posterTrust = 4.9),
            MatchEntity(category = "Sports", sport = "Football", title = "5-a-side, need a keeper", location = "Turf Arena, Sector 29", time = "Sat, 5:00 PM", joined = 8, total = 10, audience = "All", posterName = "Arjun Mehta", posterTrust = 3.9),
            MatchEntity(category = "Online gaming", sport = "BGMI", title = "Squad push, ranked grind tonight", location = "Online", time = "Today, 9:00 PM", joined = 2, total = 4, audience = "All", posterName = "Arjun Mehta", posterTrust = 3.9),
            MatchEntity(category = "Exercise", sport = "Running", title = "5K morning run, easy pace", location = "City Park, Gate 2", time = "Tomorrow, 6:00 AM", joined = 4, total = 12, audience = "All", posterName = "Sneha Kulkarni", posterTrust = 4.6)
        )
        viewModelScope.launch {
            initial.forEach { addMatch(it) }
        }
    }

    fun saveUserProfile(name: String, age: String, gender: String, sports: List<String>) {
        viewModelScope.launch {
            userPrefsRepo.saveUserProfile(name, age, gender, sports)
        }
        val uid = auth.currentUser?.uid ?: return
        db.collection("users").document(uid).get().addOnSuccessListener { doc ->
            val existingRating = doc.getDouble("averageRating") ?: 0.0
            val existingCount = doc.getLong("reviewCount")?.toInt() ?: 0
            val existingImage = doc.getString("profileImageBase64") ?: ""
            val existingCity = doc.getString("city") ?: ""
            val profile = UserProfile(uid, name, age, gender, sports, existingRating, existingCount, existingImage, existingCity)
            db.collection("users").document(uid).set(profile)
        }.addOnFailureListener {
            val profile = UserProfile(uid, name, age, gender, sports, 0.0, 0, "", "")
            db.collection("users").document(uid).set(profile)
        }
    }

    fun updateUserCity(city: String) {
        viewModelScope.launch {
            userPrefsRepo.saveUserCity(city)
        }
        val uid = auth.currentUser?.uid ?: return
        db.collection("users").document(uid).update("city", city)
    }

    fun updateProfilePhoto(base64: String) {
        val uid = auth.currentUser?.uid ?: return
        viewModelScope.launch {
            userPrefsRepo.saveUserImage(base64)
        }
        db.collection("users").document(uid).update("profileImageBase64", base64)
        db.collection("matches").whereEqualTo("posterId", uid).get().addOnSuccessListener { snap ->
            if (!snap.isEmpty) {
                db.runBatch { batch ->
                    snap.documents.forEach { doc ->
                        batch.update(doc.reference, "posterImageBase64", base64)
                    }
                }
            }
        }
    }

    fun addMatch(match: MatchEntity) {
        val ref = db.collection("matches").document()
        ref.set(match.copy(id = ref.id, posterId = auth.currentUser?.uid ?: "")).addOnFailureListener {
            android.util.Log.e("FirestoreError", "Add match failed.", it)
        }
    }

    fun joinMatch(match: MatchEntity) {
        if (match.id.isNotEmpty()) {
            db.collection("matches").document(match.id).update("joined", match.joined + 1)
        }
    }

    fun requestToJoinMatch(match: MatchEntity, userName: String) {
        val uid = auth.currentUser?.uid ?: return
        val req = MatchRequest(
            matchId = match.id,
            matchTitle = match.title,
            requesterId = uid,
            requesterName = userName,
            posterId = match.posterId,
            status = "pending"
        )
        val ref = db.collection("requests").document()
        ref.set(req.copy(id = ref.id))
    }
    
    fun cancelRequest(matchId: String) {
        val uid = auth.currentUser?.uid ?: return
        db.collection("requests")
            .whereEqualTo("requesterId", uid)
            .whereEqualTo("matchId", matchId)
            .get()
            .addOnSuccessListener { snap ->
                snap.documents.forEach { doc ->
                    val status = doc.getString("status")
                    doc.reference.delete()
                    if (status == "accepted") {
                        // Reduce joined count and remove fullAtTimestamp if necessary
                        db.collection("matches").document(matchId).get().addOnSuccessListener { matchDoc ->
                            val joined = matchDoc.getLong("joined")?.toInt() ?: 0
                            val newJoined = if (joined > 0) joined - 1 else 0
                            matchDoc.reference.update(mapOf(
                                "joined" to newJoined,
                                "fullAtTimestamp" to null
                            ))
                        }
                    }
                }
            }
    }
    
    fun acceptRequest(req: MatchRequest) {
        db.collection("requests").document(req.id).update("status", "accepted")
        db.collection("matches").document(req.matchId).get().addOnSuccessListener { doc ->
            val joined = doc.getLong("joined")?.toInt() ?: 0
            val total = doc.getLong("total")?.toInt() ?: 0
            val newJoined = joined + 1
            if (newJoined >= total) {
                doc.reference.update(mapOf(
                    "joined" to newJoined,
                    "fullAtTimestamp" to System.currentTimeMillis()
                ))
            } else {
                doc.reference.update("joined", newJoined)
            }
        }
    }
    
    fun rejectRequest(req: MatchRequest) {
        db.collection("requests").document(req.id).delete()
    }
    
    fun getUserProfile(userId: String, onResult: (UserProfile?) -> Unit) {
        db.collection("users").document(userId).addSnapshotListener { snap, _ ->
            if (snap != null && snap.exists()) {
                onResult(snap.toObject(UserProfile::class.java))
            } else {
                onResult(null)
            }
        }
    }

    fun getUserReviews(userId: String, onUpdate: (List<UserReview>) -> Unit) {
        db.collection("reviews").whereEqualTo("targetUserId", userId)
            .orderBy("timestamp", Query.Direction.DESCENDING)
            .addSnapshotListener { snap, _ ->
                if (snap != null) {
                    onUpdate(snap.documents.mapNotNull { it.toObject(UserReview::class.java)?.apply { id = it.id } })
                }
            }
    }

    fun submitReview(targetUserId: String, rating: Float, text: String, reviewerName: String) {
        val uid = auth.currentUser?.uid ?: return
        if (uid == targetUserId) return // Can't review self

        val ref = db.collection("reviews").document()
        val review = UserReview(
            id = ref.id,
            reviewerId = uid,
            reviewerName = reviewerName,
            targetUserId = targetUserId,
            rating = rating,
            reviewText = text,
            timestamp = System.currentTimeMillis()
        )
        
        ref.set(review).addOnSuccessListener {
            // Update user's average rating
            db.collection("reviews").whereEqualTo("targetUserId", targetUserId).get().addOnSuccessListener { snap ->
                val reviews = snap.documents.mapNotNull { it.toObject(UserReview::class.java) }
                val newCount = reviews.size
                val newAvg = if (newCount > 0) reviews.map { it.rating }.average() else 0.0
                
                db.collection("users").document(targetUserId).update(
                    mapOf("averageRating" to newAvg, "reviewCount" to newCount)
                )
                
                // Also update the user's matches so MatchCard shows new rating
                db.collection("matches").whereEqualTo("posterId", targetUserId).get().addOnSuccessListener { matchSnap ->
                    db.runBatch { batch ->
                        matchSnap.documents.forEach { doc ->
                            batch.update(doc.reference, "posterTrust", newAvg)
                        }
                    }
                }
            }
        }
    }

    fun getMessages(requestId: String, onUpdate: (List<ChatMessage>) -> Unit) {
        db.collection("requests").document(requestId).collection("messages")
            .orderBy("timestamp", Query.Direction.ASCENDING)
            .addSnapshotListener { snap, _ ->
                if (snap != null) {
                    onUpdate(snap.documents.mapNotNull { it.toObject(ChatMessage::class.java)?.apply { id = it.id } })
                }
            }
    }
    
    fun sendMessage(requestId: String, text: String) {
        val uid = auth.currentUser?.uid ?: return
        val ref = db.collection("requests").document(requestId).collection("messages").document()
        ref.set(ChatMessage(id = ref.id, senderId = uid, text = text, timestamp = System.currentTimeMillis()))
    }

    fun signUp(email: String, pass: String, onSuccess: () -> Unit, onError: (String) -> Unit) {
        auth.createUserWithEmailAndPassword(email, pass)
            .addOnSuccessListener { onSuccess() }
            .addOnFailureListener { onError(it.message ?: "Error") }
    }

    fun signIn(email: String, pass: String, onSuccess: () -> Unit, onError: (String) -> Unit) {
        auth.signInWithEmailAndPassword(email, pass)
            .addOnSuccessListener { onSuccess() }
            .addOnFailureListener { onError(it.message ?: "Error") }
    }
    
    fun signInAnonymously(onSuccess: () -> Unit, onError: (String) -> Unit) {
        auth.signInAnonymously()
            .addOnSuccessListener { onSuccess() }
            .addOnFailureListener { onError(it.message ?: "Error") }
    }

    fun resetPassword(email: String, onResult: (String) -> Unit) {
        auth.sendPasswordResetEmail(email)
            .addOnSuccessListener { onResult("Password reset email sent.") }
            .addOnFailureListener { onResult(it.message ?: "Failed to send reset email.") }
    }

    fun updatePassword(password: String, onResult: (String) -> Unit) {
        auth.currentUser?.updatePassword(password)
            ?.addOnSuccessListener { onResult("Password updated successfully.") }
            ?.addOnFailureListener { onResult(it.message ?: "Failed to update password.") }
            ?: onResult("User not logged in.")
    }
}
