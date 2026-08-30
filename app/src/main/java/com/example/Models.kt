package com.example

data class MatchRequest(
    var id: String = "",
    val matchId: String = "",
    val matchTitle: String = "",
    val requesterId: String = "",
    val requesterName: String = "",
    val posterId: String = "",
    val status: String = "pending" // "pending", "accepted", "rejected"
)

data class ChatMessage(
    var id: String = "",
    val senderId: String = "",
    val text: String = "",
    val timestamp: Long = 0L
)

data class UserReview(
    var id: String = "",
    val reviewerId: String = "",
    val reviewerName: String = "",
    val targetUserId: String = "",
    val rating: Float = 0f,
    val reviewText: String = "",
    val timestamp: Long = 0L
)

data class UserProfile(
    val id: String = "",
    val name: String = "",
    val age: String = "",
    val gender: String = "",
    val sports: List<String> = emptyList(),
    val averageRating: Double = 0.0,
    val reviewCount: Int = 0,
    val profileImageBase64: String = "",
    val city: String = ""
)
