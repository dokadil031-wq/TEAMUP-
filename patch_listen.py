with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    lines = f.readlines()

def find_func_end(lines, start_idx):
    braces = 0
    for i in range(start_idx, len(lines)):
        if '{' in lines[i]:
            braces += lines[i].count('{')
        if '}' in lines[i]:
            braces -= lines[i].count('}')
        if braces == 0 and '{' in lines[start_idx:i+1][-1]:
            return i
    return -1

start_idx = -1
for i, line in enumerate(lines):
    if "private fun listenToMatches()" in line:
        start_idx = i
        break

if start_idx != -1:
    end_idx = find_func_end(lines, start_idx)
    new_code = """    private fun listenToMatches() {
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
"""
    lines[start_idx:end_idx+1] = [new_code]
    with open("app/src/main/java/com/example/MaidanViewModel.kt", "w") as f:
        f.writelines(lines)
