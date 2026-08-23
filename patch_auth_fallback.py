import re

with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    content = f.read()

if "fun signInAnonymously" not in content:
    target = """    fun signIn(email: String, pass: String, onSuccess: () -> Unit, onError: (String) -> Unit) {
        auth.signInWithEmailAndPassword(email, pass)
            .addOnSuccessListener { onSuccess() }
            .addOnFailureListener { onError(it.message ?: "Error") }
    }"""
    replacement = """    fun signIn(email: String, pass: String, onSuccess: () -> Unit, onError: (String) -> Unit) {
        auth.signInWithEmailAndPassword(email, pass)
            .addOnSuccessListener { onSuccess() }
            .addOnFailureListener { onError(it.message ?: "Error") }
    }
    
    fun signInAnonymously(onSuccess: () -> Unit, onError: (String) -> Unit) {
        auth.signInAnonymously()
            .addOnSuccessListener { onSuccess() }
            .addOnFailureListener { onError(it.message ?: "Error") }
    }"""
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/MaidanViewModel.kt", "w") as f:
        f.write(content)

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                                onError = {
                                    viewModel.saveUserProfile(name, age, gender, selectedSports.toList())
                                    currentScreen = "main"
                                }"""
replacement = """                                onError = {
                                    viewModel.signInAnonymously(
                                        onSuccess = {
                                            viewModel.saveUserProfile(name, age, gender, selectedSports.toList())
                                            currentScreen = "main"
                                        },
                                        onError = {
                                            viewModel.saveUserProfile(name, age, gender, selectedSports.toList())
                                            currentScreen = "main"
                                        }
                                    )
                                }"""
content = content.replace(target, replacement)

# Do the same for AuthScreen (signIn)
target2 = """                    viewModel.signIn(
                        email = actualEmail,
                        pass = password,
                        onSuccess = { currentScreen = "main" },
                        onError = { currentScreen = "main" }
                    )"""
replacement2 = """                    viewModel.signIn(
                        email = actualEmail,
                        pass = password,
                        onSuccess = { currentScreen = "main" },
                        onError = { 
                            viewModel.signInAnonymously(
                                onSuccess = { currentScreen = "main" },
                                onError = { currentScreen = "main" }
                            )
                        }
                    )"""
content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
print("Auth fallback updated")
