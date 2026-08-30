with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    text = f.read()

target = '    fun updateProfilePhoto(base64: String) {'

repl = '''    fun updateUserCity(city: String) {
        viewModelScope.launch {
            userPrefsRepo.saveUserCity(city)
        }
        val uid = auth.currentUser?.uid ?: return
        db.collection("users").document(uid).update("city", city)
    }

    fun updateProfilePhoto(base64: String) {'''

text = text.replace(target, repl)

with open("app/src/main/java/com/example/MaidanViewModel.kt", "w") as f:
    f.write(text)
