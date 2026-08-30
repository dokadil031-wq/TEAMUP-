import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target1 = """    if (showSplash) {
        SplashScreen()
        return
    }"""

content = content.replace(target1, "")

target2 = """    Box(
        modifier = modifier
            .fillMaxSize()
            .background(Pitch)
    ) {"""

repl2 = """    if (showSplash) {
        SplashScreen()
    } else {
    Box(
        modifier = modifier
            .fillMaxSize()
            .background(Pitch)
    ) {"""

content = content.replace(target2, repl2)

target3 = """                    }
                }
            }
        }
    }
}

@Composable
fun StepDots"""

repl3 = """                    }
                }
            }
        }
    }
    }
}

@Composable
fun StepDots"""

content = content.replace(target3, repl3)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
