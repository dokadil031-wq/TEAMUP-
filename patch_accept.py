import re

with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    content = f.read()

# Patch acceptRequest
accept_target = """    fun acceptRequest(req: MatchRequest) {
        db.collection("requests").document(req.id).update("status", "accepted")
        db.collection("matches").document(req.matchId).get().addOnSuccessListener { doc ->
            val joined = doc.getLong("joined") ?: 0
            doc.reference.update("joined", joined + 1)
        }
    }"""
accept_repl = """    fun acceptRequest(req: MatchRequest) {
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
    }"""
content = content.replace(accept_target, accept_repl)

# Patch listenToMatches
listen_target = """                val matches = snapshot.documents.mapNotNull { doc ->
                    doc.toObject(MatchEntity::class.java)?.apply { id = doc.id }
                }
                _allMatches.value = matches"""
listen_repl = """                val matches = snapshot.documents.mapNotNull { doc ->
                    doc.toObject(MatchEntity::class.java)?.apply { id = doc.id }
                }
                
                val currentTime = System.currentTimeMillis()
                val validMatches = mutableListOf<MatchEntity>()
                
                for (match in matches) {
                    var shouldDelete = false
                    if (match.fullAtTimestamp != null && match.fullAtTimestamp > 0) {
                        // 30 minutes = 30 * 60 * 1000 = 1800000 ms
                        if (currentTime > match.fullAtTimestamp + 1800000L) {
                            shouldDelete = true
                        }
                    } else if (match.joined < match.total && match.timestamp > 0) {
                        // Delete right at match time if not full
                        if (currentTime > match.timestamp) {
                            shouldDelete = true
                        }
                    }
                    
                    if (shouldDelete) {
                        db.collection("matches").document(match.id).delete()
                    } else {
                        validMatches.add(match)
                    }
                }
                _allMatches.value = validMatches"""
content = content.replace(listen_target, listen_repl)

with open("app/src/main/java/com/example/MaidanViewModel.kt", "w") as f:
    f.write(content)
