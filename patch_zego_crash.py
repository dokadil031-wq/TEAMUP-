import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """            val config = com.zegocloud.uikit.prebuilt.call.invite.ZegoUIKitPrebuiltCallInvitationConfig()
            com.zegocloud.uikit.prebuilt.call.ZegoUIKitPrebuiltCallService.init(
                application, appID, appSign, currentUser.uid, userName, config
            )"""

repl = """            val config = com.zegocloud.uikit.prebuilt.call.invite.ZegoUIKitPrebuiltCallInvitationConfig()
            try {
                com.zegocloud.uikit.prebuilt.call.ZegoUIKitPrebuiltCallService.init(
                    application, appID, appSign, currentUser.uid, userName, config
                )
            } catch (e: Exception) {
                e.printStackTrace()
            }"""

content = content.replace(target, repl)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
