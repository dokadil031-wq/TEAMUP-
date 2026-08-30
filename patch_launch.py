import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    text = f.read()

target = '''                kotlinx.coroutines.Dispatchers.IO.invoke {
                    val city = LocationHelper.getCurrentCity(context)
                    if (city != null) {
                        viewModel.updateUserCity(city)
                    }
                }'''

repl = '''                val city = LocationHelper.getCurrentCity(context)
                if (city != null) {
                    viewModel.updateUserCity(city)
                }'''

text = text.replace(target, repl)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(text)
