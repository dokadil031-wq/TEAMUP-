import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """            try {
                com.zegocloud.uikit.prebuilt.call.ZegoUIKitPrebuiltCallService.init(
                    application, appID, appSign, currentUser.uid, userName, config
                )
            } catch (e: Exception) {
                e.printStackTrace()
            }"""

repl = """            try {
                com.zegocloud.uikit.prebuilt.call.ZegoUIKitPrebuiltCallService.init(
                    application, appID, appSign, currentUser.uid, userName, config
                )
            } catch (e: Exception) {
                e.printStackTrace()
                android.widget.Toast.makeText(context, "Zego SDK Init Failed. AppSign might be invalid.", android.widget.Toast.LENGTH_LONG).show()
            }"""

content = content.replace(target, repl)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
