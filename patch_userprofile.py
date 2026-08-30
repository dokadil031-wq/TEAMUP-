import re

with open("app/src/main/java/com/example/UserProfileScreen.kt", "r") as f:
    content = f.read()

target1 = """    val currentUserName by viewModel.userName.collectAsStateWithLifecycle()
    val currentUserId = viewModel.auth.currentUser?.uid"""

replacement1 = """    val currentUserName by viewModel.userName.collectAsStateWithLifecycle()
    val currentUserId = viewModel.auth.currentUser?.uid
    val myRequests by viewModel.myRequests.collectAsStateWithLifecycle()
    val myNotifications by viewModel.myNotifications.collectAsStateWithLifecycle()"""

content = content.replace(target1, replacement1)

target2 = """        // Add review section
        if (currentUserId != null && currentUserId != targetUserId) {
            val hasReviewed = reviews.any { it.reviewerId == currentUserId }
            if (!hasReviewed) {"""

replacement2 = """        // Add review section
        if (currentUserId != null && currentUserId != targetUserId) {
            val hasReviewed = reviews.any { it.reviewerId == currentUserId }
            val hasPlayedTogether = myRequests.any { it.posterId == targetUserId && it.status == "accepted" } || 
                                    myNotifications.any { it.requesterId == targetUserId && it.status == "accepted" }
            if (!hasReviewed && hasPlayedTogether) {"""

content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/UserProfileScreen.kt", "w") as f:
    f.write(content)
