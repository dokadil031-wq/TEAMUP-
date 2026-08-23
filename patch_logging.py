import re

with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    content = f.read()

target = """    private fun listenToMatches() {
        db.collection("matches").addSnapshotListener { snapshot, error ->
            if (error != null) {
                return@addSnapshotListener
            }"""

replacement = """    private fun listenToMatches() {
        db.collection("matches").addSnapshotListener { snapshot, error ->
            if (error != null) {
                android.util.Log.e("FirestoreError", "Listen failed.", error)
                return@addSnapshotListener
            }"""

content = content.replace(target, replacement)

target2 = """    fun addMatch(match: MatchEntity) {
        val ref = db.collection("matches").document()
        ref.set(match.copy(id = ref.id))
    }"""

replacement2 = """    fun addMatch(match: MatchEntity) {
        val ref = db.collection("matches").document()
        ref.set(match.copy(id = ref.id)).addOnFailureListener {
            android.util.Log.e("FirestoreError", "Add match failed.", it)
        }
    }"""

content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/MaidanViewModel.kt", "w") as f:
    f.write(content)
