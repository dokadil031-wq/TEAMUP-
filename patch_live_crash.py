import re

with open("app/src/main/java/com/example/LiveActivity.kt", "r") as f:
    content = f.read()

target = """        val fragment = ZegoUIKitPrebuiltLiveStreamingFragment.newInstance(
            appID, appSign, userID, userName, liveID, config
        )
        
        supportFragmentManager.beginTransaction()
            .replace(android.R.id.content, fragment)
            .commitNow()"""

repl = """        try {
            val fragment = ZegoUIKitPrebuiltLiveStreamingFragment.newInstance(
                appID, appSign, userID, userName, liveID, config
            )
            
            supportFragmentManager.beginTransaction()
                .replace(android.R.id.content, fragment)
                .commitNow()
        } catch (e: Exception) {
            e.printStackTrace()
            android.widget.Toast.makeText(this, "Failed to start Zego SDK. Check AppSign.", android.widget.Toast.LENGTH_LONG).show()
            finish()
        }"""

content = content.replace(target, repl)

with open("app/src/main/java/com/example/LiveActivity.kt", "w") as f:
    f.write(content)
