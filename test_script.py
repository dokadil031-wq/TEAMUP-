import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    text = f.read()
    
# check accompanist logic
if "locationPermissions.launchMultiplePermissionRequest" in text:
    print("Uses Accompanist!")
