with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    content = f.read()

target1 = """    val userSports: StateFlow<List<String>> = userPrefsRepo.userSports.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())"""
replacement1 = """    val userSports: StateFlow<List<String>> = userPrefsRepo.userSports.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
    val userImage: StateFlow<String> = userPrefsRepo.userImage.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "")"""

target2 = """    fun updateProfilePhoto(base64: String) {
        val uid = auth.currentUser?.uid ?: return
        db.collection("users").document(uid).update("profileImageBase64", base64)
    }"""
replacement2 = """    fun updateProfilePhoto(base64: String) {
        val uid = auth.currentUser?.uid ?: return
        viewModelScope.launch {
            userPrefsRepo.saveUserImage(base64)
        }
        db.collection("users").document(uid).update("profileImageBase64", base64)
    }"""

content = content.replace(target1, replacement1).replace(target2, replacement2)
with open("app/src/main/java/com/example/MaidanViewModel.kt", "w") as f:
    f.write(content)
