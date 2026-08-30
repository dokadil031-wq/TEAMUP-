import re

with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    content = f.read()

target_init = """    init {
        auth.firebaseAuthSettings.setAppVerificationDisabledForTesting(true)
        listenToMatches()"""

repl_init = """    init {
        auth.firebaseAuthSettings.setAppVerificationDisabledForTesting(true)
        listenToMatches()
        viewModelScope.launch {
            while (true) {
                kotlinx.coroutines.delay(30000) // check every 30 seconds
                checkAndDeleteExpiredMatches()
            }
        }"""

content = content.replace(target_init, repl_init)

target_listen = """    private fun listenToMatches() {
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
                _allMatches.value = validMatches
                
            }
        }
    }"""

repl_listen = """    private fun listenToMatches() {
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
    }"""

content = content.replace(target_listen, repl_listen)

with open("app/src/main/java/com/example/MaidanViewModel.kt", "w") as f:
    f.write(content)
