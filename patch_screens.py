import re

with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target_signature = 'fun ProfileScreen(viewModel: MaidanViewModel, onEditProfileClick: () -> Unit = {}) {'
replacement_signature = 'fun ProfileScreen(viewModel: MaidanViewModel, onEditProfileClick: () -> Unit = {}, onLogoutClick: () -> Unit = {}) {'
content = content.replace(target_signature, replacement_signature)

target_edit_row = '''        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
            Box(modifier = Modifier.clip(RoundedCornerShape(20.dp)).border(1.dp, Line, RoundedCornerShape(20.dp)).clickable { onEditProfileClick() }.padding(horizontal = 12.dp, vertical = 6.dp)) {
                Text("Edit profile", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
            }
        }'''
replacement_edit_row = '''        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End, verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.clip(RoundedCornerShape(20.dp)).border(1.dp, Line, RoundedCornerShape(20.dp)).clickable { onEditProfileClick() }.padding(horizontal = 12.dp, vertical = 6.dp)) {
                Text("Edit profile", color = Bench, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
            }
            Spacer(modifier = Modifier.width(8.dp))
            Box(modifier = Modifier.clip(RoundedCornerShape(20.dp)).border(1.dp, Color(0xFFEF4444), RoundedCornerShape(20.dp)).clickable { onLogoutClick() }.padding(horizontal = 12.dp, vertical = 6.dp)) {
                Text("Logout", color = Color(0xFFEF4444), fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
            }
        }'''
content = content.replace(target_edit_row, replacement_edit_row)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
