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
    private val db = FirebaseFirestore.getInstance()
    val auth = FirebaseAuth.getInstance()
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

    init {
        auth.firebaseAuthSettings.setAppVerificationDisabledForTesting(true)
        listenToMatches()
        
        auth.addAuthStateListener {
            if (it.currentUser != null) {
                listenToMyRequests()
                listenToMyNotifications()
            } else {
                _myRequests.value = emptyList()
                _myNotifications.value = emptyList()
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
                _allMatches.value = matches
                
                if (matches.isEmpty()) {
                    insertInitialDataIfNeeded()
                }
            }
        }
    }

    private fun insertInitialDataIfNeeded() {
        val initial = listOf(
            MatchEntity("", "Sports", "Cricket", "Sunday morning cricket, need 3 more", "DLF Ground, Sector 14", "Tomorrow, 7:00 AM", 5, 8, "All", "Rahul Verma", "", 4.8),
            MatchEntity("", "Sports", "Badminton", "Evening doubles, casual level", "Indoor Court, Sector 21", "Today, 6:30 PM", 2, 4, "Female", "Priya Sharma", "", 4.9),
            MatchEntity("", "Sports", "Football", "5-a-side, need a keeper", "Turf Arena, Sector 29", "Sat, 5:00 PM", 8, 10, "All", "Arjun Mehta", "", 3.9),
            MatchEntity("", "Online gaming", "BGMI", "Squad push, ranked grind tonight", "Online", "Today, 9:00 PM", 2, 4, "All", "Arjun Mehta", "", 3.9),
            MatchEntity("", "Exercise", "Running", "5K morning run, easy pace", "City Park, Gate 2", "Tomorrow, 6:00 AM", 4, 12, "All", "Sneha Kulkarni", "", 4.6)
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
            val profile = UserProfile(uid, name, age, gender, sports, existingRating, existingCount, existingImage)
            db.collection("users").document(uid).set(profile)
        }.addOnFailureListener {
            val profile = UserProfile(uid, name, age, gender, sports, 0.0, 0, "")
            db.collection("users").document(uid).set(profile)
        }
    }

    fun updateProfilePhoto(base64: String) {
        val uid = auth.currentUser?.uid ?: return
        viewModelScope.launch {
            userPrefsRepo.saveUserImage(base64)
        }
        db.collection("users").document(uid).update("profileImageBase64", base64)
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
    
    fun acceptRequest(req: MatchRequest) {
        db.collection("requests").document(req.id).update("status", "accepted")
        db.collection("matches").document(req.matchId).get().addOnSuccessListener { doc ->
            val joined = doc.getLong("joined") ?: 0
            doc.reference.update("joined", joined + 1)
        }
    }
    
    fun rejectRequest(req: MatchRequest) {
        db.collection("requests").document(req.id).delete()
    }
    
    fun getUserProfile(userId: String, onResult: (UserProfile?) -> Unit) {
        db.collection("users").document(userId).get()
            .addOnSuccessListener { onResult(it.toObject(UserProfile::class.java)) }
            .addOnFailureListener { onResult(null) }
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
