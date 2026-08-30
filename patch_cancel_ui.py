import re

with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target1 = """        } else if (requestStatus == "requested" || requestStatus == "pending") {
            Button(
                onClick = { },
                colors = ButtonDefaults.buttonColors(containerColor = Turf2, contentColor = Bench),
                shape = RoundedCornerShape(12.dp),
                contentPadding = PaddingValues(vertical = 15.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Icon(Icons.Default.Schedule, contentDescription = null, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("Requested", fontSize = 15.sp, fontWeight = FontWeight.Bold)
            }
            Text("${match.posterName.split(" ").first()} will get a notification to accept.", color = Bench, fontSize = 12.sp, modifier = Modifier.padding(top = 10.dp).fillMaxWidth(), textAlign = androidx.compose.ui.text.style.TextAlign.Center)"""

repl1 = """        } else if (requestStatus == "requested" || requestStatus == "pending") {
            Button(
                onClick = { viewModel.cancelRequest(match.id) },
                colors = ButtonDefaults.buttonColors(containerColor = Turf2, contentColor = Bench),
                shape = RoundedCornerShape(12.dp),
                contentPadding = PaddingValues(vertical = 15.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Icon(Icons.Default.Schedule, contentDescription = null, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("Cancel Request", fontSize = 15.sp, fontWeight = FontWeight.Bold)
            }
            Text("Tap to cancel your pending request.", color = Bench, fontSize = 12.sp, modifier = Modifier.padding(top = 10.dp).fillMaxWidth(), textAlign = androidx.compose.ui.text.style.TextAlign.Center)"""
content = content.replace(target1, repl1)

target2 = """        } else if (requestStatus == "accepted") {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                Button(
                    onClick = { },
                    colors = ButtonDefaults.buttonColors(containerColor = Turf2, contentColor = Floodlight),
                    shape = RoundedCornerShape(12.dp),
                    contentPadding = PaddingValues(vertical = 15.dp),
                    border = androidx.compose.foundation.BorderStroke(1.dp, Line),
                    modifier = Modifier.weight(1f)
                ) {
                    Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("You're in", fontSize = 15.sp, fontWeight = FontWeight.Bold)
                }"""

repl2 = """        } else if (requestStatus == "accepted") {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                Button(
                    onClick = { viewModel.cancelRequest(match.id) },
                    colors = ButtonDefaults.buttonColors(containerColor = Turf2, contentColor = Floodlight),
                    shape = RoundedCornerShape(12.dp),
                    contentPadding = PaddingValues(vertical = 15.dp),
                    border = androidx.compose.foundation.BorderStroke(1.dp, Line),
                    modifier = Modifier.weight(1f)
                ) {
                    Icon(Icons.Default.Close, contentDescription = null, modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Cancel", fontSize = 15.sp, fontWeight = FontWeight.Bold)
                }"""
content = content.replace(target2, repl2)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
