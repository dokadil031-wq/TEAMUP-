with open("app/src/main/java/com/example/Models.kt", "r") as f:
    content = f.read()

target = """data class UserProfile(
    val id: String = "",
    val name: String = "",
    val age: String = "",
    val gender: String = "",
    val sports: List<String> = emptyList(),
    val averageRating: Double = 0.0,
    val reviewCount: Int = 0
)"""

replacement = """data class UserProfile(
    val id: String = "",
    val name: String = "",
    val age: String = "",
    val gender: String = "",
    val sports: List<String> = emptyList(),
    val averageRating: Double = 0.0,
    val reviewCount: Int = 0,
    val profileImageBase64: String = ""
)"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/Models.kt", "w") as f:
    f.write(content)
