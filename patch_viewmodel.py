with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    content = f.read()

target_imports = "import kotlinx.coroutines.launch"
replacement_imports = """import kotlinx.coroutines.launch
import com.google.firebase.firestore.Query"""
content = content.replace(target_imports, replacement_imports)

target_vars = """    private val _allMatches = MutableStateFlow<List<MatchEntity>>(emptyList())
    val allMatches: StateFlow<List<MatchEntity>> = _allMatches.asStateFlow()"""
replacement_vars = target_vars + """

    private val _myRequests = MutableStateFlow<List<MatchRequest>>(emptyList())
    val myRequests: StateFlow<List<MatchRequest>> = _myRequests.asStateFlow()

    private val _myNotifications = MutableStateFlow<List<MatchRequest>>(emptyList())
    val myNotifications: StateFlow<List<MatchRequest>> = _myNotifications.asStateFlow()"""
content = content.replace(target_vars, replacement_vars)

target_init = """    init {
        auth.firebaseAuthSettings.setAppVerificationDisabledForTesting(true)
        listenToMatches()
    }"""
replacement_init = """    init {
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
    }"""
content = content.replace(target_init, replacement_init)

target_addmatch = "        ref.set(match.copy(id = ref.id)).addOnFailureListener {"
replacement_addmatch = "        ref.set(match.copy(id = ref.id, posterId = auth.currentUser?.uid ?: \"\")).addOnFailureListener {"
content = content.replace(target_addmatch, replacement_addmatch)

target_joinmatch = """    fun joinMatch(match: MatchEntity) {
        if (match.id.isNotEmpty()) {
            db.collection("matches").document(match.id).update("joined", match.joined + 1)
        }
    }"""
replacement_joinmatch = target_joinmatch + """

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
    }"""
content = content.replace(target_joinmatch, replacement_joinmatch)

with open("app/src/main/java/com/example/MaidanViewModel.kt", "w") as f:
    f.write(content)

