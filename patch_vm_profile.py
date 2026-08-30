with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    text = f.read()

text = text.replace('val userImage: StateFlow<String> = userPrefsRepo.userImage.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "")', 'val userImage: StateFlow<String> = userPrefsRepo.userImage.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "")\n    val userCity: StateFlow<String> = userPrefsRepo.userCity.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), "")')

text = text.replace('val profile = UserProfile(uid, name, age, gender, sports, existingRating, existingCount, existingImage)', 'val existingCity = doc.getString("city") ?: ""\n            val profile = UserProfile(uid, name, age, gender, sports, existingRating, existingCount, existingImage, existingCity)')
text = text.replace('val profile = UserProfile(uid, name, age, gender, sports, 0.0, 0, "")', 'val profile = UserProfile(uid, name, age, gender, sports, 0.0, 0, "", "")')

# in addAuthStateListener
text = text.replace('if (p.profileImageBase64.isNotEmpty()) {\n                                    userPrefsRepo.saveUserImage(p.profileImageBase64)\n                                }', 'if (p.profileImageBase64.isNotEmpty()) {\n                                    userPrefsRepo.saveUserImage(p.profileImageBase64)\n                                }\n                                if (p.city.isNotEmpty()) {\n                                    userPrefsRepo.saveUserCity(p.city)\n                                }')

with open("app/src/main/java/com/example/MaidanViewModel.kt", "w") as f:
    f.write(text)
