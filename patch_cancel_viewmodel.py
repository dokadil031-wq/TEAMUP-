import re

with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    content = f.read()

target = """    fun requestToJoinMatch(match: MatchEntity, userName: String) {
        val uid = auth.currentUser?.uid ?: return
        val req = MatchRequest(
            matchId = match.id,
            matchTitle = match.title,
            requesterId = uid,
            requesterName = userName,
            posterId = match.posterId
        )
        val ref = db.collection("requests").document()
        ref.set(req.copy(id = ref.id))
    }"""

repl = """    fun requestToJoinMatch(match: MatchEntity, userName: String) {
        val uid = auth.currentUser?.uid ?: return
        val req = MatchRequest(
            matchId = match.id,
            matchTitle = match.title,
            requesterId = uid,
            requesterName = userName,
            posterId = match.posterId
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
    }"""

content = content.replace(target, repl)

with open("app/src/main/java/com/example/MaidanViewModel.kt", "w") as f:
    f.write(content)
