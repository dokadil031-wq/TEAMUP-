import re

with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target_launcher = """    val launcher = rememberLauncherForActivityResult(contract = ActivityResultContracts.PickVisualMedia()) { uri: Uri? ->
        uri?.let {
            try {
                val inputStream: InputStream? = context.contentResolver.openInputStream(it)
                val originalBitmap = BitmapFactory.decodeStream(inputStream)
                // Resize and compress
                val maxSize = 400
                val ratio = Math.min(maxSize.toFloat() / originalBitmap.width, maxSize.toFloat() / originalBitmap.height)
                val width = Math.round(ratio * originalBitmap.width)
                val height = Math.round(ratio * originalBitmap.height)
                val resizedBitmap = Bitmap.createScaledBitmap(originalBitmap, width, height, false)
                val outputStream = ByteArrayOutputStream()
                resizedBitmap.compress(Bitmap.CompressFormat.JPEG, 70, outputStream)
                val byteArray = outputStream.toByteArray()
                val base64 = Base64.encodeToString(byteArray, Base64.DEFAULT)
                viewModel.updateProfilePhoto(base64)
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }"""

replace_launcher = """    val launcher = androidx.activity.compose.rememberLauncherForActivityResult(
        contract = androidx.activity.result.contract.ActivityResultContracts.TakePicturePreview()
    ) { bitmap: android.graphics.Bitmap? ->
        if (bitmap != null) {
            val outputStream = java.io.ByteArrayOutputStream()
            bitmap.compress(android.graphics.Bitmap.CompressFormat.JPEG, 80, outputStream)
            val byteArray = outputStream.toByteArray()
            val base64 = android.util.Base64.encodeToString(byteArray, android.util.Base64.DEFAULT)
            viewModel.updateProfilePhoto(base64)
        }
    }

    val cameraPermissionLauncher = androidx.activity.compose.rememberLauncherForActivityResult(
        contract = androidx.activity.result.contract.ActivityResultContracts.RequestPermission()
    ) { isGranted: Boolean ->
        if (isGranted) {
            launcher.launch(null)
        }
    }"""

content = content.replace(target_launcher, replace_launcher)

target_clickable = """                    .clickable { launcher.launch(androidx.activity.result.PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)) },"""

replace_clickable = """                    .clickable {
                        if (androidx.core.content.ContextCompat.checkSelfPermission(context, android.Manifest.permission.CAMERA) == android.content.pm.PackageManager.PERMISSION_GRANTED) {
                            launcher.launch(null)
                        } else {
                            cameraPermissionLauncher.launch(android.Manifest.permission.CAMERA)
                        }
                    },"""

content = content.replace(target_clickable, replace_clickable)

with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
