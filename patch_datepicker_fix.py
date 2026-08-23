with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

content = content.replace("val cal = java.util.Calendar.getInstance()\n                    android.app.DatePickerDialog(", "val cal = java.util.Calendar.getInstance(); android.app.DatePickerDialog(")

content = content.replace("dateStr = \"$d/${m+1}/$y\"\n                            android.app.TimePickerDialog(", "dateStr = \"$d/${m+1}/$y\"; android.app.TimePickerDialog(")

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
