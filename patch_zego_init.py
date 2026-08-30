import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """    val userName by viewModel.userName.collectAsStateWithLifecycle()"""
repl = """    val userName by viewModel.userName.collectAsStateWithLifecycle()
    
    val currentUser = viewModel.auth.currentUser
    androidx.compose.runtime.LaunchedEffect(currentUser?.uid, userName) {
        if (currentUser != null && userName.isNotEmpty()) {
            val application = context.applicationContext as android.app.Application
            val appID: Long = 259383851L
            val appSign = "ead2e75a111bd2bfaddc3d0687cdd98175b3398"
            val config = com.zegocloud.uikit.prebuilt.call.invite.ZegoUIKitPrebuiltCallInvitationConfig()
            com.zegocloud.uikit.prebuilt.call.ZegoUIKitPrebuiltCallService.init(
                application, appID, appSign, currentUser.uid, userName, config
            )
        }
    }"""

content = content.replace(target, repl)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
