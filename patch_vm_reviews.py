with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    content = f.read()

target = """    fun getMessages(requestId: String, onUpdate: (List<ChatMessage>) -> Unit) {"""
replacement = """    fun getUserProfile(userId: String, onResult: (UserProfile?) -> Unit) {
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

    fun getMessages(requestId: String, onUpdate: (List<ChatMessage>) -> Unit) {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MaidanViewModel.kt", "w") as f:
    f.write(content)
