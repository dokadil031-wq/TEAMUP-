with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    main_content = f.read()

main_content = main_content.replace("\\\"profileSetup\\\"", "\"profileSetup\"")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(main_content)
