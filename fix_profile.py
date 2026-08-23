import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """        Spacer(modifier = Modifier.weight(1f))
        
        Text("Create Password", color = Chalk, fontSize = 14.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 8.dp, top = 16.dp))
        TextField(
            value = password,
            onValueChange = onPasswordChange,
            placeholder = { Text("At least 6 characters", color = Bench) },
            colors = TextFieldDefaults.colors(
                focusedContainerColor = Color.Transparent,
                unfocusedContainerColor = Color.Transparent,
                focusedIndicatorColor = Floodlight,
                unfocusedIndicatorColor = Line,
                focusedTextColor = Chalk,
                unfocusedTextColor = Chalk
            ),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
            modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp)
        )
        
        Button(
            onClick = onNext,"""

replacement = """        Spacer(modifier = Modifier.weight(1f))
        
        Button(
            onClick = onNext,"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
        f.write(content)
    print("Success")
else:
    print("Not found")

