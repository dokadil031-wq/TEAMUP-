with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

content = content.replace("fun ProfileScreen(viewModel: MaidanViewModel) {", "fun ProfileScreen(viewModel: MaidanViewModel, onEditProfileClick: () -> Unit = {}) {")
content = content.replace("clickable { }.padding(horizontal = 12.dp, vertical = 6.dp)", "clickable { onEditProfileClick() }.padding(horizontal = 12.dp, vertical = 6.dp)")

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    main_content = f.read()

main_content = main_content.replace("\"Profile\" -> ProfileScreen(viewModel)", "\"Profile\" -> ProfileScreen(viewModel, onEditProfileClick = { currentScreen = \\\"profileSetup\\\" })")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(main_content)
