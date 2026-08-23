import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """    var verificationId by remember { mutableStateOf("") }
    var isSendingOtp by remember { mutableStateOf(false) }
    val activity = LocalContext.current as Activity"""

replacement = """    var verificationId by remember { mutableStateOf("") }
    var isSendingOtp by remember { mutableStateOf(false) }
    val context = LocalContext.current
    val activity = remember(context) { 
        var ctx = context
        while (ctx is android.content.ContextWrapper) {
            if (ctx is Activity) break
            ctx = ctx.baseContext
        }
        ctx as Activity
    }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
