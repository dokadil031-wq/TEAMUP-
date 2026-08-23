import re
with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("Icons.AutoMirrored.Filled.ArrowBack", "Icons.Default.ArrowBack")

# Fix the end of file
idx = content.rfind("fun ProfileSetupScreen")
# Let's just find the last closing brace and remove everything after it. Wait, the extra braces are from my replacement mistake.
# The end of the file currently is:
'''
        }
    }
}
@Composable 
}
    }
}
'''
# I will replace it.
content = content.replace("}\n@Composable \n}\n    }\n}", "}\n")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content.strip() + "\n")
