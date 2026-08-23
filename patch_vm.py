with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    content = f.read()

target = """    fun saveUserProfile(name: String, age: String, gender: String, sports: List<String>) {
        viewModelScope.launch {
            userPrefsRepo.saveUserProfile(name, age, gender, sports)
        }
        val uid = auth.currentUser?.uid ?: return
        db.collection("users").document(uid).get().addOnSuccessListener { doc ->
            val existingRating = doc.getDouble("averageRating") ?: 0.0
            val existingCount = doc.getLong("reviewCount")?.toInt() ?: 0
            val profile = UserProfile(uid, name, age, gender, sports, existingRating, existingCount)
            db.collection("users").document(uid).set(profile)
        }.addOnFailureListener {
            val profile = UserProfile(uid, name, age, gender, sports, 0.0, 0)
            db.collection("users").document(uid).set(profile)
        }
    }"""

replacement = """    fun saveUserProfile(name: String, age: String, gender: String, sports: List<String>) {
        viewModelScope.launch {
            userPrefsRepo.saveUserProfile(name, age, gender, sports)
        }
        val uid = auth.currentUser?.uid ?: return
        db.collection("users").document(uid).get().addOnSuccessListener { doc ->
            val existingRating = doc.getDouble("averageRating") ?: 0.0
            val existingCount = doc.getLong("reviewCount")?.toInt() ?: 0
            val existingImage = doc.getString("profileImageBase64") ?: ""
            val profile = UserProfile(uid, name, age, gender, sports, existingRating, existingCount, existingImage)
            db.collection("users").document(uid).set(profile)
        }.addOnFailureListener {
            val profile = UserProfile(uid, name, age, gender, sports, 0.0, 0, "")
            db.collection("users").document(uid).set(profile)
        }
    }

    fun updateProfilePhoto(base64: String) {
        val uid = auth.currentUser?.uid ?: return
        db.collection("users").document(uid).update("profileImageBase64", base64)
    }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/MaidanViewModel.kt", "w") as f:
    f.write(content)
