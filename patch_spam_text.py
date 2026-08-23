import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = 'Text("Enter your email address to receive a password reset link.", color = Bench, fontSize = 14.sp, modifier = Modifier.padding(bottom = 16.dp))'
replacement = 'Text("Enter your email address to receive a password reset link.\\n\\nNote: If you don\'t see it in your Inbox, please check your Spam/Junk folder.", color = Bench, fontSize = 14.sp, modifier = Modifier.padding(bottom = 16.dp))'

content = content.replace(target, replacement)

target_toast = 'android.widget.Toast.makeText(context, msg, android.widget.Toast.LENGTH_LONG).show()'
replacement_toast = 'android.widget.Toast.makeText(context, "Link sent! Please check your Inbox and Spam folder.", android.widget.Toast.LENGTH_LONG).show()'

content = content.replace(target_toast, replacement_toast)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
