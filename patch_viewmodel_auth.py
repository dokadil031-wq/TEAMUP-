import re

with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    content = f.read()

target = """        auth.addAuthStateListener {
            if (it.currentUser != null) {
                listenToMyRequests()
                listenToMyNotifications()
            } else {
                _myRequests.value = emptyList()
                _myNotifications.value = emptyList()
            }
        }"""

repl = """        auth.addAuthStateListener {
            if (it.currentUser != null) {
                listenToMyRequests()
                listenToMyNotifications()
                db.collection("users").document(it.currentUser!!.uid).get().addOnSuccessListener { doc ->
                    if (doc.exists()) {
                        val p = doc.toObject(UserProfile::class.java)
                        if (p != null) {
                            viewModelScope.launch {
                                userPrefsRepo.saveUserProfile(p.name, p.age, p.gender, p.sports)
                                if (p.profileImageBase64.isNotEmpty()) {
                                    userPrefsRepo.saveUserImage(p.profileImageBase64)
                                }
                            }
                        }
                    }
                }
            } else {
                _myRequests.value = emptyList()
                _myNotifications.value = emptyList()
                viewModelScope.launch {
                    userPrefsRepo.clearProfile()
                }
            }
        }"""

content = content.replace(target, repl)

with open("app/src/main/java/com/example/MaidanViewModel.kt", "w") as f:
    f.write(content)
